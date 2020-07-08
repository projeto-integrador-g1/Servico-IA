#import fiona
import rasterio
import rasterio.mask
import json
import matplotlib.pyplot as plt
from rasterio.warp import calculate_default_transform, reproject, Resampling

def cropImg(coord):
    geoms = [{
                "type": "Polygon",
                "coordinates": [
                    [[-40.98167561648731, -9.235799733189367], [-40.94014730150366, -9.235501262559865], [-40.94004650462216, -9.263357430947423], [-40.98288517905988, -9.26395432469262], [-40.98167561648731, -9.235799733189367]]
                    ]
    }]

    with rasterio.open(r"C:\Users\mathe\Servico-IA\reprojected.tif") as src:
        out_image, out_transform = rasterio.mask.mask(
            src, geoms, crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})

    with rasterio.open("cropped.tif", "w", **out_meta) as dest:
        dest.write(out_image)
    
    




def reprojectA(id):
    dst_crs = 'EPSG:4326'
    with rasterio.open('C:/Users/mathe/Servico-IA/'+ id +'.tif') as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })
        with rasterio.open('reprojected.tif', 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)


