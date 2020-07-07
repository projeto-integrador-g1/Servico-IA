import fiona
import rasterio
import rasterio.mask
import json
import matplotlib.pyplot as plt

geoms = [{
    "type": "FeatureCollection",
    "crs": {
        "type": "name",
        "properties": {
            "name": "EPSG:32622"
        }
    },
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    (
                        -50.48751719782649,
                        -16.404813405303997
                    ),
                    (
                        -50.467370502876435,
                        -16.423333779750436
                    ),
                    (
                        -50.50027677129552,
                        -16.440081120831323
                    ),
                    (
                        -50.520407933302636,
                        -16.417352893554707
                    ),
                    (
                        -50.48751719782649,
                        -16.404813405303997
                    )
                ]]
            }
        }
    ]
}]

with fiona.open("A:\Bruno\Documents\Faculdade\Projeto-Intergador\Servico-IA\layers\POLYGON.shp", "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

with rasterio.open("A:\Bruno\Documents\Faculdade\Projeto-Intergador\Servico-IA\LC08_L1TP_222071_20180429_20180502_01_T1_B2.tif", "r") as src:
    out_image, out_transform = rasterio.mask.mask(
        src, shapes)
    out_meta = src.meta

out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open("RGB.byte.masked.tif", "w", **out_meta) as dest:
    dest.write(out_image)
    
    
var = rasterio.open("RGB.byte.masked.tif")
plt.imshow(var.read(1))
plt.show()