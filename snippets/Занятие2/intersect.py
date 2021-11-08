layer1 = QgsProject.instance().mapLayersByName('RUS_adm2')[0]
layer2 = QgsProject.instance().mapLayersByName('RUS_adm1')[0]

#for f in layer2.dataProvider().getFeatures():
for f in layer2.selectedFeatures():
    r = QgsFeatureRequest().setFilterRect(f.geometry().boundingBox())
    for f1 in layer1.dataProvider().getFeatures(r):
        # вычисляем площадь пересечения
        relation = (f1.geometry().intersection(f.geometry()).area())/(f1.geometry().area())
        if relation > 0.97:
            print ("Yes", f1['NAME_1'])
            # обновляем фичу по id, где передаем 
            # {айдифичи:{индекс поля: значение}}
            fid = f1.id()
            layer1.dataProvider().changeAttributeValues({fid:{15:"1"}})
        else:
            print ("No", f1['NAME_1'])
        