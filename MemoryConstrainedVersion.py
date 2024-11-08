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
