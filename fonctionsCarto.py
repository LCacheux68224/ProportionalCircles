# -*- coding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import  QVariant
from qgis.core import *
import math

def setTypoColor(layer) : 
    fields = layer.pendingFields().toList()
    idx = len(fields)-1
    values = layer.uniqueValues(idx)
    values.sort() 
    AccentColorList = ( '#7fc97f','#ffff99' ,  '#fdc086',  '#beaed4', '#386cb0' , '#f0027f' , '#bf5b17' , '#666666')  # ColorBrewer Accent reorganised
    j = 0
    categories = []
    for attributeName in values :
        symbol = QgsFillSymbolV2.createSimple({'style': 'solid', 'color': AccentColorList[(j+2) % 8 ], 'width_border':'0.1'})
        category = QgsRendererCategoryV2(attributeName,symbol,attributeName)
        categories.append(category)
        j += 1
    renderer = QgsCategorizedSymbolRendererV2(fields[-1].name(), categories)

    layer.setRendererV2(renderer)
    
def drawSector(center, radius, startAngle, stopAngle, precision):
    sector = [QgsPoint(center)]
    angle = startAngle
    step = math.pi / (precision*2)
    while angle < stopAngle :
        x = center[0] + radius * math.sin(angle)
        y = center[1] + radius * math.cos(angle)
        sector.append(QgsPoint(x,y))
        angle += step
    sector.append(QgsPoint((center[0] + radius * math.sin(stopAngle)),\
                   (center[1] + radius * math.cos(stopAngle))))
    sector.append(QgsPoint(center))
    return sector
    
