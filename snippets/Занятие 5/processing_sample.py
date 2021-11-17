from processing import Processing
from qgis._core import QgsVectorLayer
from qgis.core import (QgsProcessingContext,QgsProcessingFeedback,
QgsProcessingAlgorithm, QgsProject
)

Processing.initialize()
context: QgsProcessingContext = QgsProcessingContext()
context.setProject(QgsProject.instance())
algorithm_register = QgsApplication.processingRegistry()
feedback: QgsProcessingFeedback = QgsProcessingFeedback()

BUFFER = algorithm_register.algorithmById(u'qgis:buffer')

params = {
    'DISSOLVE' : False,
    'DISTANCE' : 1000,
    'END_CAP_STYLE' : 0,
    'INPUT' : 'C:\\Users\\ANDREWCOMP\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\myselectionnewdock\\data\\basemap.gpkg|layername=pk_boundary',
    'JOIN_STYLE' : 0,
    'MITER_LIMIT' : 2,
    'OUTPUT' :
    'TEMPORARY_OUTPUT',
    'SEGMENTS' : 5
}

BUFFER.prepare(params, context, feedback)
tool_result = BUFFER.runPrepared(params, context, feedback)

toolResult = context.takeResultLayer(tool_result[u'OUTPUT'])

QgsProject.instance().addMapLayer(toolResult)

for f in toolResult.getFeatures():
    print (f.geometry().area())