# calculations.py
import numpy as np
from scipy.special import erf
import math
from calculations import *


def calculate_analytical_results(
    channels, sinr_threshold_dB, beta, P_t_dB, fc, alpha, P_s_dB, N_0_dB, 
    maxchannel, slot, s, rc1, rc2, rri, p_res_ik, max_distance, step_distance
):
    """
    Calculate analytical PRR and PIR for SPC6G and NRV2X protocols.

    Parameters:
    - channels: Total number of communication channels.
    - sinr_threshold_dB: SINR threshold in dB.
    - beta: Beta coefficient for resource allocation.
    - P_t_dB: Transmission power in dB.
    - fc: Carrier frequency in GHz.
    - alpha: Path loss exponent.
    - P_s_dB: Noise power in dB.
    - N_0_dB: Noise power density in dB.
    - maxchannel: Maximum number of channels.
    - slot: Slot duration.
    - s: Channel sensing parameter.
    - rc1, rc2: Resource configuration parameters.
    - rri: Resource reservation interval.
    - p_res_ik: Probability of successful reception.
    - max_distance: Maximum distance between transmitter and receiver.
    - step_distance: Distance increment for analysis.

    Returns:
    - PRR and PIR results for SPC6G and NRV2X protocols.
    """
    # Convert parameters from dB to linear scale
    P_s = 10 ** (P_s_dB / 10)
    P_t = 10 ** (P_t_dB / 10)
    K_0_dB = -(32.4 + 20 * math.log10(fc))  # Path loss constant in dB
    K_0 = 10 ** (K_0_dB / 10)
    N_0 = 10 ** (N_0_dB / 10)
    sinr_threshold = 10 ** (sinr_threshold_dB / 10)

    # Initialize distance range
    distances = list(range(0, max_distance + step_distance, step_distance))

    # Initialize result containers
    prr_spc6G, prr_nrv2x = [], []
    pir_spc6G, pir_nrv2x = [], []

    # Calculate resources (R) and sensing ratios
    channel_slot = maxchannel / channels
    R = maxchannel * (rri / slot)
    spsr = SPSR(beta, P_t_dB, P_s_dB, K_0_dB, alpha)
    RU = calculate_RU(R, spsr, channels / R)
      
    # Adjust sensing threshold
    while RU > (1 - s) * R:
        P_s_dB += 3  # Increment noise power
        spsr = SPSR(beta, P_t_dB, P_s_dB, K_0_dB, alpha)
        RU = calculate_RU(R, spsr, channels / R)

    # Loop through distances and calculate metrics
    for d_ij in distances:
        d_int = calculate_d_int(P_t, K_0, sinr_threshold, d_ij + 1, alpha, N_0)
        d_min, d_max = d_ij - d_int, d_ij + d_int
        d_ik_range = range(int(d_min), int(d_max), int(1 / beta))

        ps_values, ps_dik_nr_values = [], []
        for dik in d_ik_range:
            d_ik = abs(dik)
            psr_value = PSR(d_ik, P_t_dB, P_s_dB, K_0_dB, alpha)
            common_neighbors_count = common_neighbors(beta,  P_t_dB, P_s_dB, K_0_dB, alpha, d_ik)
            u_dik = calculate_u_dik(R, RU, common_neighbors_count, spsr)
            o_dik = calculate_o_dik(R, RU, u_dik)
            mu_dik=calculate_mu( rc1, rc2, psr_value)
            p_dik = calculate_p_dik(mu_dik, o_dik, channels, R - RU)
            ps_dik = calculate_ps_dik(p_dik, RU/R)
            ps_dik_nr = 1 - p_dik
            

            ps_values.append(ps_dik)
            ps_dik_nr_values.append(ps_dik_nr)
            

        # Calculate PRR and PIR for SPC6G and NRV2X
        prr_spc6G.append(calculate_prr_dij(1-np.prod(ps_values)))
        prr_nrv2x.append(calculate_prr_dij(1-np.prod(ps_dik_nr_values)))
        pir_spc6G.append(calculate_pir_dij(1-np.prod(ps_values), rri))
        pir_nrv2x.append(calculate_pir_dij(1-np.prod(ps_dik_nr_values), rri))

    return prr_spc6G, prr_nrv2x, pir_spc6G, pir_nrv2x