def ronds(inputLayer, analysisAttributes, scale, outputLayerName, extendedAnalysis = False):
    """
        Proportional circles or sectors
          inputLayer = input layer (points or polygons)
          analysisAttributes = list of index or names of the variables to reprensend
          scale : polygon layer for an automatic scale or tuple (maxValue, maxRadius) for a custom scale
          extendedAnalysis : True for an extended analysis (True/False) 
          
        Outputs:
          resultLayer,
          maximumValue, maximumRadius, 
          missingValues = number of missing values (or =0), 
          crsString = string of the input layer
    """
    # convert list of selected attributes names to a list of attributes index
    if isinstance(analysisAttributes, str):
        analysisAttributes = (analysisAttributes,)
    listeVariable = [inputLayer.fieldNameIndex(element) \
                    for element in analysisAttributes]
                    
    nbSector = len(analysisAttributes)
    zfillValue = nbSector // 10 + 1
    sectorAngle = 2.0 * math.pi / nbSector

    # convert the values to absolute values
    absoluteValuesList = []
    for col in listeVariable :
        # restrict the input layer to the selected features layer if necessary
        if inputLayer.selectedFeatures():
            features = inputLayer.selectedFeatures()
        else :
            features = inputLayer.getFeatures()
        listElements = [abs(element.attributes()[col]) \
            for element in features if element.attributes()[col]]
        absoluteValuesList.extend(listElements)

    if len(absoluteValuesList) > 0 :   # if not -> nothinq to do
        maximumValue = max(absoluteValuesList)
        sumValues = sum(absoluteValuesList)

        # automatic scale 
        if isinstance(scale, QgsVectorLayer):  
            contour = scale
            # restrict the reference layer to the selected features layer if necessary
            if contour.selectedFeatures():
                features = contour.selectedFeatures()
            else :
                features = contour.getFeatures() 
            layerArea = sum([element.geometry().area() for element in features])
            coeff = (layerArea/(7*(sumValues/nbSector)))**.5
            
        # custom scale
        else:  
            coeff = scale[1] * (math.pi/scale[0])**.5
        maximumRadius = coeff * (maximumValue/math.pi) ** .5
        
        newAttributeList = list(inputLayer.pendingFields())    
        
        missingValues = 0
        sectorNr = 0        
        
        # create a temporary table : tableau = [radius, outfeat]
        tableau =[]

        field_names = [field.name() for field in inputLayer.pendingFields() ]

        for col in listeVariable :
            startAngle = sectorAngle * sectorNr
            stopAngle = startAngle + sectorAngle
            
            # restrict the input layer to the selected features layer if NO extended analysis
            if inputLayer.selectedFeatures() and not extendedAnalysis:
                features = inputLayer.selectedFeatures()
            else :
                features = inputLayer.getFeatures()

            for element in features :
                currentValue = element.attributes()[col]
                if currentValue and currentValue !=0:
                    absValue = abs(currentValue)
                    radius = coeff * (absValue/math.pi) ** .5
                    center = element.geometry().centroid()           
                    outFeat = QgsFeature()
                    precision = (5.0 + 10.0 * (radius / maximumRadius))  

                    if nbSector == 1:   # draw circles -> buffer
                        outFeat.setGeometry(center.buffer(radius,precision))
                    else :              # draw sectors
                        outFeat.setGeometry(QgsGeometry.fromPolygon([drawSector(\
                            center.asPoint(), radius,startAngle, stopAngle, precision)]))

                    # add value and radius to the new attribute table
                    originLine = element.attributes()
                    originLine.extend([currentValue,radius])

                    # for sectors add also the name of the variable
                    if nbSector == 1 :
                        if currentValue < 0:
                            sign = ' < 0' 
                            texte = '2 - '
                        else :
                            sign = ' >= 0'
                            texte = '1 - '
                    else :
                        sign = ''
                        texte = str(sectorNr + 1).zfill(zfillValue) + ' - '
                    originLine.append(texte + field_names[col] + sign)
                    outFeat.setAttributes(originLine)
                    tableau.append((radius, outFeat))

                else:
                    # count the missing or values equal to zero
                    missingValues +=1
            sectorNr += 1

        # sort the features to put the smal geometries to the front
        tableau.sort(reverse = True)

        listElements = [elem[1] for elem in tableau]
        features =  inputLayer.getFeatures()    
        f = features.next()

        # add 'VAL' for value and 'R' for radius to the attributes
        # Increment 'VAL' and 'R' if still exist in the origin attribute table 
        attributeList = [element.name() for element in f.fields().toList()]
        valueName, radiusName, varName = u'VAL', u'R', u'VARIABLE'
        i, iLabel = 0, ''
        while (valueName+iLabel) in attributeList \
                or radiusName+iLabel in attributeList\
                or varName + iLabel in attributeList:
            i += 1
            iLabel = '_'+str(i)
        valueName += iLabel
        radiusName += iLabel
        varName += iLabel
        
        # New polygon layer

        # crs of the input layer
        if 'EPSG' in inputLayer.crs().authid() :
            crsString = inputLayer.crs().authid()
        else : 
            crsString = inputLayer.crs().toWkt()
            
        resultLayer = QgsVectorLayer('Polygon?crs='+crsString, outputLayerName,'memory')
        
        # resultLayer.startEditing()
        pr = resultLayer.dataProvider()
        newAttributeList.extend([QgsField(valueName, QVariant.Double, "Real", 10,3)])
        newAttributeList.extend([QgsField(radiusName, QVariant.Double, "Real", 10,1)])
        # if nbSector > 1:
        newAttributeList.extend([QgsField(varName, QVariant.String, "String", 50)])

        pr.addAttributes(newAttributeList)
        resultLayer.updateFields()
        pr.addFeatures( listElements )
        
        resultLayer.selectAll()  # 2.2
        resultLayer.setExtent(resultLayer.boundingBoxOfSelected()) #2.2
        resultLayer.setSelectedFeatures([]) #2.2
        
        resultLayer.commitChanges()
        # resultLayer.updateExtents()

        return resultLayer, maximumValue, maximumRadius, missingValues, crsString
    else :
        return NULL, NULL, NULL, NULL, NULL


