from datetime import datetime
from typing import Union

from osgeo import ogr
from qgis.core import QgsVectorFileWriter, QgsVectorLayer
import os

from PyQt5.QtWidgets import QMessageBox as msg

def write_layer_to_gpkg(out_GPKG: str, in_layer: QgsVectorLayer, out_name: str) -> Union[str,None]:
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
    options.layerName = out_name.replace(' ', "_")
    error, error_string = QgsVectorFileWriter.writeAsVectorFormat(in_layer, out_GPKG, options)
    if error != QgsVectorFileWriter.NoError:
        return f'Error has happened: {error_string}'
    else:
        return None


def create_gpkg(in_folder: str, name_GPKG: str) -> Union[str, None]:
    out_GPKG = os.path.normpath(os.path.join(in_folder, f"{name_GPKG}.gpkg"))

    #name: str = f"export_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"

    if os.path.exists(out_GPKG):
        answer = msg.information(
            None,
            "Внимание",
            f'GeoPackage с именем {name_GPKG} уже существует в папке {in_folder}.' +
            '\nПерезаписать?',
            msg.StandardButtons(msg.Yes | msg.No)
        )
        if answer == msg.No:
            return

    dr: ogr.Driver = ogr.GetDriverByName("GPKG")
    ds: ogr.DataSource = dr.CreateDataSource(out_GPKG)
    if not os.path.exists(out_GPKG):
        del dr
        del ds
        return None

    del dr
    del ds
    return out_GPKG
