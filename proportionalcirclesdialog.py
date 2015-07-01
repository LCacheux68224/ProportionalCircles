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

# Import the utilities from the fTools plugin (a standard QGIS plugin),
# which provide convenience functions for handling QGIS vector layers
import sys, os, imp
import fTools
path = os.path.dirname(fTools.__file__)
ftu = imp.load_source('ftools_utils', os.path.join(path,'tools','ftools_utils.py'))


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
	self.buttonBox.rejected.connect(self.reject)
	self.buttonBox.accepted.connect(self.accept)	
        #QObject.connect(self.btnAdd, SIGNAL("clicked()"), self.onAdd)

        self.inputLayer.currentIndexChanged.connect(self.populateSelectedAttributes)
        self.inputLayer.currentIndexChanged.connect(self.populateAttributes)
        self.oldPath = ''
        self.selectFileName.clicked.connect(self.browse)
        self.btnAdd.clicked.connect(self.onAdd)
        self.btnRemove.clicked.connect(self.onRemove)

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



    def populateLayers( self ):
	self.inputLayer.clear()     #InputLayer
	self.analysisLayer.clear()  #ExtentLayer
        myListFonds = []
        myListContours = []
        myListFonds = ftu.getLayerNames( [ qgis.QGis.Polygon, qgis.QGis.Point ] )
        myListContours = ftu.getLayerNames( [ qgis.QGis.Polygon ] )
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
               if field.type() in (QtCore.QVariant.Double, QtCore.QVariant.Int)]
            # print fieldList
            self.availableAttributes.addItems(fieldList)


            
    def populateSelectedAttributes( self):

        layerName = self.inputLayer.currentText()
        self.selectedAttributes.clear()
        if layerName != "":         
            layer = qgis.QgsMapLayerRegistry.instance().mapLayersByName(layerName)[0]
            fieldList = [field.name()
               for field in list(layer.pendingFields().toList())
               if field.type() in (QtCore.QVariant.Double, QtCore.QVariant.Int)]
            # print fieldList
            self.selectedAttributes.addItems(self.selectedAttributesList)

    def browse( self ):

        fileName0 = QtGui.QFileDialog.getSaveFileName(self, 'Save as',
                                        self.oldPath, "Shapefile (*.shp);;All files (*)")
        fileName = os.path.splitext(str(fileName0))[0]+'.shp'
        if os.path.splitext(str(fileName0))[0] != '':
            self.oldPath = os.path.dirname(fileName)
        legendSuffix = QtGui.QApplication.translate("ProportionalCircles","_legend.shp", None, QtGui.QApplication.UnicodeUTF8)
        legendeFileName = os.path.splitext(str(fileName0))[0]+legendSuffix
        layername = os.path.splitext(os.path.basename(str(fileName)))[0]
        legendeLayerName = os.path.splitext(os.path.basename(str(legendeFileName)))[0]
        if (layername=='.shp'):
            return
        self.circlesFileName.setText(fileName)
        self.legendFileName.setText(legendeFileName)


