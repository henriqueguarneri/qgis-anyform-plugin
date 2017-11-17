from PyQt4.QtCore import QVariant
layer = QgsVectorLayer("point?crs=epsg:32722", 'basegrid', "memory")
res = layer.dataProvider().addAttributes([QgsField("S", QVariant.Double)])
layer.startEditing()
feature = QgsFeature()
feature.setGeometry( QgsGeometry.fromPoint(QgsPoint(685027.315920436,9449844.93627268) )
feature.setAttributes([100] )
layer.dataProvider().addFeatures([feature])
layer.commitChanges()
#layer.updateExtents()
QgsMapLayerRegistry.instance().addMapLayer(layer)