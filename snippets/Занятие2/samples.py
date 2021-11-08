#for f in iface.activeLayer().selectedFeatures():
#    print (f.geometry().area())


#for f in iface.activeLayer().selectedFeatures():
#    #print(f.attributes())
#    print(f['NAME_1'])

# Пример получения данных с DataProvider
#exp = QgsExpression(''' "NAME_1" = 'Karelia' ''')
#request = QgsFeatureRequest(exp)
#request.setSubsetOfAttributes([])
#    
#for row in iface.activeLayer().dataProvider().getFeatures(request):
#    print(row.geometry().area())

# Пример получения данных без геометрии
#request = QgsFeatureRequest()
#request.setSubsetOfAttributes(['ID_1'],iface.activeLayer().fields())
#request.setFlags(QgsFeatureRequest.NoGeometry)
#for row in iface.activeLayer().dataProvider().getFeatures(request):
#    print(row.attributes()) 
#    # print(row['ID_1']) 

# Пример получения данных с пространстенным фильтром
#request = QgsFeatureRequest()
#request.setFilterRect(QgsRectangle(40,45,50,55))
#for row in iface.activeLayer().dataProvider().getFeatures(request):
#    print(f"{row.id()},")

#базовое взаимодействие
#QMessageBox.warning(
#    iface.mainWindow(), "",
#    "Error"
#)

