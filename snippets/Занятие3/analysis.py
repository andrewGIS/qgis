layer = iface.activeLayer()

buildings = QgsProject.instance().mapLayersByName('temp1')[0]

for f in layer.getFeatures():
    buffer = f.geometry().buffer(1000,50)
#   c преобразованием
#    sourceCrs = QgsCoordinateReferenceSystem("EPSG:4326")
#    destCrs = QgsCoordinateReferenceSystem("EPSG:32640")
#    tr = QgsCoordinateTransform(sourceCrs, destCrs, QgsProject.instance())
#    надо геометрию копировать
#    bufferCopy = buffer.fromWkt(f.geometry().asWkt())
#    bufferCopy.transform(tr)
    
    request = QgsFeatureRequest()
    request.setFilterRect(buffer.boundingBox())
    count = []
    for f1 in buildings.dataProvider().getFeatures(request):
        if buffer.contains(f1.geometry()):
            count.append(f1.id())
    print (len(count))