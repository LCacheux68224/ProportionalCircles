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
from qgis.gui import *
from fonctionsCarto import *

import sys, os, imp

# Used to print a informations in the message bar of the canvas 
from PyQt4.QtGui import QProgressBar
from qgis.utils import iface

import math

class ProportionalCircles:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale for translation
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'proportionalcircles_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ProportionalCirclesDialog()

    def initGui(self):
        pluginName = QtGui.QApplication.translate("Proportional circles","Proportional circles", None, QtGui.QApplication.UnicodeUTF8)
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/ProportionalCircles/iconRonds.png"), 
            pluginName, self.iface.mainWindow())

        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        if hasattr( self.iface, 'addDatabaseToolBarIcon' ):
            self.iface.addVectorToolBarIcon(self.action)
        else:
            self.iface.addToolBarIcon(self.action)
        if hasattr( self.iface, 'addPluginToVectorMenu' ):
            self.iface.addPluginToVectorMenu( pluginName, self.action )
        else:
            self.iface.addPluginToMenu(pluginName, self.action)

    def unload(self):
        pluginName = QtGui.QApplication.translate("ProportionalCircles","Proportional circles", None, QtGui.QApplication.UnicodeUTF8)

        # Remove the plugin menu item and icon

        if hasattr( self.iface, 'removePluginVectorMenu' ):
            self.iface.removePluginVectorMenu( pluginName, self.action )
        else:
            self.iface.removePluginMenu( pluginName, self.action )
        if hasattr( self.iface, 'removeVectorToolBarIcon' ):
            self.iface.removeVectorToolBarIcon(self.action)
        else:
            self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # Populate the combo boxes
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
        if result == 1 :
        
            if self.dlg.legendOnly == False :  # Generates an analysis and a legend 
                try :
                    # start waitCursor
                    QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )  

                    # recover the options from the plugin gui
                    inputLayer = QgsMapLayerRegistry.instance().mapLayersByName(self.dlg.inputLayer.currentText())[0]
                    
                    resultNameLayer = QtGui.QApplication.translate("ProportionalCircles","Proportional_Circles_", None, QtGui.QApplication.UnicodeUTF8)+inputLayer.name()
                    valueFieldNames = self.dlg.selectedAttributesList
                    nbSector = len(valueFieldNames)
                    extendedAnalysis = self.dlg.selectedFeatures.isChecked()

                    # Scale of the circles / sectors
                    if self.dlg.autoScale.isChecked():        # automatic scale : total of the areas of the circles = 1/7 area of the analysis area                       
                        scale = QgsMapLayerRegistry.instance().mapLayersByName(self.dlg.analysisLayer.currentText())[0]
                        
                    else :                                      # custom scale
                        scale = ( self.dlg.maxCustomValue.value(), self.dlg.maxCustomRadius.value() )

                    # proceed analysis
                    outputLayer, maximumValue, maximumRadius, missingValues, crsString = ronds(inputLayer, valueFieldNames, scale, resultNameLayer, extendedAnalysis)

                    # fill MaxValue, MaxRadius and NbSector in lengend only GUI part
                    self.dlg.legendOnlyMaxCustomValue.setValue(maximumValue)
                    self.dlg.legendOnlyMaxCustomRadius.setValue(maximumRadius) 
                    self.dlg.legendOnlyNbSector.setValue(nbSector)
                    
                    # Output
                    if outputLayer :   # if resultLayer is Ok...

                        if self.dlg.memoryOutput.isChecked():           # ...add the memory layer to the canevas
                            setTypoColor(outputLayer)   # customize style
                            QgsMapLayerRegistry.instance().addMapLayer(outputLayer)

                        else :                                          # ...or save as a shapefile
                            shapefilename = self.dlg.circlesFileName.text()
                            error = QgsVectorFileWriter.writeAsVectorFormat(outputLayer, shapefilename, "CP1250", None, "ESRI Shapefile")

                            if self.dlg.addCanevas.isChecked():         # ...and add saved layer to the canevas
                                layername = os.path.splitext(os.path.basename(shapefilename))[0]
                                loadedLayer = QgsVectorLayer(shapefilename, layername, "ogr")

                                setTypoColor(loadedLayer)  # customize style
                                QgsMapLayerRegistry.instance().addMapLayer(loadedLayer)  
                                                    
                        # show scale and amount of missing values in the message bar
                        text1 = QtGui.QApplication.translate("ProportionalCircles","Proportional circles", None, QtGui.QApplication.UnicodeUTF8)
                        text2 = QtGui.QApplication.translate("ProportionalCircles","Missing value(s) : %d ; Max value : %d ; Max radius :  %d", None, QtGui.QApplication.UnicodeUTF8)  
                        iface.messageBar().pushMessage(text1, text2 %(missingValues, maximumValue, maximumRadius), level = QgsMessageBar.INFO, duration = 15)

                        # lengend

                        # coordinates of the legend (at the right of the output layer)
                        coeff = maximumRadius * (math.pi/maximumValue)**.5
                        maxRadiusLegend = coeff * (maximumValue/math.pi) ** .5  
                        xLegend = outputLayer.extent().xMaximum() + maxRadiusLegend *2
                        yLegend = (outputLayer.extent().yMinimum() + outputLayer.extent().yMaximum())*.5    
                        del outputLayer  # no more needed
                        
                        legendLayer = legendeRonds(crsString, (xLegend,yLegend), (maximumValue,maximumRadius), 'legende rond', nbSector, self.dlg.legendValuesList)

                        if self.dlg.memoryOutput.isChecked():           # ...add memory legend layer to the canevas
                            rendererV2 = legendLayer.rendererV2()
                            # load and apply a style to circles layer from a file
                            style_path = os.path.join( os.path.dirname(__file__), "legendeStyle.qml" )
                            (errorMsg, result) = legendLayer.loadNamedStyle( style_path )

                            QgsMapLayerRegistry.instance().addMapLayer(legendLayer)

                        else :                                              # ...or save as a shapefile
                            legendFilename = self.dlg.legendFileName.text()
                            error = QgsVectorFileWriter.writeAsVectorFormat(legendLayer, legendFilename, "CP1250", None, "ESRI Shapefile")

                            if self.dlg.addCanevas.isChecked():         # ...and add saved layer to the canevas
                                layername = os.path.splitext(os.path.basename(legendFilename))[0]
                                loadedLayer = QgsVectorLayer(legendFilename, layername, "ogr")
                                # # customize style
                                rendererV2 = loadedLayer.rendererV2()
                                # load and apply a style to circles layer from a file
                                style_path = os.path.join( os.path.dirname(__file__), "legendeStyle.qml" )
                                (errorMsg, result) = loadedLayer.loadNamedStyle( style_path )
                                
                                QgsMapLayerRegistry.instance().addMapLayer(loadedLayer)    
                        del legendLayer

                    else :                  # Warning message if resultLayer is empty...
                        textError1 = QtGui.QApplication.translate("ProportionalCircles","Input error ", None, QtGui.QApplication.UnicodeUTF8)
                        textError2 = QtGui.QApplication.translate("ProportionalCircles","No valid datas available in the attribute table", None, QtGui.QApplication.UnicodeUTF8)
                        iface.messageBar().pushMessage(textError1, textError2 , level = QgsMessageBar.CRITICAL)
            
                finally :
                    # stop waitCursor
                    QApplication.restoreOverrideCursor()

            elif self.dlg.legendOnly :   # Generates only a legend 

                # use the CRS of the project
                canvas = self.iface.mapCanvas()
                mapRenderer = canvas.mapRenderer()
                srs=mapRenderer.destinationCrs()
                if 'EPSG' in srs.authid() :
                    crsString = srs.authid()
                else : 
                    crsString = srs.toWkt()

                # Center the legend in the canevas    
                canevasExtent = iface.mapCanvas().extent()
                xLegend = (canevasExtent.xMaximum()+canevasExtent.xMinimum() )/2
                yLegend = (canevasExtent.yMaximum()+canevasExtent.yMinimum() )/2

                scale = (self.dlg.legendOnlyMaxCustomValue.value(), self.dlg.legendOnlyMaxCustomRadius.value())
                nbSector = self.dlg.legendOnlyNbSector.value()

                legendOnlyLayer = legendeRonds(crsString, (xLegend,yLegend), scale, 'legende rond', nbSector, self.dlg.legendOnlyValuesList)

                if self.dlg.legendOnlyMemoryOutput.isChecked():           # ...add memory legend layer to the canevas
                    # customize style
                    rendererV2 = legendOnlyLayer.rendererV2()
                    # load and apply style to circles layer
                    style_path = os.path.join( os.path.dirname(__file__), "legendeStyle.qml" )
                    (errorMsg, result) = legendOnlyLayer.loadNamedStyle( style_path )

                    QgsMapLayerRegistry.instance().addMapLayer(legendOnlyLayer)
                    # Editing mode in order to move the legend easy
                    legendOnlyLayer.startEditing()
                    legendOnlyLayer.selectAll()

                else :                                              # ...or save as a shapefile
                    legendOnlyFilename = self.dlg.legendOnlyFileName.text()
                    error = QgsVectorFileWriter.writeAsVectorFormat(legendOnlyLayer, legendOnlyFilename, "CP1250", None, "ESRI Shapefile")

                    if self.dlg.legendOnlyAddCanevas.isChecked():         # ...and add saved layer to the canevas
                        layername = os.path.splitext(os.path.basename(legendOnlyFilename))[0]
                        loadedLayer = QgsVectorLayer(legendOnlyFilename, layername, "ogr")
                        # customize style
                        rendererV2 = loadedLayer.rendererV2()
                        # load and apply style to legend
                        style_path = os.path.join( os.path.dirname(__file__), "legendeStyle.qml" )
                        (errorMsg, result) = loadedLayer.loadNamedStyle( style_path )
                        QgsMapLayerRegistry.instance().addMapLayer(loadedLayer) 
                        # Editing mode in order to move the legend easy
                        loadedLayer.startEditing()
                        loadedLayer.selectAll()
                del legendOnlyLayer   


  


