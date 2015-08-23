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
from ui_legendonly import Ui_LegendOnly

# Import the utilities from the fTools plugin (a standard QGIS plugin),
# which provide convenience functions for handling QGIS vector layers
import sys, os, imp
import fTools
path = os.path.dirname(fTools.__file__)
ftu = imp.load_source('ftools_utils', os.path.join(path,'tools','ftools_utils.py'))

from qgis.gui import QgsMessageBar
from qgis.utils import iface

# create the dialog for zoom to point

class LegendOnlyDialog(QtGui.QDialog, Ui_LegendOnly):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect

        self.selectedAttributesList = []
        self.setupUi(self)
        self.shapefileOutput.toggled.connect(self.radio_shapefile)
	self.buttonBox.rejected.connect(self.reject)
	# self.buttonBox.accepted.connect(self.accept)	
	self.buttonBox.accepted.connect(self.testSelectedOptions)	
        #QObject.connect(self.btnAdd, SIGNAL("clicked()"), self.onAdd)

        self.oldPath = ''
        self.selectFileName.clicked.connect(self.browse)


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
                    self.addCanevas.setEnabled(True)
                    self.legendFileName.setEnabled(True)
                    self.selectFileName.setEnabled(True)
                    self.addCanevas.setEnabled(True)
            else:
                    self.circlesFileName.setEnabled(False)
                    self.legendFileName.clear()
                    self.selectFileName.setEnabled(False)
                    self.addCanevas.setEnabled(False)


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

    def testSelectedOptions( self ):

        # list of custom radiuses for the circles in the legend
        legendCustomValues = self.legendCustomValues.text()
        legendCustomValues = legendCustomValues.strip().replace(';',' ')
        self.legendValuesList = legendCustomValues.split()

        try:			
            for i in range(len(self.legendValuesList)):  # custom values for the circles in the legend
	        self.legendValuesList[i] = float(self.legendValuesList[i])
                self.legendValuesList.sort()
            legendError = False
            
        except:   # if error in customisation -> automatic values for legend + warning message
            legendError = True
 
        if (self.shapefileOutput.isChecked() and self.circlesFileName.text() == '')  :
            QtGui.QMessageBox.warning(self, "ProportionalCircles", \
                QtGui.QApplication.translate("ProportionalCircles", \
                "Wrong or missing file name", None, QtGui.QApplication.UnicodeUTF8)) 

        elif (self.maxCustomValue.value() * self.maxCustomRadius.value() == 0):
            QtGui.QMessageBox.warning(self, "ProportionalCircles", \
                QtGui.QApplication.translate("ProportionalCircles", \
                "Radius and value cannot be equal to zero for a custom scale", None, QtGui.QApplication.UnicodeUTF8)) 

        elif legendError == True:
            QtGui.QMessageBox.warning(self, "ProportionalCircles", \
                QtGui.QApplication.translate("ProportionalCircles", \
                "Error in custom values for legend", None, QtGui.QApplication.UnicodeUTF8)) 

	else :

            self.accept()




