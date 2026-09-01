# Ripple effects of prizewinning across knowledge space and collaboration networks

This repository contains the replication code for the study **"Ripple effects of prizewinning across knowledge space and collaboration networks."**

## Overview

Scientific prizes recognize individual achievement, but their influence may extend beyond the recipients themselves. This study examines how prizewinning reshapes scientific attention across collaboration networks. We find that the increase in attention following an award extends to collaborators’ independent work and propagates through both knowledge and collaboration networks, with effects diminishing as distance from the prizewinner increases.

This repository provides the code and data required to reproduce the main analyses, tables, and figures in the study.

## Repository Structure

```text
Ripple effects of prizewinning across knowledge space and collaboration networks/
├── Matching_algorithm.py
├── Figure 1.ipynb
├── Figure 2.ipynb
├── Figure 3.ipynb
├── Figure 4.ipynb
├── Figure 5.ipynb
├── Figure 6.ipynb
├── Table 1_2.R
└── README.md
```

### Main files

-   **`Matching_algorithm.py`** --- Implements the matching procedure
    used to construct the comparison sample.
-   **`Figure 1.ipynb`** --- Reproduces Figure 1.
-   **`Figure 2.ipynb`** --- Reproduces Figure 2.
-   **`Figure 3.ipynb`** --- Reproduces Figure 3.
-   **`Figure 4.ipynb`** --- Reproduces Figure 4.
-   **`Figure 5.ipynb`** --- Reproduces Figure 5.
-   **`Figure 6.ipynb`** --- Reproduces Figure 6.
-   **`Table 1_2.R`** --- Reproduces the results reported in Tables 1
    and 2.

## Data

The replication data are stored separately on **Google Drive** because some data files exceed GitHub's file-size limit.

**Data repository:**  
[Google Drive](https://drive.google.com/drive/folders/1_RNRytilj0fV1a2YV3dPe9zD1XQ8o7P0?usp=sharing)

Download the replication data and place them in a local `Data/` directory before running the replication code.


## Software Requirements

The analysis was conducted using **Python 3.11** and **R**.

### Python

Install the main Python packages using:

``` bash
pip install pandas numpy scipy matplotlib seaborn jupyter
```

### R

An installation of R is required to reproduce Tables 1 and 2. RStudio
may be used as the development environment but is not required.
Additional R packages required for replication are loaded within
`Table 1_2.R`.

## Reproduction Instructions

### 1. Download the code

Clone or download this GitHub repository.

### 2. Download the replication data

Download the replication dataset from Zenodo

Extract the archive and place the data files in the `Data/` directory.

### 3. Construct the matched sample

Run:

``` bash
python Matching_algorithm.py
```

The matching procedure constructs the matched treatment and comparison
samples used in the subsequent analyses.

### 4. Reproduce the figures

Open the following Jupyter notebooks and execute all cells sequentially:

``` text
Figure 1.ipynb
Figure 2.ipynb
Figure 3.ipynb
Figure 4.ipynb
Figure 5.ipynb
Figure 6.ipynb
```

Each notebook contains the analysis required to reproduce the
corresponding figure in the paper.

### 5. Reproduce Tables 1 and 2

Open and run:

``` text
Table 1_2.R
```

in R or RStudio.

## Reproducibility Notes

-   Run the notebooks from top to bottom because later cells may depend
    on objects generated in earlier cells.
-   File paths may need to be adjusted depending on the local directory
    structure.
-   Numerical results may differ slightly across software or package
    versions because of differences in numerical precision.
-   Large replication datasets are stored separately from the GitHub
    repository.
