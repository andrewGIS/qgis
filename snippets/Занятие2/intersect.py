layer1 = QgsProject.instance().mapLayersByName('RUS_adm1')[0]
layer2 = QgsProject.instance().mapLayersByName('RUS_adm2')[0]

for f in layer2.selectedFeatures():
    request = QgsFeatureRequest()
    request.setFilterRect(f.geometry().boundingBox())
    for f1 in layer1.dataProvider().getFeatures(request):
        intersection = f.geometry().intersection(f1.geometry())
        relation = intersection.area() / f.geometry().area()
        print(f1['NAME_1'])
        if relation > 0.95:
            print(relation, f1['NAME_1'])
            fid = f.id()
            attrs = {'REMARKS': f1.id()}
            layer1.changeAttributeValues({fid: attrs})
