import os
from typing import Union

from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QFileDialog

from PyQt5.QtXml import QDomDocument

from qgis.core import (
    QgsMapSettings,
    QgsProject,
    QgsMapRendererParallelJob,
    # Примеры классов для добавления в компоновку
    QgsLayoutItemLabel,
    QgsLayoutItemLegend,
    QgsLayoutItemMap,
    QgsLayoutItemPolygon,
    QgsLayoutItemScaleBar,
    QgsLayoutExporter,
    QgsLayoutItem,
    QgsLayoutPoint,
    QgsLayoutSize,
    #############
    QgsUnitTypes,
    QgsPrintLayout,
    QgsRectangle,
    QgsLayerTree,
    QgsReadWriteContext
)

from qgis.PyQt.QtCore import (
    QSize,
)


def simple_export(template_layer):
    fld = ask_for_folder()
    image_location = os.path.join(fld, "render.png")

    settings = QgsMapSettings()
    settings.setLayers([template_layer])
    settings.setBackgroundColor(QColor(255, 255, 255))
    settings.setOutputSize(QSize(800, 600))
    settings.setExtent(template_layer.extent())

    # settings.setDestinationCrs(layers[0].crs()) # Если рендер нескольких слое в разных CRS

    render = QgsMapRendererParallelJob(settings)

    def finished():
        img = render.renderedImage()
        img.save(image_location, "png")

    render.finished.connect(finished)
    render.start()


def ask_for_folder(init_folder: str = "/") -> Union[str, None]:
    """
    Спрашивает папку у пользователя. Если пользователь не выбрал папку возвращает None

    :return: Выбранную папку, если она была выбрана. None если ничего не было выбрано

    """
    out_path: str = QFileDialog.getExistingDirectory(None, 'Выходная папка', init_folder, QFileDialog.ShowDirsOnly)
    return out_path if out_path else QgsProject.instance().homePath()


def simple_export_with_layout(iface):
    project = QgsProject.instance()
    layoutName = "MyLayout"

    layouts_list = project.layoutManager().printLayouts()
    for layout in layouts_list:
        if layout.name() == layoutName:
            project.layoutManager().removeLayout(layout)

    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(layoutName)
    project.layoutManager().addLayout(layout)

    # КАРТА

    myMap = QgsLayoutItemMap(layout)

    myMap.setRect(20, 20, 20, 20)  # надо задать обязательно для отрисовки
    # (т.к. наследуется от PyQt5.QtWidgets.QGraphicsRectItem)
    ms = QgsMapSettings()
    ms.setLayers([iface.activeLayer()])  # set layers to be mapped
    rect = QgsRectangle(iface.mapCanvas().extent())

    # Можно и к выбранной фиче приблизить
    # rect = QgsRectangle(list(iface.activeLayer().selectedFeatures())[0].geometry().boundingBox())
    # myMap.setExtent(rect.buffered(30000))  # можем увеличить чтобы объект точно влез

    ms.setExtent(rect)
    myMap.setExtent(rect)

    # Размер и позиция элемента карты(по умолчанию ширина -0  высота - 0, позиция в 0,0)
    myMap.attemptMove(QgsLayoutPoint(5, 5, QgsUnitTypes.LayoutMillimeters))
    myMap.attemptResize(QgsLayoutSize(200, 200, QgsUnitTypes.LayoutMillimeters))

    layout.addLayoutItem(myMap)
    layout.refresh()

    base_path = ask_for_folder()
    pdf_path = os.path.join(base_path, "output.pdf")

    # ЛЕГЕНДА
    legend = QgsLayoutItemLegend(layout)
    legend.setTitle("Условные обозначения")
    layerTree = QgsLayerTree()
    layerTree.addLayer(iface.activeLayer())
    legend.model().setRootGroup(layerTree)
    layout.addLayoutItem(legend)
    legend.attemptMove(QgsLayoutPoint(230, 15, QgsUnitTypes.LayoutMillimeters))
    # legend.setLinkedMap(myMap) для связи с элементом карты

    # ЗАГОЛОВОК
    title = QgsLayoutItemLabel(layout)
    title.setText("Заголовок карты")
    title.setFont(QFont('Arial', 24))
    title.adjustSizeToText()
    layout.addLayoutItem(title)
    title.attemptMove(QgsLayoutPoint(10, 5, QgsUnitTypes.LayoutMillimeters))

    # ЛЮБОЙ ДРУГОЙ ТЕКСТ
    label = QgsLayoutItemLabel(layout)
    label.setText(iface.activeLayer().name())
    label.adjustSizeToText()
    layout.addLayoutItem(label)

    # ТАБЛИЦА АТРИБУТОВ, МАСШТАБ и т.д.

    exporter = QgsLayoutExporter(layout)
    exporter.exportToPdf(pdf_path, QgsLayoutExporter.PdfExportSettings())


# ЗАГРУЗКА С КОМПОНОВКОЙ

def export_with_predefined_layout(iface):
    project = QgsProject.instance()
    templatePath = r"C:\Users\ANDREWCOMP\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\myselectionnewdock\lib\templates\template.qpt"

    layouts_list = project.layoutManager().printLayouts()
    for layout in layouts_list:
        if layout.name() == "test name":
            project.layoutManager().removeLayout(layout)

    template_file = open(templatePath)
    # если есть русские символы смотрим в какой кодировке сохранен
    # template_file = open(templatePath, encoding='utf-8')
    template_content = template_file.read()
    template_file.close()

    manager = QgsProject.instance().layoutManager()
    layout = QgsPrintLayout(QgsProject.instance())
    layout.setName("test name")
    layout.initializeDefaults()
    manager.addLayout(layout)

    document = QDomDocument()
    document.setContent(template_content)
    items, ok = layout.loadFromTemplate(document, QgsReadWriteContext(), False)

    # можем изменять дополнительно
    title = QgsLayoutItemLabel(layout)
    title.setText("Экстра подписи для компоновки")
    title.setFont(QFont('Arial', 24))
    title.adjustSizeToText()
    layout.addLayoutItem(title)
    title.attemptMove(QgsLayoutPoint(10, 15, QgsUnitTypes.LayoutMillimeters))

    iface.openLayoutDesigner(layout)


# можно например менять шаблоны в файлике
def replacer(templatePath, templateFilePath):
    # открываем файл на чтение
    file = open(templatePath, "rt")
    # читаем входной файл
    data = file.read()
    # заменяем нужные подстроки
    data = data.replace("SOME_PATTERN", "SOME_VALUE")
    # закрываем файл
    file.close()
    # открываем файл на запись
    file = open(templateFilePath, "wt")
    # перезаписываем входной файл
    file.write(data)
    # закрываем файл
    file.close()






