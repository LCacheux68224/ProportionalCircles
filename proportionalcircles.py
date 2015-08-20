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
from fonctionsCarto import *


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

            # if self.dlg.inputValue.currentText() == '':
            if len(self.dlg.selectedAttributesList) < 1:
                textError1 = QtGui.QApplication.translate("ProportionalCircles","Input error ", None, QtGui.QApplication.UnicodeUTF8)
                textError2 = QtGui.QApplication.translate("ProportionalCircles"," No valid datas available in the attribute table", None, QtGui.QApplication.UnicodeUTF8)
                iface.messageBar().pushMessage(textError1, textError2, level = QgsMessageBar.CRITICAL, duration = 5)  
            else:
                try :

                    # start waitCursor
                    QApplication.setOverrideCursor( QCursor( Qt.WaitCursor ) )  

                    # recover the options from the plugin gui
                    inputLayer = self.ftu.getMapLayerByName(self.dlg.inputLayer.currentText())
                    if 'EPSG' in inputLayer.crs().authid() :
                        crsString = inputLayer.crs().authid()
                    else : 
                        crsString = inputLayer.crs().toWkt()

                            
                    resultNameLayer = QtGui.QApplication.translate("ProportionalCircles","Proportional_Circles_", None, QtGui.QApplication.UnicodeUTF8)+inputLayer.name()
                    valueFieldNames = self.dlg.selectedAttributesList
                    nbSector = len(valueFieldNames)
                    extendedAnalysis = self.dlg.selectedFeatures.isChecked()

                    # Scale of the circles / sectors
                    if self.dlg.autoScale.isChecked():        # automatic scale : total of the areas of the circles = 1/7 area of the analysis area
                        scale = self.ftu.getMapLayerByName(self.dlg.analysisLayer.currentText())

                    else :                                      # custom scale
                        scale = ( self.dlg.maxCustomValue.value(), self.dlg.maxCustomRadius.value() )

                    # proceed analysis
                    outputLayer, maximumValue, maximumRadius, missingValues = ronds(inputLayer, valueFieldNames, scale, resultNameLayer, extendedAnalysis)

                    # Output
                    if outputLayer :   # if resultLayer is Ok...
                        if self.dlg.memoryOutput.isChecked():           # ...add memory layer to the canevas
                            rendererV2 = outputLayer.rendererV2()
                            # load and apply style to circles layer
                            style_path = os.path.join( os.path.dirname(__file__), "ronds_style.qml" )
                            (errorMsg, result) = outputLayer.loadNamedStyle( style_path )
                            QgsMapLayerRegistry.instance().addMapLayer(outputLayer)

                        else :                                              # ...or save as a shapefile
                            shapefilename = self.dlg.circlesFileName.text()
                            error = QgsVectorFileWriter.writeAsVectorFormat(outputLayer, shapefilename, "CP1250", None, "ESRI Shapefile")

                            if self.dlg.addCanevas.isChecked():         # ...and add saved layer to the canevas
                                layername = os.path.splitext(os.path.basename(str(shapefilename)))[0]
                                loadedLayer = QgsVectorLayer(shapefilename, layername, "ogr")
                                # # customize style
                                rendererV2 = loadedLayer.rendererV2()
                                # load and apply style to legend
                                style_path = os.path.join( os.path.dirname(__file__), "ronds_style.qml" )
                                (errorMsg, result) = loadedLayer.loadNamedStyle( style_path )
                                QgsMapLayerRegistry.instance().addMapLayer(loadedLayer)    

                        # show scale and amount of missing values in the message bar
                        text1 = QtGui.QApplication.translate("ProportionalCircles","Proportional circles", None, QtGui.QApplication.UnicodeUTF8)
                        text2 = QtGui.QApplication.translate("ProportionalCircles","Missing value(s) : %d ; Max value : %d ; Max radius :  %d", None, QtGui.QApplication.UnicodeUTF8)  
                        iface.messageBar().pushMessage(text1, text2 %(missingValues, maximumValue, maximumRadius), level = QgsMessageBar.INFO, duration = 30)

                        # lengend

                        # coordinates of the legend
                        coeff = maximumRadius * (math.pi/maximumValue)**.5
                        maxRadiusLegend = coeff * (maximumValue/math.pi) ** .5  
                        xLegend = outputLayer.extent().xMaximum() + maxRadiusLegend
                        yLegend = (outputLayer.extent().yMinimum() + outputLayer.extent().yMaximum())*.5    

                        legendLayer = legendeRonds(crsString, (xLegend,yLegend), (maximumValue,maximumRadius), 'legende rond', nbSector, self.dlg.legendValuesList)

                        if self.dlg.memoryOutput.isChecked():           # ...add memory legend layer to the canevas
                            rendererV2 = legendLayer.rendererV2()
                            # load and apply style to circles layer
                            style_path = os.path.join( os.path.dirname(__file__), "legendeStyle.qml" )
                            (errorMsg, result) = legendLayer.loadNamedStyle( style_path )
                            QgsMapLayerRegistry.instance().addMapLayer(legendLayer)

                        else :                                              # ...or save as a shapefile
                            legendFilename = self.dlg.legendFileName.text()
                            error = QgsVectorFileWriter.writeAsVectorFormat(legendLayer, legendFilename, "CP1250", None, "ESRI Shapefile")

                            if self.dlg.addCanevas.isChecked():         # ...and add saved layer to the canevas
                                layername = os.path.splitext(os.path.basename(str(legendFilename)))[0]
                                loadedLayer = QgsVectorLayer(legendFilename, layername, "ogr")
                                # # customize style
                                rendererV2 = loadedLayer.rendererV2()
                                # load and apply style to legend
                                style_path = os.path.join( os.path.dirname(__file__), "legendeStyle.qml" )
                                (errorMsg, result) = loadedLayer.loadNamedStyle( style_path )
                                QgsMapLayerRegistry.instance().addMapLayer(loadedLayer)    


                                # QgsMapLayerRegistry.instance().addMapLayer(legendLayer)


                    else :                  # Warning message if resultLayer is empty...
                        iface.messageBar().pushMessage("Error", " No valid datas to represent" , level = QgsMessageBar.CRITICAL)


                finally :

                    # stop waitCursor
                    QApplication.restoreOverrideCursor()



