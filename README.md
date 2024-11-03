# TIFF-Files-Merger

# Canopy Cover Mosaic Project

This project provides Python scripts for merging large sets of geospatial TIFF files into a single mosaic using the `rasterio` library. There are two versions of the script: one for systems with limited memory (using resampling and chunking) and another optimized for high-memory systems.

## Table of Contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
  - [Option 1: Memory-Constrained Version](#option-1-memory-constrained-version)
  - [Option 2: High-Memory Version](#option-2-high-memory-version)
- [Explanation](#explanation)
- [Visualization](#visualization)
- [Contributing](#contributing)
- [License](#license)

## Introduction
The Canopy Cover Mosaic Project is designed to handle and process large sets of TIFF files representing geospatial data, such as canopy cover. The scripts can be adjusted based on the available system resources.

## Prerequisites
- **Python 3.6 or higher**
- **Dependencies**: `rasterio`, `numpy`
- **Hardware**: A high-memory computer or a supercomputer is recommended for the high-memory version.

## Setup and Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/username/canopy-cover-mosaic.git
   cd canopy-cover-mosaic
## Install Dependencies
```bash
pip install rasterio numpy

## Configure the PROJ Path

Set the PROJ_LIB environment variable to avoid errors related to the PROJ database. Update the path in the script to match your system's configuration.

## Usage
## Option 1: Memory-Constrained Version
Use MemoryConstrainedVersion.py if you are working on a system with limited memory. It resamples the TIFF files to a lower resolution and processes them in smaller chunks to reduce memory usage.
