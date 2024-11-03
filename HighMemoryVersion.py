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
