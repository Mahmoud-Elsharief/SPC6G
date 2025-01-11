# calculations.py
import numpy as np
from scipy.special import erf
import math

def calculate_d_int(P_t, K_0, gamma, d_ij, alpha, N_0):
    """
    Calculate the interference distance (d_int).

    Parameters:
    P_t   -- Transmitted power
    K_0   -- Path gain constant
    gamma -- Signal-to-noise ratio (SNR)
    d_ij  -- Distance between transmitter and receiver
    alpha -- Path loss exponent
    N_0   -- Noise power

    Returns:
    d_int -- Interference distance
    """
    numerator = P_t * K_0
    denominator = (P_t * K_0) / (gamma * d_ij ** alpha) - N_0
    d_int = (numerator / denominator) ** (1 / alpha)
    return d_int

def calculate_RU(R, spsr, op):
    """
    Calculate the Resource Utilization (RU).

    Parameters:
    R    -- Total resources
    spsr -- Sensed Packet Sensing Ratio
    op   -- Overlap probability

    Returns:
    RU -- Calculated resource utilization value
    """
    RU = R * (1 - (1 - op) ** spsr)
    return RU

def calculate_u_dik(R, RU, common_neighbors_count, spsr):
    """
    Calculate the utility function u_dik.

    Parameters:
    - R: Total resources.
    - RU: Resources utilized.
    - common_neighbors_count: Number of common neighbors.
    - spsr: Sensed Packet Sensing Ratio.

    Returns:
    - u_dik: Calculated utility value.
    """
    return (RU**2 / R) * (1 - common_neighbors_count / spsr) + RU * (common_neighbors_count / spsr)

def calculate_o_dik(R, RU, u_dik):
    """
    Calculate o(d_(i,k)), the overlap resource count.

    Parameters:
    R     -- Total resources
    RU    -- Resources utilized
    u_dik -- Utility value

    Returns:
    o_dik -- Overlap resource count
    """
    o_dik = R - 2 * RU + u_dik
    return o_dik

def calculate_mu(rc1, rc2, psr_value):
    """
    Calculate the value of μ(d_(i,k)) based on resource configuration.

    Parameters:
    rc1, rc2 -- Resource configuration parameters
    psr_value -- Packet Success Rate value

    Returns:
    mu -- Calculated μ(d_(i,k))
    """
    mu = (1 - (1 - (2 / (rc1 + rc2))) * psr_value)
    return mu

def calculate_p_dik(mu_dik, o_dik, channels, R_f):
    """
    Calculate p(d_(i,k)).

    Parameters:
    mu_dik -- μ(d_(i,k)), a calculated value based on the distance and other factors
    o_dik  -- Overlap resource count
    channels -- Total number of communication channels
    R_f    -- A constant representing the total number of resources

    Returns:
    p_dik -- The calculated p(d_(i,k)) value
    """
    p_dik = mu_dik * o_dik * (channels / R_f)**2
    return p_dik

def calculate_ps_dik(p_dik, p_res_ik):
    """
    Calculate p_s(d_(i,k)).

    Parameters:
    p_dik    -- Probability of interference
    p_res_ik -- Probability of successful reception

    Returns:
    p_s_dik -- Calculated success probability
    """
    p_s_dik = (1 - p_dik) + p_dik * (1 - p_res_ik)
    return p_s_dik

def calculate_prr_dij(p_o_dij):
    """
    Calculate Packet Reception Ratio (PRR) for a given distance.

    Parameters:
    p_o_dij -- Packet transmission outage probability

    Returns:
    prr_dij -- Packet Reception Ratio (PRR)
    """
    prr_dij = 1 - p_o_dij
    return prr_dij

def calculate_pir_dij(p_o_dij, RRI):
    """
    Calculate Packet Inter-Reception Rate (PIR).

    Parameters:
    p_o_dij -- Packet transmission outage probability
    RRI     -- Resource reservation interval

    Returns:
    PIR -- Packet Inter-Reception value
    """
    if p_o_dij >= 1:
        return float('inf')  # PIR is infinite if outage probability is 1
    PIR = RRI / (1 - p_o_dij)
    return PIR

def PathLoss(d, K0_dB, gamma):
    """
    Calculate path loss (PL) and standard deviation (std_dev).

    Parameters:
    d      -- Distance between nodes
    K0_dB  -- Reference path loss in dB
    gamma  -- Path loss exponent

    Returns:
    PL     -- Path loss in dB
    std_dev -- Standard deviation for shadowing
    """
    d = np.asarray(d)
    PL = -K0_dB + 10 * gamma * np.log10(d)
    std_dev = 3  # Example constant for standard deviation
    return PL, std_dev

def PSR(d, Pt_dBm, P_sen_dBm, K0_dB, gamma):
    """
    Calculate Packet Success Rate (PSR).

    Parameters:
    d         -- Distance between transmitter and receiver
    Pt_dBm    -- Transmission power in dBm
    P_sen_dBm -- Receiver sensitivity in dBm
    K0_dB     -- Reference path loss in dB
    gamma     -- Path loss exponent

    Returns:
    PSR -- Packet Success Rate
    """
    PL, std_dev = PathLoss(np.abs(d) + 1, K0_dB, gamma)
    PSR_value = 0.5 * (1 + erf((Pt_dBm - PL - P_sen_dBm) / (std_dev * np.sqrt(2))))
    return PSR_value

def SPSR(beta, P_t_dB, P_s_dB, K_0_dB, alpha):
    """
    Compute the Sensed Packet Sensing Ratio (SPSR).

    Parameters:
    beta    -- Traffic density
    P_t_dB  -- Transmission power in dB
    P_s_dB  -- Receiver sensitivity in dB
    K_0_dB  -- Reference path loss in dB
    alpha   -- Path loss exponent

    Returns:
    SPSR -- Computed SPSR value
    """
    distances = np.arange(-2000, 2000, 1)
    psr_values = PSR(distances, P_t_dB, P_s_dB, K_0_dB, alpha)
    spsr_sum = np.sum(psr_values)
    return beta * spsr_sum

def rho(d_i_k, sigma):
    """
    Calculate correlation factor rho.

    Parameters:
    d_i_k -- Distance between vehicles
    sigma -- Standard deviation of the sensing range

    Returns:
    rho -- Correlation factor
    """
    return np.exp(-d_i_k)

def common_neighbors(beta, P_t_dB, P_s_dB, K_0_dB, alpha, d_i_k):
    """
    Calculate the number of common neighbors between two vehicles.

    Parameters:
    beta      -- Traffic density
    P_t_dB    -- Transmission power in dB
    P_s_dB    -- Receiver sensitivity in dB
    K_0_dB    -- Reference path loss in dB
    alpha     -- Path loss exponent
    d_i_k     -- Distance between vehicles

    Returns:
    common_neighbors -- Number of common neighbors
    """
    distances = np.arange(-2000, 2000, 1)
    psr_i = PSR(distances, P_t_dB, P_s_dB, K_0_dB, alpha)
    psr_k = PSR(np.abs(distances - d_i_k), P_t_dB, P_s_dB, K_0_dB, alpha)
    correlation_factor = rho(d_i_k, 3)
    common_psr = correlation_factor * np.minimum(psr_i, psr_k) + (1 - correlation_factor) * psr_i * psr_k
    common_neighbors_sum = np.sum(common_psr)
    return beta * common_neighbors_sum
