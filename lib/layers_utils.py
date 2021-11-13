import os
from typing import Union

from qgis.core import (
    QgsLayerTreeLayer,
    QgsLayerTreeGroup,
    QgsProject,
    QgsVectorLayer,
    QgsLayerTree,
)


class LayerInfo(object):
    def __init__(self, src, src_layer, node_name, style, visible_in_project):
        self.src: str = src
        self.src_layer: str = src_layer
        self.node_name: str = node_name
        self.style: str = style
        self.visible_in_project: bool = visible_in_project


def create_layer_from_gpkg(path_To_GPKG: str, GPKG_layer: str, layer_name: str, crs) -> QgsVectorLayer:
    """
    Создает слой QgsVectorLayer из указанного GeoPackage и и именнованного слоя. Для нового слоя будет
    присвоено имя указанное в параметре. Если слой не получилось создать, возникнет необработанная ошибка

    :param path_To_GPKG: Путь до GeoPackage

    :param GPKG_layer: Слой в GeoPackage на основе которого будет создаваться QgsVectorLayer

    :param layer_name: Имя для созданного слоя QgsVectorLayer

    :return:
    """
    layer_source: str = f"{path_To_GPKG}|layername={GPKG_layer}"
    qgs_layer: QgsVectorLayer = QgsVectorLayer(layer_source, layer_name, "ogr")
    qgs_layer.setCrs(crs)
    if not qgs_layer.isValid():
        print("Layer failed to load!")
        raise Exception(f"Invalid layer {layer_name} ,dataSource - {path_To_GPKG},  layerName - {GPKG_layer}")
    else:
        return qgs_layer


def set_node_visibility(layer_node: QgsVectorLayer, visible: bool):
    """
    Устанавливает видимость для слоя

    :param layer_node: Слой в проекте QGIS

    :param visible: Параметр видимости слоя

    :return: None

    """

    layer_node.setItemVisibilityChecked(visible)


def set_style(layer: QgsLayerTreeLayer, style: str, stylePath: str):
    """
    Устанавливает стиль

    :param layer: Слой в проекте QGIS

    :param style: Применяемый стиль

    :return: None

    """

    layer.loadNamedStyle(
        os.path.join(stylePath, style),
        True
    )
    layer.triggerRepaint()


def create_node(in_src, in_layer, node_name, style, visibility, crs) -> QgsLayerTreeLayer:
    """
    Создает слой для добавления в проект, а также устанавливает видимость, стиль

    :param in_src: Путь до GeoPackage

    :param in_layer: Слой в GeoPackage, на основе которого будет создан слой

    :param node_name: Имя, которое будет в проекте

    :param style: Стиль, которой будет примененем для слоя

    :param visibility: Видимость слоя в проекте

    :return: Созданный слой для добавления в проект
    """

    layer: QgsVectorLayer = create_layer_from_gpkg(in_src, in_layer, node_name, crs)
    QgsProject().instance().addMapLayer(layer, False)
    #set_style(layer, style, stylePath)
    node: QgsLayerTreeLayer = QgsLayerTreeLayer(layer)
    #set_node_visibility(node, visibility)
    return node
