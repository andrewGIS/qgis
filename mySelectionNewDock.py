# -*- coding: utf-8 -*-
"""
/***************************************************************************
 mySelectionNewDock
                                 A QGIS plugin
 mySelectionNewDock
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-11-03
        git sha              : $Format:%H$
        copyright            : (C) 2021 by andrew tarasov
        email                : some@mail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from typing import List

from PyQt5.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
# Initialize Qt resources from file resources.py
from .mapTools.squareTool import SquareMapTool
from .mapTools.firstTool import circleDrawerMapTool
from qgis.core import QgsProject, QgsGeometry, QgsLayerTreeGroup, QgsCoordinateReferenceSystem, QgsLayerTreeLayer, QgsEditFormConfig


# Import the code for the DockWidget
from .mySelectionNewDock_dockwidget import mySelectionNewDockDockWidget
import os.path

from .lib.layers_utils import LayerInfo, create_layer_from_gpkg, create_node, set_node_visibility, set_style
from .lib.checker import Checker
from .lib.export import simple_export, simple_export_with_layout, export_with_predefined_layout


class mySelectionNewDock:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'mySelectionNewDock_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&mySelectionNewDock')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'mySelectionNewDock')
        self.toolbar.setObjectName(u'mySelectionNewDock')

        #print "** INITIALIZING mySelectionNewDock"

        self.pluginIsActive = False
        self.dockwidget = None
        self.layers = []
        self.selectedLayer = None
        self.mapTool = circleDrawerMapTool(iface.mapCanvas())
        self.rectangleDrawTool = SquareMapTool(iface.mapCanvas())


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('mySelectionNewDock', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/mySelectionNewDock/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'selectionWidget'),
            callback=self.run,
            parent=self.iface.mainWindow())

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        print ("** CLOSING mySelectionNewDock")

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        self.dockwidget = None
        self.selectedLayer = None
        self.layers = []
        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        print("** UNLOAD mySelectionNewDock")

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&mySelectionNewDock'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    #--------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            print ("** STARTING mySelectionNewDock")


            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = mySelectionNewDockDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.TopDockWidgetArea, self.dockwidget)
            self.layers = [lyr.name() for lyr in QgsProject.instance().mapLayers().values()]

            #self.selectedLayer = QgsProject.instance().mapLayersByName(self.layers[0])[0]  # устанавливаем при запуске

            # добавление с ключом
            # for id, layer in QgsProject.instance().mapLayers().items():
            #     self.dockwidget.comboBox.addItem(layer.name(), userData=id)
            #     self.dockwidget.comboBox.addItem((layer.name(), id))

            self.dockwidget.comboBox.addItems(self.layers)
            self.dockwidget.comboBox.currentIndexChanged.connect(self.onLayerChange)
            self.dockwidget.pushButton.clicked.connect(self.makeQuery)
            self.dockwidget.loadProject.clicked.connect(self.loadProject)
            self.dockwidget.drawPolygon.clicked.connect(self.rectangle_draw)
            self.dockwidget.checkParcel.clicked.connect(self.polygon_checker)
            self.dockwidget.simpleExport.clicked.connect(self.simple_print)
            self.dockwidget.show()

    def onLayerChange(self, index):

        # print(index)

        # Доступ по имени
        print(self.layers[index])
        # print(index)
        selectedLayerName = self.layers[index]
        self.selectedLayer = QgsProject.instance().mapLayersByName(selectedLayerName)[0]  # возвращает список

    def makeQuery(self):

        # Запрос
        print('Do query')

        # sF = []
        # sFeatures = self.selectedLayer.selectedFeatures()
        # if len(sFeatures) == 0:
        #     return
        # for f in sFeatures:
        #     sF.append(f.id())
        #
        # exp = ",".join([str(i) for i in sF])
        # print (f"fid in ({exp})")
        # self.selectedLayer.setSubsetString(f"fid in ({exp})")

        # Инструмент
        # set my cutom tool to qgis
        if not self.mapTool.isActive():
            self.iface.mapCanvas().setMapTool(self.mapTool)
        else:
            self.mapTool.clearRubberBand()
            self.iface.mapCanvas().unsetMapTool(self.mapTool)

    def loadProject(self):

        curFolder = os.path.dirname(os.path.abspath(__file__))
        base_map_GPKG = os.path.join(curFolder, "data", "basemap.gpkg")
        stylePath = os.path.join(curFolder, "style")
        crs = QgsCoordinateReferenceSystem("EPSG:32640")

        # Список слоев для проекта.
        # источник (GeoPackage), слой в источнике, имя в проекте, стиль, видимость слоя, имя группы
        layers_info: List[LayerInfo] = [
            LayerInfo(base_map_GPKG, "boundary", "Граница МО", "boundary.qml", True),
            LayerInfo(base_map_GPKG, "pk_boundary", "Граница ПК", "pk_boundary.qml", False),
        ]

        QgsProject.instance().setCrs(crs)

        for idx, layer in enumerate(layers_info):
            layerToAdd = create_layer_from_gpkg(base_map_GPKG, layer.src_layer, layer.node_name, crs)
            set_style(layerToAdd, layer.style, stylePath)
            QgsProject().instance().addMapLayer(layerToAdd, False)
            node: QgsLayerTreeLayer = QgsLayerTreeLayer(layerToAdd)
            set_node_visibility(node, layer.visible_in_project)

            if layer.src_layer == "boundary":
                formConfig: QgsEditFormConfig = layerToAdd.editFormConfig()
                formPath = os.path.join(curFolder, "editForms", "boundary.ui")
                formConfig.setUiForm(formPath)

                formConfig.setInitCodeSource(QgsEditFormConfig.CodeSourceFile)
                formConfig.setInitFilePath(os.path.join(curFolder, "editForms", "boundary.py"))
                formConfig.setInitFunction("open")
                layerToAdd.setEditFormConfig(formConfig)


            QgsProject().instance().layerTreeRoot().insertChildNode(idx, node)

    def rectangle_draw(self):
        # Инструмент
        # set my custom tool to qgis
        if not self.rectangleDrawTool.isActive():
            self.iface.mapCanvas().setMapTool(self.rectangleDrawTool)
        else:
            self.rectangleDrawTool.clearRubberBand()
            self.iface.mapCanvas().unsetMapTool(self.rectangleDrawTool)

    def polygon_checker(self):
        checker = Checker()
        if self.rectangleDrawTool.geometry:
            checker.check_geometry(self.rectangleDrawTool.geometry)
            QMessageBox.information(self.iface.mainWindow(), "Сообщение",
                                 u"Участок проверен")
        else:
            QMessageBox.critical(self.iface.mainWindow(), "Сообщение",
                                 u"Не установлена геометрия")

    def simple_print(self):
        # simple_export(self.iface.activeLayer())
        # simple_export_with_layout(self.iface)
        export_with_predefined_layout(self.iface)



