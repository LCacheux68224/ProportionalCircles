# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ProportionalCircles
                                 A QGIS plugin
 Proportional circles map
                              -------------------
        begin                : 2014-07-27
        copyright            : (C) 2014 by Lionel Cacheux
        email                : lionel.cacheux@gmx.fr
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

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from proportionalcirclesdialog import ProportionalCirclesDialog
import os.path



from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *



# Import the utilities from the fTools plugin (a standard QGIS plugin),
# which provide convenience functions for handling QGIS vector layers
import sys, os, imp
import fTools

import math

# Used to print a informations in the message bar of the canvas 
from PyQt4.QtGui import QProgressBar
from qgis.gui import QgsMessageBar
from qgis.utils import iface

class ProportionalCircles:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'proportionalcircles_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
	path = os.path.dirname(fTools.__file__)
	self.ftu = imp.load_source('ftools_utils', os.path.join(path,'tools','ftools_utils.py'))

        # Create the dialog (after translation) and keep reference
        self.dlg = ProportionalCirclesDialog()

    def initGui(self):
        text = QtGui.QApplication.translate("Proportional circles","Proportional circles", None, QtGui.QApplication.UnicodeUTF8)
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/ProportionalCircles/iconRonds.png"), 
            text, self.iface.mainWindow())


        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        #self.iface.addToolBarIcon(self.action)
        #self.iface.addPluginToMenu(u"&Analyses en ronds", self.action)

        # Add toolbar button and menu item
        if hasattr( self.iface, 'addDatabaseToolBarIcon' ):
            self.iface.addVectorToolBarIcon(self.action)
        else:
            self.iface.addToolBarIcon(self.action)
        if hasattr( self.iface, 'addPluginToVectorMenu' ):
            self.iface.addPluginToVectorMenu( text, self.action )
        else:
            self.iface.addPluginToMenu(text, self.action)

    def unload(self):
        text = QtGui.QApplication.translate("ProportionalCircles","Proportional circles", None, QtGui.QApplication.UnicodeUTF8)

        # Remove the plugin menu item and icon
        #self.iface.removePluginMenu(u"&Analyses en ronds", self.action)
        #self.iface.removeToolBarIcon(self.action)

        if hasattr( self.iface, 'removePluginVectorMenu' ):
            self.iface.removePluginVectorMenu( text, self.action )
        else:
            self.iface.removePluginMenu( text, self.action )
        if hasattr( self.iface, 'removeVectorToolBarIcon' ):
            self.iface.removeVectorToolBarIcon(self.action)
        else:
            self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # Populate the combo boxes
        self.dlg.onlyLegend.setEnabled(False)
        self.dlg.populateLayers()
        if self.dlg.analysisLayer.currentText() == '' :
		    self.dlg.autoScale.setEnabled(False)
		    self.dlg.customScale.setChecked(True)
        else :
		    self.dlg.autoScale.setEnabled(True)
		    self.dlg.autoScale.setChecked(True)			
			
			
        self.dlg.circlesFileName.clear()
        self.dlg.legendFileName.clear()
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()

        # See if OK was pressed
        if result == 1:

	    # do something useful (delete the line containing pass and
	    # substitute with your code)

	    # if self.dlg.inputValue.currentText() == '':
	    if len(self.dlg.selectedAttributesList) < 1:
	            iface.messageBar().pushMessage("Error", " No valid datas" , level = QgsMessageBar.WARNING, duration = 10)
            elif (self.dlg.shapefileOutput.isChecked() and self.dlg.circlesFileName.text() == '')  :
                    iface.messageBar().pushMessage("Shapefile error ", " Wrong or missing file name" , level = QgsMessageBar.WARNING, duration = 10)
            else:

		    QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )  # start processing

		    inputLayer = self.ftu.getMapLayerByName(self.dlg.inputLayer.currentText())

		    # valueFieldName = self.dlg.inputValue.currentText()
		    valueFieldNames = self.dlg.selectedAttributesList
                    valueFieldIndex = []
                    nbSector = len(self.dlg.selectedAttributesList)
                    angleEnd = 2 * math.pi /nbSector
                    sectorAngle = 2 * math.pi / nbSector  
                    for i in xrange(0 , len(valueFieldNames)) :
                        valueFieldIndex.append(inputLayer.fieldNameIndex(valueFieldNames[i]))
		    # valueFieldIndex = inputLayer.fieldNameIndex(valueFieldName)
		    maxValue, totalColumn, newTable, missingValues = self.newSortedAttributeTable(inputLayer, valueFieldIndex)
		    

		    # Scale 
		    if self.dlg.autoScale.isChecked():		# automatic scale : total of the areas of the circles = 1/7 area of the analysis area
		        analysisLayer = self.ftu.getMapLayerByName(self.dlg.analysisLayer.currentText())
		        customScale = False
		        analysisArea = self.layerArea(analysisLayer)
		        coeff = math.sqrt(nbSector*analysisArea/(7*math.pi*totalColumn))
		        scaleOk = True

		    else:  						# custom scale
		        customMaxValue = self.dlg.maxCustomValue.value()
		        customMaxRadius = self.dlg.maxCustomRadius.value()
		        customScale = True
		        if (customMaxValue == 0) or (customMaxRadius == 0):  
		               scaleOk = False
		        else:
		            scaleOk = True

		    if scaleOk:
		        newAttributesFieldsList = list(inputLayer.pendingFields())

                        # add a number to the fiel name 'VALUE' if the fiel stil exist in the attrubute table. ex: VALUE_1
                        valueLabel, iLabel = QtGui.QApplication.translate("ProportionalCircles",\
				QtGui.QApplication.translate("ProportionalCircles","VALUE", None, QtGui.QApplication.UnicodeUTF8), None, QtGui.QApplication.UnicodeUTF8), ''  
			i = 0
                        while inputLayer.fieldNameIndex(valueLabel+iLabel) >=0:
				i += 1
				iLabel = '_'+str(i)
			valueLabel +=iLabel	

                        # add a number to the fiel name 'RADIUS' if the fiel stil exist in the attribute table. ex: RADIUS_1
			radiusLabel, iLabel = QtGui.QApplication.translate("ProportionalCircles",\
				QtGui.QApplication.translate("ProportionalCircles","RADIUS", None, QtGui.QApplication.UnicodeUTF8), None, QtGui.QApplication.UnicodeUTF8) , ''
			i = 0
                        while inputLayer.fieldNameIndex(radiusLabel+iLabel) >=0:
				i += 1
				iLabel = '_'+str(i)
                        radiusLabel += iLabel

                        # add a number to the fiel name 'ROW' if the fiel stil exist in the attribute table. ex: ROW_1
			rowLabel, iLabel = QtGui.QApplication.translate("ProportionalCircles",\
				QtGui.QApplication.translate("ProportionalCircles","VARNAME", None, QtGui.QApplication.UnicodeUTF8), None, QtGui.QApplication.UnicodeUTF8) , ''
			i = 0
                        while inputLayer.fieldNameIndex(rowLabel+iLabel) >=0:
				i += 1
				iLabel = '_'+str(i)
                        rowLabel += iLabel

		        # add RADIUS AND VALUE to attributes table
		        newAttributesFieldsList.extend([QgsField(radiusLabel, QVariant.Double, "numeric", 10, 1),QgsField(valueLabel, QVariant.Double, "numeric", 10, 3),QgsField(rowLabel, QVariant.Double, "string", 255)])
		        
		        # new memory layer
		        crsString = inputLayer.crs().authid()  # crs of input layer
                        text = QtGui.QApplication.translate("ProportionalCircles","Proportional_Circles_", None, QtGui.QApplication.UnicodeUTF8)
		        resultLayer = QgsVectorLayer("Polygon?crs=" + crsString, text+inputLayer.name(), "memory")
		        resultLayer.startEditing()
		        resultLayer.dataProvider().addAttributes(newAttributesFieldsList)
		        resultLayer.updateFields()

		        if self.dlg.shapefileOutput.isChecked():
		            shapefilename = self.dlg.circlesFileName.text()
		            legendeShapefileName = self.dlg.legendFileName.text()


		        if customScale:
		             maxRadius = customMaxRadius
		        else:
		             maxRadius = math.sqrt(abs(maxValue) ) * coeff    

		        #ft = QgsFeature()
		        outFeat_centroids = QgsFeature()
		        #outFeat = QgsFeature()
		        point = QgsFeature()
		        circlesList = []
		        # bufferPrecision = 20

		        for ft in newTable:
		            
		            center = ft[2]         
		            attrs = ft[3]          # origin attributes
		            absoluteValue = ft[0]      
		            value = ft[1]         
                            sectorNr = ft[4]
                            print sectorNr
		            # Calculate radius
		            if absoluteValue !=0.0:    
		                if customScale:
		                    radius = customMaxRadius * math.sqrt(absoluteValue/customMaxValue)
		                else:
		                    radius = math.sqrt(absoluteValue ) * coeff

		                outFeat_centroids.setGeometry(center) # centre du cercle
		                point = QgsGeometry(outFeat_centroids.geometry())
                                bufferPrecision = 4.0 *( 3.0 + 20.0*radius /maxRadius)
		                # circle = point.buffer(radius,bufferPrecision)  # buffer circulaire autour d'un point
                                angleStart = 0
                                # angleEnd = math.pi/6

				sector = self.drawSector(center.asPoint(), radius, angleStart, angleEnd, nbSector, sectorAngle, sectorNr, bufferPrecision)
		                outFeat = QgsFeature()
		                #outFeat.setGeometry(circle)
                                # outFeatLigne.setGeometry(QgsGeometry.fromPolygon([listePoints2]))
		                outFeat.setGeometry(QgsGeometry.fromPolygon([sector]))
		                attrs.extend([radius, value, valueFieldNames[sectorNr]])
		                outFeat.setAttributes(attrs)
		                circlesList.append(outFeat)  
		                del outFeat
		                
		        resultLayer.addFeatures(circlesList)
		        resultLayer.updateExtents()
		        resultLayer.commitChanges()
		        resultLayer.setSelectedFeatures([])
		        if self.dlg.memoryOutput.isChecked():       	# add memory layer to the canevas
		            rendererV2 = resultLayer.rendererV2()
		            # load and apply style to circles layer
		            style_path = os.path.join( os.path.dirname(__file__), "ronds_style.qml" )
		            (errorMsg, result) = resultLayer.loadNamedStyle( style_path )
		            QgsMapLayerRegistry.instance().addMapLayer(resultLayer)


		        elif self.dlg.shapefileOutput.isChecked():	# save shapefile

		            error = QgsVectorFileWriter.writeAsVectorFormat(resultLayer, shapefilename, "CP1250", None, "ESRI Shapefile")
		            if self.dlg.addCanevas.isChecked():	# load layer and style
		                layername = os.path.splitext(os.path.basename(str(shapefilename)))[0]
		                resultLayer = QgsVectorLayer(shapefilename, layername, "ogr")
		                rendererV2 = resultLayer.rendererV2()
		                # load and apply style to circles layer
		                style_path = os.path.join( os.path.dirname(__file__), "ronds_style.qml" )
		                (errorMsg, result) = resultLayer.loadNamedStyle( style_path )
		                QgsMapLayerRegistry.instance().addMapLayer(resultLayer)

		        # del resultLayer

		        # create layer for legend
		        
			# Attribute fields X, Y, ALPHA for labeling
			# POS_LEG = déplacement X, Y des étiquettes par rapport au centroide. Labels follows the legend if moved 
		        fieldsListeLegende = []
		        fieldsListeLegende.extend([QgsField("RAYON", QVariant.Double, "numeric", 10,1) , QgsField("VALEUR", QVariant.Double, "numeric", 10,3), QgsField("X", QVariant.Double), QgsField("Y", QVariant.Double), QgsField("ALPHA", QVariant.Double), QgsField("POS_LEG", QVariant.String)])
		        crsString = resultLayer.crs().authid()  # same crs as circles layer
                        text = QtGui.QApplication.translate("ProportionalCircles","Legend_Prop_Circles_", None, QtGui.QApplication.UnicodeUTF8)
		        outputLegende = QgsVectorLayer("Polygon?crs=" + crsString, text+inputLayer.name(), "memory")

		        outputLegende.startEditing()
			outputLegende.dataProvider().addAttributes(fieldsListeLegende)
		        outputLegende.updateFields()

			circlesListLegend = []
	 
		        # max radius for the circles in the legend
		        if customScale:
		            maxRadius = customMaxRadius * math.sqrt(maxValue/customMaxValue)
		        else:
		            maxRadius = math.sqrt(maxValue) * coeff

		        # list of custom radiuses for the circles in the legend
		        legendCustomValues = self.dlg.legendCustomValues.text()
		        legendCustomValues = legendCustomValues.strip().replace(';',' ')
		        legendValuesList = legendCustomValues.split()

		        if len(legendValuesList) ==0:  # automatic VALUES for the circles in the legend 
		            legendError = False
		            legendValuesList = [maxValue/9, maxValue/3, maxValue]
			else:
		            try:			
				for i in range(len(legendValuesList)):  # custom values for the circles in the legend
				    legendValuesList[i] = float(legendValuesList[i])
		                legendError = False
		            except:   # if error in customisation -> automatic values for legend + warning message
				legendValuesList = [maxValue/9, maxValue/3, maxValue] 
		                legendError = True
		        legendValuesList.sort()

		        radiusList = []  

		        for i in range(len(legendValuesList)):
		            if customScale:
		                radius = customMaxRadius * math.sqrt(legendValuesList[i]/customMaxValue)
		            else:
		                radius = math.sqrt(legendValuesList[i] ) * coeff
		            radiusList.append(radius)

			# Legend position  

		        xLegend = inputLayer.extent().xMaximum()+ max(radiusList) *1.5 
		        yLegend = ( inputLayer.extent().yMinimum() + inputLayer.extent().yMaximum() ) /2

                        xLabel = 1.7*maxRadius

		        for i in range(len(radiusList)):
			    yCenter = yLegend + radiusList[i]-max(radiusList)

                            # use buffer to draw circle
		            outFeat2 = QgsFeature()
		  	    point = QgsFeature()
			    point2 = QgsFeature()
			    circle = QgsFeature()
		            circleValue = legendValuesList[i]
		            circleRadius = radiusList[i]
		            point.setGeometry(QgsGeometry.fromPoint(QgsPoint(xLegend, yCenter)))
			    point2 = QgsGeometry(point.geometry())
                            bufferPrecision = 3 + 20.0*radius /maxRadius
			    circle = point2.buffer(circleRadius,bufferPrecision)
			    outFeat2.setGeometry(circle)
                            yLabel = -radiusList[i]
                            legendPosition = str(xLabel) + ','+ str(yLabel)
                            outFeat2.setAttributes([circleRadius, circleValue, NULL, NULL,NULL,legendPosition])
			    circlesListLegend.append(outFeat2)

                            # draw a line (flat rectangle) between legend and labels
                            outFeatLigne = QgsFeature()
                            listePoints2 = self.flatRectangle([xLegend,yCenter] , circleRadius, maxRadius*1.5)
                            outFeatLigne.setGeometry(QgsGeometry.fromPolygon([listePoints2]))
		            outFeatLigne.setAttributes([circleRadius,NULL,NULL,NULL,NULL,NULL])
                            circlesListLegend.append(outFeatLigne)
			    
                            del outFeatLigne
			    del outFeat2

		        outputLegende.addFeatures(circlesListLegend)
		        outputLegende.updateExtents()
		        outputLegende.commitChanges()

		        if self.dlg.memoryOutput.isChecked():	# add legend to canevas
			    # customize style
			    rendererV2 = outputLegende.rendererV2()
			    # load and apply style to legend
			    style_path = os.path.join( os.path.dirname(__file__), "legende_style.qml" )
			    (errorMsg, result) = outputLegende.loadNamedStyle( style_path )
			    QgsMapLayerRegistry.instance().addMapLayer(outputLegende)

		        elif self.dlg.shapefileOutput.isChecked(): # save legend as a shapefile
		            error = QgsVectorFileWriter.writeAsVectorFormat(outputLegende, legendeShapefileName, "CP1250", None, "ESRI Shapefile")
		            if self.dlg.addCanevas.isChecked():  # add legend layer to the canevas
		                layername = os.path.splitext(os.path.basename(str(legendeShapefileName)))[0]
		                outputLegende = QgsVectorLayer(legendeShapefileName, layername, "ogr")

		        	# # customize style
				rendererV2 = outputLegende.rendererV2()
				# load and apply style to legend
				style_path = os.path.join( os.path.dirname(__file__), "legende_style.qml" )
				(errorMsg, result) = outputLegende.loadNamedStyle( style_path )
		                QgsMapLayerRegistry.instance().addMapLayer(outputLegende)


		    # Warning messages

		    if scaleOk == False:     # error in custom legend

                        text1 = QtGui.QApplication.translate("ProportionalCircles","null radius or value in customised legend", None, QtGui.QApplication.UnicodeUTF8)
			iface.messageBar().pushMessage(text1, "", level = QgsMessageBar.WARNING, duration = 5)

		    else:
                        text1 = QtGui.QApplication.translate("ProportionalCircles","Proportional circles", None, QtGui.QApplication.UnicodeUTF8)
                        text2 = QtGui.QApplication.translate("ProportionalCircles","Missing value(s) : %d ; Max radius : %d ; Max Value :  %d", None, QtGui.QApplication.UnicodeUTF8)  
			iface.messageBar().pushMessage(text1, text2 %(missingValues, maxRadius,  maxValue), level = QgsMessageBar.INFO, duration = 30)
			if legendError == True:

                            text1 = QtGui.QApplication.translate("ProportionalCircles","Automatic legend generated", None, QtGui.QApplication.UnicodeUTF8)
                            text2 = QtGui.QApplication.translate("ProportionalCircles","syntax error in customised legend", None, QtGui.QApplication.UnicodeUTF8)  

			    iface.messageBar().pushMessage(text1, text2 , level = QgsMessageBar.WARNING, duration = 5)

		    QApplication.restoreOverrideCursor()  



    
    def newSortedAttributeTable(self, inputLayer, columnNumber):
        '''
            Extract attributes to a list :  [ Value , (coordinates) , [original attributes] ]
        '''
        table = []
        totalOfColumn = 0
        missingValues = 0
        maxAbsoluteValue = 0
        coeff = len(columnNumber)
        print columnNumber

	if inputLayer.selectedFeatures():
            features = inputLayer.selectedFeatures()
	else:
	    features = inputLayer.getFeatures()

        for elem in features : 
            for sectorNr in xrange(0, len(columnNumber)):
                value = elem.attributes()[columnNumber[sectorNr]] 
                #print i, value
	        if value:
	            totalOfColumn += abs(value)
                    if abs(value)>maxAbsoluteValue:
                        maxAbsoluteValue = abs(value)

        if not inputLayer.selectedFeatures() or self.dlg.selectedFeatures.isChecked():
            features = inputLayer.getFeatures()
	else:
	    features = inputLayer.selectedFeatures()

        for elem2 in features : 
            for sectorNr in xrange(0, len(columnNumber)):

                value = elem2.attributes()[columnNumber[sectorNr]]
                if not value:
                    if value !=0: missingValues +=1
                else:
                    listeElements = [abs(value), value, elem2.geometry().centroid() , elem2.attributes(), sectorNr]
                    table += [listeElements]

        #table = sorted(table, reverse = True)   # from the smalest circles to the bigest 
		table.sort()
        print maxAbsoluteValue

        return maxAbsoluteValue, totalOfColumn, table, missingValues


    def layerArea(self, areaOfAnalysis):
        ''' 
           area of the reference map
        '''
        layerArea = 0
        if areaOfAnalysis.selectedFeatures():
	    areaOfAnalysis = areaOfAnalysis.selectedFeatures()
        else :
	    areaOfAnalysis = areaOfAnalysis.getFeatures() 
        for elem in areaOfAnalysis:
            layerArea += elem.geometry().area()
        return layerArea


    def flatRectangle(self, center, radius,lineLength):
        '''
           flat rectangle to represent a line between legend and label
           did not made a line layer for that because the lines should follow the legend if moved otherwise we have to move the lines separatedely from the circles ...
        '''
        x = center[0]
        y = center[1] + radius
        points = []
        
        points.append(QgsPoint(x,y))
        points.append(QgsPoint(x+lineLength,y))
        points.append(QgsPoint(x+lineLength,y))
        points.append(QgsPoint(x,y))
        

        return points

    def drawSector(self, center, radius, angleStart, angleStop, nbSector, sectorAngle, sectorNr, precision):
        '''
            draw a sector
        '''
        sectorAngle2 = 2.0 * math.pi / nbSector
        angleStart2 = sectorAngle2*sectorNr
        # angle = sectorAngle*sectorNr
        angleStop2 = angleStart2 + sectorAngle2
        pas = precision/radius
        if nbSector > 1 :
            sector = [QgsPoint(center)]
        else :
            sector = []
        angle = angleStart2
        sector.append(QgsPoint((center[0] + radius * math.sin(angleStart2)), (center[1] + radius * math.cos(angleStart2)) )) 
        while angle < angleStop2 :
            x1 = center[0] + radius * math.sin(angle)
            y1 = center[1] + radius * math.cos(angle)
            sector.append(QgsPoint(x1,y1))
            angle += pas   
        sector.append(QgsPoint((center[0] + radius * math.sin(angleStop2)), (center[1] + radius * math.cos(angleStop2)) ))  
        if nbSector > 1.0 :
            sector.append(QgsPoint(center))
        # print center[1] + radius * math.sin(angleStart2), center[1] + radius * math.sin(angleStop2), center[1]
        return sector



