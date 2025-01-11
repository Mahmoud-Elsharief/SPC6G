# plot_simulation_urban.py
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define a function to ensure the folder exists
def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Load the simulation metric data
metric_data_path = 'sim_metrics_data_urban.csv'  # Path to the simulation metric data file
metric_df = pd.read_csv(metric_data_path)

# Set plot parameters for IEEE Transactions style
plt.rcParams.update({
    'font.size': 16,              # Font size for readability
    'axes.labelsize': 20,         # Axis labels size
    'axes.titlesize': 16,         # Title size
    'legend.fontsize': 14,        # Legend size
    'lines.linewidth': 3,         # Line width
    'lines.markersize': 6,        # Marker size
    'figure.figsize': (10, 6),    # Default figure size
    'grid.linestyle': '--',       # Grid line style
})

# Specify folder to save plots
output_folder = 'SPC6G_plots_sim_urban'
ensure_folder_exists(output_folder)

# Map protocol types in the metric data (0 = NRV2X, 2 = SPC6G)
protocol_names = {0: 'NRV2X', 2: 'SPC6G'}
metric_df['protocol_type'] = metric_df['protocol_type'].map(protocol_names)

# Extract unique values for MCS, numerology, and protocols
unique_mcs = metric_df['MCS'].unique()
unique_numerology = metric_df['numerology'].unique()
unique_protocols = ['SPC6G', 'NRV2X']

# Iterate over MCS and numerology to plot PDR and PIR
for mcs in unique_mcs:
    for numerology in unique_numerology:

        # Plot PDR (Packet Delivery Ratio)
        plt.figure()
        for protocol in unique_protocols:
            # Filter simulation data for PDR
            metric_data = metric_df[
                (metric_df['protocol_type'] == protocol) &
                (metric_df['MCS'] == mcs) &
                (metric_df['numerology'] == numerology)
            ]

            # Plot simulation data if available
            if not metric_data.empty:
                plt.plot(
                    metric_data['distance_bin'],
                    metric_data['cumulative_PDR'],
                    label=f'{protocol}',
                    linestyle='-', marker='x'
                )

        # Customize PDR plot
        plt.ylim(0.7, 1)
        plt.xlabel('Distance (m)')
        plt.ylabel('PRR')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save PDR plot
        plt.savefig(f'{output_folder}/PDR_MCS{mcs}_Numerology{numerology}.pdf', format='pdf')
        plt.show()

        # Plot PIR (Packet Inter-Reception Rate)
        plt.figure()
        for protocol in unique_protocols:
            # Filter simulation data for PIR
            metric_data = metric_df[
                (metric_df['protocol_type'] == protocol) &
                (metric_df['MCS'] == mcs) &
                (metric_df['numerology'] == numerology)
            ]

            # Plot simulation data if available
            if not metric_data.empty:
                plt.plot(
                    metric_data['distance_bin'],
                    metric_data['cumulative_PIR'],
                    label=f'{protocol}',
                    linestyle='-', marker='x'
                )

        # Customize PIR plot
        plt.ylim(0.1, 0.18)
        plt.xlabel('Distance (m)')
        plt.ylabel('PIR (s)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save PIR plot
        plt.savefig(f'{output_folder}/PIR_MCS{mcs}_Numerology{numerology}.pdf', format='pdf')
        plt.show()