def legendeRonds(crsString, legendCoordinates, scale, legendLayerName, nbSector=1, listValues=[]):
    """
        Legend for the proportional circles or sectors
          crsString = crs used for the output layer
          legendCoordinates = coordinates of the legend
          scale = (maximumValue, maximumRadius)
          legendLayerName = name of the output layer
          nbSector = number of sectors (default = 1 for circles)
          listValues = list of values to reprensent in the legend
          
        Output:
          resultLayer
    """    
    coeff = scale[1] * (math.pi/scale[0])**.5
    if listValues == [] :
        maximumValue = scale[0]
        listValues = (maximumValue, maximumValue/3, maximumValue/9)
    else :
        listValues.sort(reverse = True)
        maximumValue = max(listValues)

        # sectorNr = 0
    maximumRadius = coeff * (maximumValue/math.pi) ** .5
    
    # create a new layer for the legend

    resultLayer = QgsVectorLayer('Polygon?crs='+crsString, legendLayerName,'memory')

    pr = resultLayer.dataProvider()
    newAttributeList = []
    valueName, radiusName, varName = u'VAL', u'R', u'SECT'
    newAttributeList.extend([QgsField(valueName, QVariant.Double, "Real", 10,3)])
    newAttributeList.extend([QgsField(radiusName, QVariant.Double, "Real", 10,1)])
    newAttributeList.extend([QgsField(varName, QVariant.String, "String", 10)])
    
    # X, Y ALPHA attributes for the position of the labels
    newAttributeList.extend([QgsField('X', QVariant.Double, "Real", 10,3)])
    newAttributeList.extend([QgsField('Y', QVariant.Double, "Real", 10,3)])
    newAttributeList.extend([QgsField('ALPHA', QVariant.Double, "Real", 10,3)])
    newAttributeList.extend([QgsField('POS_LEG', QVariant.String, "String", 30)])
    pr.addAttributes(newAttributeList)
    resultLayer.updateFields()

    sectorAngle = 2.0 * math.pi / nbSector
    listGeom = []
    sectorNr = 0

    # draw the sectors / circles in the legend

    for i in range(nbSector):
        for element in listValues :
            sectorNr = 1 + i
            startAngle = sectorAngle * i
            stopAngle = startAngle + sectorAngle
            currentValue = element
            if currentValue and currentValue !=0:
                geom = QgsFeature()
                center = QgsGeometry.fromPoint(QgsPoint(legendCoordinates[0], legendCoordinates[1]))
                absValue = abs(currentValue)
                radius = coeff * (absValue/math.pi) ** .5
          
                outFeat = QgsFeature()
                precision = (5.0 + 10.0 * (radius / maximumRadius))  

                if nbSector < 3:
                    # aling circles / half circles to the bottom
                    x = legendCoordinates[0]
                    y = legendCoordinates[1] + radius - maximumRadius
                    center = QgsGeometry.fromPoint(QgsPoint(x, y))

                    if nbSector == 1:
                        # draw circles (buffer)
                        outFeat.setGeometry(center.buffer(radius,precision))

                    else :
                        # draw sectors
                        outFeat.setGeometry(QgsGeometry.fromPolygon([drawSector(\
                        center.asPoint(), radius,startAngle, stopAngle, precision)]))


                else :              
                    # algin to the center
                    x, y = legendCoordinates[0], legendCoordinates[1] 
                    center = QgsGeometry.fromPoint(QgsPoint(x,y))
                    outFeat.setGeometry(QgsGeometry.fromPolygon([drawSector(\
                        center.asPoint(), radius,startAngle, stopAngle, precision)]))

                centroidFeature = outFeat.geometry().centroid().asPoint()
                # fill attribute table
                if sectorNr == 1:
                    # fill the coordinates of the labels
                    labelPosition = str((2*round(maximumRadius))-(centroidFeature[0]-x))+','+str(-1.0*round(radius)+(centroidFeature[1]-y))
                    outFeat.setAttributes([element,radius, sectorNr,NULL,NULL,NULL,labelPosition])
                else:
                    outFeat.setAttributes([element,radius, sectorNr,NULL,NULL,NULL,NULL])

            listGeom.append(outFeat)

    # draw the lines in the legend (flat rectangle)
    
    for element in listValues :
        lineLength = maximumRadius * 1.25
        outFeat2 = QgsFeature()
        radius = coeff * (abs(element)/math.pi) ** .5
        x = legendCoordinates[0]
        if nbSector < 3:
            y = legendCoordinates[1] + 2.0*radius - maximumRadius 
        else :
            y = legendCoordinates[1] + radius
        points =[]
        points.append(QgsPoint(x,y))
        points.append(QgsPoint(x+lineLength,y))
        points.append(QgsPoint(x+lineLength,y))
        points.append(QgsPoint(x,y))
        outFeat2.setGeometry(QgsGeometry.fromPolygon([points]))
        outFeat2.setAttributes([element,NULL, 'L',NULL,NULL,NULL])
        listGeom.append(outFeat2)
    
    pr.addFeatures( listGeom )
    resultLayer.selectAll()
    resultLayer.setExtent(resultLayer.boundingBoxOfSelected())
    # resultLayer.updateExtents()

    return resultLayer
        





    

