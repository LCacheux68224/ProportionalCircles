# -*- coding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import QVariant
from qgis.core import *
import math

def layerArea(polygonLayer):
    """
        Area of a polygon layer
        Usage : area = layerArea(polygonLayer)
    """
    if polygonLayer.wkbType() not in [QGis.WKBPolygon, QGis.WKBMultiPolygon] :
        raise NameError('must be a polygon layer')
    if polygonLayer.selectedFeatures():
        features = polygonLayer.selectedFeatures()
    else :
        features = polygonLayer.getFeatures() 
    surface = sum([element.geometry().area() for element in features])
    return surface
    
def summaryAttributes(layer, columnNumber):
    """
        Absolute max, and total of a list of columns
        Usage : (total, max)  = summaryAttributes(layer, [list of columnNumbers])
    """
    absoluteValuesList = []
    for col in columnNumber :
        if layer.selectedFeatures():
            features = layer.selectedFeatures()
        else :
            features = layer.getFeatures()
        listElements = [abs(element.attributes()[col]) \
            for element in features if element.attributes()[col]]
        absoluteValuesList.extend(listElements)
    lenList = len(absoluteValuesList)
    if lenList > 0 :
        maximumAbsoluteValue = max(absoluteValuesList)
        sumAbsoluteValues = sum(absoluteValuesList)
    else :
        maximumAbsoluteValue = NULL
        sumAbsoluteValues = NULL       
    return sumAbsoluteValues, maximumAbsoluteValue
    
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
        Anlyse en ronds ou en secteurs
        Usage : rond(inputLayer, analysisAttributes, scale, extendedAnalysis = False)
          inputLayer = fond a analyser (points ou polygones)
          analysisAttributes = numero ou liste des numeros/nom des colonnes correspondant a la ou aux variables a analyser
          scale : contour pour une echelle automatique ou tuple (valMax, rayonMax)
          extendedAnalysis : si on veut une analyse etendue (True/False) 
       ------- 
        Proportional circles or sectors
          inputLayer = input layer (points or polygons)
          analysisAttributes = index or names of the variables
          scale : polygon layer for an automatic scale or tuple (maxValue, maxRadius) for a custom scale
          extendedAnalysis : True for an extended analysis (True/False) 
    """
    if isinstance(analysisAttributes, str):
        analysisAttributes = (analysisAttributes,)
    listeVariable = [inputLayer.fieldNameIndex(element) \
                    for element in analysisAttributes]
    nbSector = len(analysisAttributes)
    sectorAngle = 2.0 * math.pi / nbSector
    sumValues, maximumValue = summaryAttributes(inputLayer, listeVariable)


    if sumValues :
        if isinstance(scale, QgsVectorLayer):  # automatic scale 
            contour = scale
            coeff = (layerArea(contour)/(7*(sumValues/nbSector)))**.5
        else:  # custom scale
            coeff = scale[1] * (math.pi/scale[0])**.5
        maximumRadius = coeff * (maximumValue/math.pi) ** .5
        
        newAttributeList = list(inputLayer.pendingFields())    
        
        tableau =[]
        missingValues = 0
        sectorNr = 0
        field_names = [field.name() for field in inputLayer.pendingFields() ]
        for col in listeVariable :

            startAngle = sectorAngle * sectorNr
            stopAngle = startAngle + sectorAngle
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
                    precision = 4*(3.0 + 10.0 * radius / maximumRadius)  
                    if nbSector == 1:   # ronds simples -> buffer

                        outFeat.setGeometry(center.buffer(radius,precision))
                    else :              # secteurs
                        outFeat.setGeometry(QgsGeometry.fromPolygon([drawSector(\
                            center.asPoint(), radius,startAngle, stopAngle, precision)]))
                    originLine = element.attributes()
                    originLine.extend([currentValue,radius])
                    if nbSector > 1:
                        originLine.append(field_names[col])
                    outFeat.setAttributes(originLine)
                    tableau.append((radius, outFeat))
                else:
                    missingValues +=1
            sectorNr += 1
        tableau.sort(reverse = True)
        listElements = [elem[1] for elem in tableau]

        features =  inputLayer.getFeatures()    
        f = features.next()
        # Ajout des colonnes 'VAL' pour valeur et 'R' pour rayon
        # Incrementation du nom de ces colonnes si celles-ci existent deja dans la table attributaire d'origine.
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
        
        # Creation d'une couche de polygones
        # projection = 'Polygon?crs=epsg:2154'
        # projection = inputLayer.crs().authid()
        if 'EPSG' in inputLayer.crs().authid() :
            crsString = inputLayer.crs().authid()
        else : 
            crsString = inputLayer.crs().toWkt()
        resultLayer = QgsVectorLayer('Polygon?crs='+crsString, outputLayerName,'memory')
        # resultLayer.startEditing()
        pr = resultLayer.dataProvider()
        newAttributeList.extend([QgsField(valueName, QVariant.Double, "Real", 10,3)])
        newAttributeList.extend([QgsField(radiusName, QVariant.Double, "Real", 10,1)])
        if nbSector > 1:
            newAttributeList.extend([QgsField(varName, QVariant.String, "String", 50)])

        pr.addAttributes(newAttributeList)
        resultLayer.updateFields()

        pr.addFeatures( listElements )
        # resultLayer.commitChanges()
        resultLayer.updateExtents()

        return resultLayer, maximumValue, maximumRadius, missingValues
    else :
        return NULL, NULL, NULL, NULL


def legendeRonds(crs, legendCoordinates, scale, legendLayerName, nbSector=1, listValues=[]):
    coeff = scale[1] * (math.pi/scale[0])**.5
    if listValues == [] :
        maximumValue = scale[0]
        listValues = (maximumValue, maximumValue/3, maximumValue/9)
    else :
        listValues.sort(reverse = True)
        maximumValue = max(listValues)

        sectorNr = 0
    maximumRadius = coeff * (maximumValue/math.pi) ** .5

    resultLayer = QgsVectorLayer('Polygon?crs='+crs, legendLayerName,'memory')
    # resultLayer.startEditing()
    pr = resultLayer.dataProvider()
    newAttributeList = []
    valueName, radiusName, varName = u'VAL', u'R', u'SECT'
    newAttributeList.extend([QgsField(valueName, QVariant.Double, "Real", 10,3)])
    newAttributeList.extend([QgsField(radiusName, QVariant.Double, "Real", 10,1)])
    newAttributeList.extend([QgsField(varName, QVariant.String, "String", 10)])
    newAttributeList.extend([QgsField('X', QVariant.Double, "Real", 10,3)])
    newAttributeList.extend([QgsField('Y', QVariant.Double, "Real", 10,3)])
    newAttributeList.extend([QgsField('ALPHA', QVariant.Double, "Real", 10,3)])
    pr.addAttributes(newAttributeList)
    resultLayer.updateFields()
    sectorAngle = 2.0 * math.pi / nbSector
    listGeom = []
    sectorNr = 0
    for i in range(nbSector):
        for element in listValues :
            sectorNr = 1+i
            startAngle = sectorAngle * i
            stopAngle = startAngle + sectorAngle
            currentValue = element
            if currentValue and currentValue !=0:
                geom = QgsFeature()
                center = QgsGeometry.fromPoint(QgsPoint(legendCoordinates[0], legendCoordinates[1]))
                absValue = abs(currentValue)
                radius = coeff * (absValue/math.pi) ** .5
          
                outFeat = QgsFeature()
                precision = 4*(3.0 + 10.0 * radius / maximumRadius)  
                if nbSector < 3:   # ronds simples -> buffer
                    x = legendCoordinates[0]
                    y = legendCoordinates[1] + radius - maximumRadius
                    center = QgsGeometry.fromPoint(QgsPoint(x, y))
                    if nbSector == 1:
                        outFeat.setGeometry(center.buffer(radius,precision))
                        # outFeat.setAttributes([element,radius])
                    else :
                        outFeat.setGeometry(QgsGeometry.fromPolygon([drawSector(\
                        center.asPoint(), radius,startAngle, stopAngle, precision)]))
                    # outFeat.setAttributes([element,radius, sectorNr])
                else :              # secteurs
                    x, y = legendCoordinates[0], legendCoordinates[1] 
                    center = QgsGeometry.fromPoint(QgsPoint(x,y))
                    outFeat.setGeometry(QgsGeometry.fromPolygon([drawSector(\
                    center.asPoint(), radius,startAngle, stopAngle, precision)]))
                if sectorNr == 1:
                    outFeat.setAttributes([element,radius, sectorNr,x+1.5*maximumRadius,y+radius,NULL])
                else:
                    outFeat.setAttributes([element,radius, sectorNr,NULL,NULL,NULL])

            listGeom.append(outFeat)
    # lines
    
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
    resultLayer.updateExtents()


    return resultLayer
        





    

