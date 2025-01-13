# README for SPC6G Simulation and Analysis

## Overview

This project is based on the research paper titled **"SPC6G: Towards Efficient Resource Allocation in 6GV2X Networks: A Smart Predictive Collision Framework"**. The project provides analytical and simulation-based tools to evaluate the performance of the SPC6G and NRV2X protocols using Packet Reception Ratio (PRR) and Packet Inter-Reception Rate (PIR) metrics. The analysis spans urban and highway scenarios.

## Structure

### 1. **Key Files**

- **`calculations.py`**: Core functions to calculate analytical and simulation-based metrics such as PRR, PIR, overlap probability, and resource utilization.
- **`analytical_prr_pir.py`**: Contains methods for computing PRR and PIR analytically across various distances and configurations.
- **`visualization_analtical_simulations.py`**: Visualizes the comparison between analytical and simulation results for metrics like PRR and PIR.
- **`visualization_simulations_highway.py`**: Plots PRR and PIR for highway simulation scenarios.
- **`visualization_simulations_urban.py`**: Plots PRR and PIR for urban simulation scenarios.

### 2. **Datasets**

- **`analytical_simulation_metrics.csv`**: Stores analytical PRR and PIR results.
- **`sim_metrics_data.csv`**: Simulated data for general scenarios.
- **`sim_metrics_data_highway.csv`**: Simulated data for highway scenarios.
- **`sim_metrics_data_urban.csv`**: Simulated data for urban scenarios.

### 3. **Notebooks**

- **`main.ipynb`**: A Jupyter notebook for integrating and running analytical calculations and visualizations interactively.



## Usage

### Run Analytical Models

Run the main file


### Generate Visualizations

#### Analytical and Simulation Comparison

```bash
$ python visualization_analtical_simulations.py
```

#### Highway Scenario Simulations

```bash
$ python visualization_simulations_highway.py
```

#### Urban Scenario Simulations
```bash
$ python visualization_simulations_urban.py
```
---

## Outputs

1. **Plots**

   - Saved in `SPS6G_plots` or `SPS6G_plots_sim_highway` or `SPS6G_plots_sim_urban` folders.
   - Includes PRR vs Distance and PIR vs Distance graphs.

2. **CSV Files**

   - Analytical results are saved in `analytical_simulation_metrics.csv`.

---

## Citation

If you use this project or its findings in your research, please cite the paper:

**Towards Efficient Resource Allocation in 6GV2X Networks: A Smart Predictive Collision Framework**\
*Authors: [Mahmoud Elsharief, Saifur Rahman Sabuj, and Han-Shin Jo]*\


---

## Contributions

This project benefits from contributions made by developers and tools, including ChatGPT, to assist in creating templates. Feel free to contribute improvements, additional scenarios, or new metrics. Submit issues or pull requests via GitHub.

---


