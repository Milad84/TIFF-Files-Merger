# TIFF-Files-Merger
![image](https://github.com/user-attachments/assets/7644c0f5-1f9a-48cf-affd-f22c533f8578)

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
```
## Configure the PROJ Path

Set the PROJ_LIB environment variable to avoid errors related to the PROJ database. Update the path in the script to match your system's configuration. To find the path to PROJ you can try the following as a standalone script:

```bash
import pyproj
print(pyproj.datadir.get_data_dir())
```
Which will give you the path required for the following scripts and specifically where the path to PROJ is 

```bash

set: os.environ['PROJ_LIB'] = r"C:\Python310\lib\site-packages\pyproj\proj_dir\share\proj"
```

 Replace the path with the one you get in the output of the above code.

## Usage
## Option 1: Memory-Constrained Version
Use MemoryConstrainedVersion.py if you are working on a system with limited memory. It resamples the TIFF files to a lower resolution and processes them in smaller chunks to reduce memory usage.

```bash
import os
import glob
import rasterio
from rasterio.enums import Resampling
import numpy as np

os.environ['PROJ_LIB'] = r"C:\Python310\lib\site-packages\pyproj\proj_dir\share\proj"

def ensure_output_directory(output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

def resample_tiff(input_file, output_file, scale_factor=0.5):
    with rasterio.open(input_file) as dataset:
        new_width = int(dataset.width * scale_factor)
        new_height = int(dataset.height * scale_factor)
        data = dataset.read(
            out_shape=(dataset.count, new_height, new_width),
            resampling=Resampling.bilinear
        )
        transform = dataset.transform * dataset.transform.scale(
            (dataset.width / new_width), (dataset.height / new_height)
        )
        metadata = dataset.meta.copy()
        metadata.update({
            "height": new_height,
            "width": new_width,
            "transform": transform
        })
        with rasterio.open(output_file, "w", **metadata) as dest:
            dest.write(data)

def merge_in_chunks(tiff_files, output_file, chunk_height=5000):
    with rasterio.open(tiff_files[0]) as src:
        meta = src.meta.copy()
        total_width = src.width
        total_height = src.height
        transform = src.transform

    meta.update({
        "driver": "GTiff",
        "height": total_height,
        "width": total_width,
        "transform": transform
    })

    with rasterio.open(output_file, "w", **meta) as dest:
        for start_row in range(0, total_height, chunk_height):
            end_row = min(start_row + chunk_height, total_height)
            rows_to_read = end_row - start_row
            accumulated_data = np.zeros((meta['count'], rows_to_read, total_width), dtype=meta['dtype'])
            for file in tiff_files:
                with rasterio.open(file) as src:
                    data = src.read(window=((start_row, end_row), (0, total_width)))
                    accumulated_data += data
            dest.write(accumulated_data, window=((start_row, end_row), (0, total_width)))

tiff_directory = "E:\\Data\\canopy cover-20241103T154241Z-001\\canopy cover"
resampled_directory = "E:\\Data\\resampled_canopy_cover"
output_directory = "E:\\output"

ensure_output_directory(resampled_directory)

tiff_files = glob.glob(f"{tiff_directory}/*.tif")
for tiff_file in tiff_files:
    filename = os.path.basename(tiff_file)
    resample_tiff(tiff_file, os.path.join(resampled_directory, filename))

final_output_path = os.path.join(output_directory, "final_mosaic.tif")
merge_in_chunks(glob.glob(f"{resampled_directory}/*.tif"), final_output_path)

print(f"Final mosaic created successfully in {output_directory}!")
```
## Option 2: High-Memory Version
Use HighMemoryVersion.py if you have a high-memory system or supercomputer. It merges all TIFF files at once without resampling.

```bash
import os
import glob
import rasterio
from rasterio.merge import merge

os.environ['PROJ_LIB'] = r"C:\Python310\lib\site-packages\pyproj\proj_dir\share\proj"

def ensure_output_directory(output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

def merge_all_tiffs(tiff_files, output_file):
    src_files_to_mosaic = [rasterio.open(file) for file in tiff_files]
    mosaic, out_trans = merge(src_files_to_mosaic)
    out_meta = src_files_to_mosaic[0].meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans
    })
    with rasterio.open(output_file, "w", **out_meta) as dest:
        dest.write(mosaic)
    for src in src_files_to_mosaic:
        src.close()

tiff_directory = "E:\\Data\\canopy cover-20241103T154241Z-001\\canopy cover"
output_directory = "E:\\output"

ensure_output_directory(output_directory)

tiff_files = glob.glob(f"{tiff_directory}/*.tif")
final_output_path = os.path.join(output_directory, "final_mosaic.tif")

merge_all_tiffs(tiff_files, final_output_path)

print(f"Final mosaic created successfully in {output_directory}!")
```
## Explanation
Memory-Constrained Version: Resamples and merges TIFF files in smaller chunks to reduce memory usage.
High-Memory Version: Directly merges all TIFF files in one step, optimized for systems with ample memory.
## Visualization
Use QGIS or other GIS platforms to visualize the final mosaic. You can add basemaps in QGIS using the QuickMapServices plugin for context.

## Adding a Basemap in QGIS
Install the QuickMapServices plugin from the Plugins menu.
Use it to add basemaps like Google Satellite or OpenStreetMap.
