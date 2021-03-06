# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RondsProportionnelsDialog
                                 A QGIS plugin
 Proportional circles
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

from PyQt4 import QtCore, QtGui
import qgis.core as qgis
from ui_proportionalcircles import Ui_ProportionalCircles

import sys, os, imp

from qgis.gui import QgsMessageBar
from qgis.utils import iface

# create the dialog for zoom to point

class ProportionalCirclesDialog(QtGui.QDialog, Ui_ProportionalCircles):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect




        self.selectedAttributesList = []
        self.setupUi(self)
        self.autoScale.toggled.connect(self.radio_scale)
        self.shapefileOutput.toggled.connect(self.radio_shapefile)
        self.legendOnlyShapefileOutput.toggled.connect(self.legendOnlyRadio_shapefile)
	self.buttonBox.rejected.connect(self.reject)
	self.legendOnlyButtonBox.rejected.connect(self.reject)	
	self.buttonBox.accepted.connect(self.testSelectedOptions)	
	self.legendOnlyButtonBox.accepted.connect(self.legendOnlyTestSelectedOptions)
        #QObject.connect(self.btnAdd, SIGNAL("clicked()"), self.onAdd)

        self.inputLayer.currentIndexChanged.connect(self.populateSelectedAttributes)
        self.inputLayer.currentIndexChanged.connect(self.populateAttributes)
        self.oldPath = ''
        self.selectFileName.clicked.connect(self.browse)
        self.legendOnlySelectFileName.clicked.connect(self.legendOnlyBrowse)
        self.btnAdd.clicked.connect(self.onAdd)
        self.availableAttributes.doubleClicked.connect(self.onAdd)
        self.btnRemove.clicked.connect(self.onRemove)
        self.selectedAttributes.doubleClicked.connect(self.onRemove)

    def onAdd(self):
        selectedItem = self.availableAttributes.currentItem()
        if selectedItem is not None and selectedItem.text() not in self.selectedAttributesList:
            self.selectedAttributesList.append(selectedItem.text())
            self.populateSelectedAttributes()

    def onRemove(self):
	selectedItem = self.selectedAttributes.currentItem()
        if selectedItem is not None and selectedItem.text() in self.selectedAttributesList :
            self.selectedAttributesList.remove(selectedItem.text())
            self.populateSelectedAttributes()

    def  DeleteStyle(self):      
        self.listStyles.takeItem(self.listStyles.currentRow())
        delStyle(self.currentItem.text())
        StyleList = getStyleList()
        if len(StyleList)==0:
            self.Delete_btn.setEnabled(False)
            self.Activate_btn.setEnabled(False)
            self.currentItem = None 
        return

    def radio_scale(self):
            if self.autoScale.isChecked():
                    self.analysisLayer.setEnabled(True)
                    self.label_4.setEnabled(False)
                    self.label_5.setEnabled(False)
                    self.maxCustomRadius.setEnabled(False)
                    self.maxCustomValue.setEnabled(False)

            else:
                    self.analysisLayer.setEnabled(False)
                    self.label_4.setEnabled(True)
                    self.label_5.setEnabled(True)
                    self.maxCustomValue.setEnabled(True)
                    self.maxCustomRadius.setEnabled(True)

    def radio_shapefile(self):
            if self.shapefileOutput.isChecked():
                    self.label_3.setEnabled(True)
                    self.label_8.setEnabled(True)
                    self.addCanevas.setEnabled(True)
                    self.circlesFileName.setEnabled(True)
                    self.legendFileName.setEnabled(True)
                    self.selectFileName.setEnabled(True)

            else:
                    self.label_3.setEnabled(False)
                    self.label_8.setEnabled(False)
                    self.addCanevas.setEnabled(False)
                    self.circlesFileName.setEnabled(False)
                    self.legendFileName.setEnabled(False)
                    self.circlesFileName.clear()
                    self.legendFileName.clear()
                    self.selectFileName.setEnabled(False)

    def legendOnlyRadio_shapefile(self):
            if self.legendOnlyShapefileOutput.isChecked():
                    self.legendOnlyAddCanevas.setEnabled(True)
                    self.legendOnlyFileName.setEnabled(True)
                    self.legendOnlySelectFileName.setEnabled(True)
                    #self.addCanevas.setEnabled(True)
            else:
                    self.legendOnlyFileName.setEnabled(False)
                    self.legendOnlyFileName.clear()
                    self.legendOnlySelectFileName.setEnabled(False)
                    self.legendOnlyAddCanevas.setEnabled(False)

    def populateLayers( self ):
	self.inputLayer.clear()     #InputLayer
	self.analysisLayer.clear()  #ExtentLayer
        myListFonds = []
        myListContours = []
        for elem in qgis.QgsMapLayerRegistry.instance().mapLayers().values():
            if isinstance(elem, qgis.QgsVectorLayer) :
                if elem.geometryType() == qgis.QGis.Polygon:
                    myListContours.append(elem.name())
        # myListContours = [layer.name() for layer in qgis.QgsMapLayerRegistry.instance().mapLayers().values() if layer.geometryType() == qgis.QGis.Polygon ]

        for elem in qgis.QgsMapLayerRegistry.instance().mapLayers().values():
            if isinstance(elem, qgis.QgsVectorLayer) :
                if elem.geometryType() in (qgis.QGis.Point, qgis.QGis.Polygon):
                    myListFonds.append(elem.name())
        # myListFonds = [layer.name() for layer in qgis.QgsMapLayerRegistry.instance().mapLayers().values() if layer.geometryType() in (qgis.QGis.Point, qgis.QGis.Polygon)]

        self.inputLayer.addItems( myListFonds )
        self.analysisLayer.addItems( myListContours )

  

    def populateAttributes( self ):

        layerName = self.inputLayer.currentText()
        self.availableAttributes.clear()
        self.selectedAttributesList = []
        self.selectedAttributes.clear()
        if layerName != "":         
            layer = qgis.QgsMapLayerRegistry.instance().mapLayersByName(layerName)[0]
            fieldList = [field.name()
               for field in list(layer.pendingFields().toList())
               if field.type() in (QtCore.QVariant.Double, QtCore.QVariant.Int, QtCore.QVariant.UInt, QtCore.QVariant.LongLong, QtCore.QVariant.ULongLong)]
            # print fieldList
            self.availableAttributes.addItems(fieldList)


            
    def populateSelectedAttributes( self):

        layerName = self.inputLayer.currentText()
        self.selectedAttributes.clear()
        if layerName != "":         
            layer = qgis.QgsMapLayerRegistry.instance().mapLayersByName(layerName)[0]
            fieldList = [field.name()
               for field in list(layer.pendingFields().toList())
               if field.type() in (QtCore.QVariant.Double, QtCore.QVariant.Int, QtCore.QVariant.UInt, QtCore.QVariant.LongLong, QtCore.QVariant.ULongLong)]
            # print fieldList
            self.selectedAttributes.addItems(self.selectedAttributesList)

    def browse( self ):

        fileName0 = QtGui.QFileDialog.getSaveFileName(self, 'Save as',
                                        self.oldPath, "Shapefile (*.shp);;All files (*)")
        fileName = os.path.splitext(fileName0)[0]+ u'.shp'
        if os.path.splitext(fileName0)[0] != '':
            self.oldPath = os.path.dirname(fileName)
        legendSuffix = QtGui.QApplication.translate("ProportionalCircles","_legend.shp", None, QtGui.QApplication.UnicodeUTF8)
        legendeFileName = os.path.splitext(fileName0)[0]+legendSuffix
        layername = os.path.splitext(os.path.basename(fileName))[0]
        legendeLayerName = os.path.splitext(os.path.basename(legendeFileName))[0]
        if (layername=='.shp'):
            return
        self.circlesFileName.setText(fileName)
        self.legendFileName.setText(legendeFileName)

    def legendOnlyBrowse( self ):

        fileName0 = QtGui.QFileDialog.getSaveFileName(self, 'Save as',
                                        self.oldPath, "Shapefile (*.shp);;All files (*)")
                                     
        legendOnlyFileName = os.path.splitext(fileName0)[0]+ u'.shp' # QtGui.QApplication.translate("ProportionalCircles",".shp", None, QtGui.QApplication.UnicodeUTF8)  #'.shp'
        if os.path.splitext(fileName0)[0] != '':
            self.oldPath = os.path.dirname(legendOnlyFileName)
        # legendOnlyFileName = os.path.splitext(str(fileName0))[0]
        legendOnlyLayername = os.path.splitext(os.path.basename(legendOnlyFileName))[0]
        if (legendOnlyLayername=='.shp'):
            return
        self.legendOnlyFileName.setText(legendOnlyFileName)

    def testSelectedOptions( self ):

        # list of custom radiuses for the circles in the legend
        legendCustomValues = self.legendCustomValues.text()
        legendCustomValues = legendCustomValues.strip().replace(';',' ')
        self.legendValuesList = legendCustomValues.split()
        if len(self.legendValuesList) == 0:  # automatic VALUES for the circles in the legend 
            legendError = False
            self.legendValuesList = []
        else:
            try:			
	       for i in range(len(self.legendValuesList)):  # custom values for the circles in the legend
	           self.legendValuesList[i] = float(self.legendValuesList[i])
                   self.legendValuesList.sort()
                   legendError = False
            except:   # if error in customisation -> automatic values for legend + warning message
                legendError = True

	if len(self.selectedAttributesList) < 1:
            QtGui.QMessageBox.warning(self, "ProportionalCircles", \
                QtGui.QApplication.translate("ProportionalCircles", \
                "Please select at least one an attribute", None, QtGui.QApplication.UnicodeUTF8))
 
        elif (self.shapefileOutput.isChecked() and self.circlesFileName.text() == '')  :
            QtGui.QMessageBox.warning(self, "ProportionalCircles", \
                QtGui.QApplication.translate("ProportionalCircles", \
                "Wrong or missing file name", None, QtGui.QApplication.UnicodeUTF8)) 

        elif (self.customScale.isChecked() and self.maxCustomValue.value() * self.maxCustomRadius.value() == 0):
            QtGui.QMessageBox.warning(self, "ProportionalCircles", \
                QtGui.QApplication.translate("ProportionalCircles", \
                "Radius and value cannot be equal to zero for a custom scale", None, QtGui.QApplication.UnicodeUTF8)) 

        elif legendError:
            QtGui.QMessageBox.warning(self, "ProportionalCircles", \
                QtGui.QApplication.translate("ProportionalCircles", \
                "Error in custom values for legend", None, QtGui.QApplication.UnicodeUTF8)) 


            #elif qgis.QgsMapLayerRegistry.instance().mapLayersByName(self.analysisLayer.currentText())[0].featureCount() == 0 and self.autoScale.isChecked() :
        elif qgis.QgsMapLayerRegistry.instance().mapLayersByName(self.analysisLayer.currentText()) is None and self.autoScale.isChecked() :
            QtGui.QMessageBox.warning(self, "ProportionalCircles", \
            QtGui.QApplication.translate("ProportionalCircles", \
                "Empty polygon layer", None, QtGui.QApplication.UnicodeUTF8)) 

        else :
            self.legendOnly = False
            self.accept()

    def legendOnlyTestSelectedOptions( self ):


        # list of custom radiuses for the circles in the legend
        legendOnlyCustomValues = self.legendOnlyCustomValues.text()
        legendOnlyCustomValues = legendOnlyCustomValues.strip().replace(';',' ')
        self.legendOnlyValuesList = legendOnlyCustomValues.split()
        if len(self.legendOnlyValuesList) == 0:  # automatic VALUES for the circles in the legend 
            legendError = False
            self.legendOnlyValuesList = []
        else:
            try:			
	       for i in range(len(self.legendOnlyValuesList)):  # custom values for the circles in the legend
	           self.legendOnlyValuesList[i] = float(self.legendOnlyValuesList[i])
                   self.legendOnlyValuesList.sort()
                   legendError = False
            except:   # if error in customisation -> automatic values for legend + warning message
                legendError = True

 
        if (self.legendOnlyShapefileOutput.isChecked() and self.legendOnlyFileName.text() == '')  :
            QtGui.QMessageBox.warning(self, "ProportionalCircles", \
                QtGui.QApplication.translate("ProportionalCircles", \
                "Wrong or missing file name", None, QtGui.QApplication.UnicodeUTF8)) 

        elif self.legendOnlyMaxCustomValue.value() * self.legendOnlyMaxCustomRadius.value() == 0 :
            QtGui.QMessageBox.warning(self, "ProportionalCircles", \
                QtGui.QApplication.translate("ProportionalCircles", \
                "Radius and value cannot be equal to zero for a custom scale", None, QtGui.QApplication.UnicodeUTF8)) 

        elif legendError:
            QtGui.QMessageBox.warning(self, "ProportionalCircles", \
                QtGui.QApplication.translate("ProportionalCircles", \
                "Error in custom values for legend", None, QtGui.QApplication.UnicodeUTF8)) 

	else :
            self.legendOnly = True
            self.accept()




