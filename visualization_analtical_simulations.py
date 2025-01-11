# plot_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.cm import get_cmap

# Define a function to ensure the folder exists
def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Function to compare beta with a given tolerance
def compare_beta_with_tolerance(beta1, beta2, tol=1e-3):
    return abs(beta1 - beta2) < tol

# Function to find the communication range
def find_communication_range(data, PRR_threshold):
    valid_data = data[data['cumulative_PDR'] >= PRR_threshold]
    if not valid_data.empty:
        return valid_data['distance_bin'].max()
    else:
        return 0  # Return 0 if no distance satisfies the condition

# Set plot parameters for IEEE Transactions style
plt.rcParams.update({
    'font.size': 16,              # Font size for readability
    'axes.labelsize': 20,         # Axis labels size
    'axes.titlesize': 16,         # Title size
    'legend.fontsize': 13,        # Legend size
    'lines.linewidth': 3,         # Line width
    'lines.markersize': 6,        # Marker size
    'figure.figsize': (10, 6),    # Default figure size
    'grid.linestyle': '--',       # Grid line style
})

# Load data paths
analytical_data_path = 'analytical_simulation_metrics.csv'  # Analytical data
metric_data_path = 'sim_metrics_data.csv'  # Simulation metric data

# Load the data
analytical_df = pd.read_csv(analytical_data_path)
metric_df = pd.read_csv(metric_data_path)

# Map protocol types
protocol_names = {0: 'NRV2X', 2: 'SPC6G'}
metric_df['protocol_type'] = metric_df['protocol_type'].map(protocol_names)

# Map num_lanes to beta (reverse relationship)
metric_df['beta'] = metric_df['num_lanes'] / 40

# Unique values for MCS, numerology, and protocol
unique_mcs = analytical_df['MCS'].unique()
unique_numerology = analytical_df['numerology'].unique()
unique_protocols = ['SPC6G', 'NRV2X']

# Plot settings
output_folder = 'SPS6G_plots'
ensure_folder_exists(output_folder)

# Plot PDR and PIR for each combination of MCS, numerology, and beta
for mcs in unique_mcs:
    for numerology in unique_numerology:
        # PDR Plot
        plt.figure()
        for protocol in unique_protocols:
            protocol_name = protocol_names.get(protocol, f'{protocol}')

            # Filter analytical and metric data
            analytical_data = analytical_df[
                (analytical_df['protocol_type'] == protocol) &
                (analytical_df['MCS'] == mcs) &
                (analytical_df['numerology'] == numerology)
            ]

            metric_data = metric_df[
                (metric_df['protocol_type'] == protocol) &
                (metric_df['MCS'] == mcs) &
                (metric_df['numerology'] == numerology)
            ]

            # Plot data for each beta
            for beta in analytical_data['beta'].unique():
                analytical_data_beta = analytical_data[analytical_data['beta'] == beta]
                metric_data_beta = metric_data[metric_data['beta'].apply(lambda x: compare_beta_with_tolerance(x, beta))]

                # Plot Analytical Data
                if not analytical_data_beta.empty:
                    plt.plot(
                        analytical_data_beta['distance_bin'],
                        analytical_data_beta['cumulative_PDR'],
                        label=f'Ana. {protocol_name}, $\\beta$={beta}',
                        linestyle='--', marker='o'
                    )

                # Plot Simulation Data
                if not metric_data_beta.empty:
                    plt.plot(
                        metric_data_beta['distance_bin'],
                        metric_data_beta['cumulative_PDR'],
                        label=f'Sim. {protocol_name}, $\\beta$={beta}',
                        linestyle='-', marker='x'
                    )

        # Customize PDR plot
        plt.ylim(0.7, 1)
        plt.xlabel('Distance (m)')
        plt.ylabel('PRR')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'{output_folder}/PDR_MCS{mcs}_Numerology{numerology}.pdf', format='pdf')
        plt.show()

        # PIR Plot
        plt.figure()
        for protocol in unique_protocols:
            protocol_name = protocol_names.get(protocol, f'{protocol}')

            # Filter analytical and metric data
            analytical_data = analytical_df[
                (analytical_df['protocol_type'] == protocol) &
                (analytical_df['MCS'] == mcs) &
                (analytical_df['numerology'] == numerology)
            ]

            metric_data = metric_df[
                (metric_df['protocol_type'] == protocol) &
                (metric_df['MCS'] == mcs) &
                (metric_df['numerology'] == numerology)
            ]

            # Plot data for each beta
            for beta in analytical_data['beta'].unique():
                analytical_data_beta = analytical_data[analytical_data['beta'] == beta]
                metric_data_beta = metric_data[metric_data['beta'].apply(lambda x: compare_beta_with_tolerance(x, beta))]

                # Plot Analytical Data
                if not analytical_data_beta.empty:
                    plt.plot(
                        analytical_data_beta['distance_bin'],
                        analytical_data_beta['cumulative_PIR'],
                        label=f'Ana. {protocol_name}, $\\beta$={beta}',
                        linestyle='--', marker='o'
                    )

                # Plot Simulation Data
                if not metric_data_beta.empty:
                    plt.plot(
                        metric_data_beta['distance_bin'],
                        metric_data_beta['cumulative_PIR'],
                        label=f'Sim. {protocol_name}, $\\beta$={beta}',
                        linestyle='-', marker='x'
                    )

        # Customize PIR plot
        plt.ylim(0.1, 0.18)
        plt.xlabel('Distance (m)')
        plt.ylabel('PIR (s)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'{output_folder}/PIR_MCS{mcs}_Numerology{numerology}.pdf', format='pdf')
        plt.show()

# Communication Range vs MCS
unique_betas = analytical_df['beta'].unique()
PRR_threshold = 0.98
communication_ranges = {protocol: {beta: [] for beta in unique_betas} for protocol in unique_protocols}

for protocol in unique_protocols:
    for beta in unique_betas:
        for mcs in unique_mcs:
            analytical_data_beta_mcs = analytical_df[
                (analytical_df['protocol_type'] == protocol) &
                (analytical_df['MCS'] == mcs) &
                (analytical_df['beta'] == beta)
            ]
            comm_range = find_communication_range(analytical_data_beta_mcs, PRR_threshold)
            communication_ranges[protocol][beta].append(comm_range)

# Generate bar plots
color_map = get_cmap('tab10')
colors = [color_map(i / (len(unique_protocols) * len(unique_betas))) for i in range(len(unique_protocols) * len(unique_betas))]

bar_width = 0.08
space_between_betas = 0.02
space_between_protocols = 0.15
index = np.arange(len(unique_mcs))
group_width = (len(unique_protocols) * len(unique_betas) * bar_width) + space_between_protocols

for i, protocol in enumerate(unique_protocols):
    for j, beta in enumerate(unique_betas):
        bar_positions = index + i * (len(unique_betas) * (bar_width + space_between_betas)) + j * (bar_width + space_between_betas) + i * space_between_protocols
        plt.bar(
            bar_positions,
            communication_ranges[protocol][beta],
            bar_width,
            label=f'{protocol}, $\\beta$={beta}',
            color=colors[i * len(unique_betas) + j]
        )

# Customize bar plot
plt.xlabel('MCS Index')
plt.ylabel('PRR Distance (m)')
plt.xticks(index + group_width / 2 - bar_width / 2, unique_mcs)
plt.legend(loc='upper center', bbox_to_anchor=(0.4, 1))
plt.grid(True, axis='y')
plt.tight_layout()

# Save bar plot
plt.savefig(f'{output_folder}/Communication_Range_vs_MCS_BarPlot.pdf', format='pdf')
plt.show()
