# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_proportionalcircles.ui'
#
# Created: Sun Jun 28 13:23:24 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ProportionalCircles(object):
    def setupUi(self, ProportionalCircles):
        ProportionalCircles.setObjectName(_fromUtf8("ProportionalCircles"))
        ProportionalCircles.resize(519, 828)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProportionalCircles.sizePolicy().hasHeightForWidth())
        ProportionalCircles.setSizePolicy(sizePolicy)
        ProportionalCircles.setMinimumSize(QtCore.QSize(519, 669))
        ProportionalCircles.setMaximumSize(QtCore.QSize(1000, 900))
        self.horizontalLayoutWidget_5 = QtGui.QWidget(ProportionalCircles)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(10, 780, 501, 41))
        self.horizontalLayoutWidget_5.setObjectName(_fromUtf8("horizontalLayoutWidget_5"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.buttonBox = QtGui.QDialogButtonBox(self.horizontalLayoutWidget_5)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_5.addWidget(self.buttonBox)
        self.frame = QtGui.QFrame(ProportionalCircles)
        self.frame.setGeometry(QtCore.QRect(10, 310, 501, 281))
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.frame)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 481, 147))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_6 = QtGui.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_2.addWidget(self.label_6)
        self.autoScale = QtGui.QRadioButton(self.verticalLayoutWidget_2)
        self.autoScale.setChecked(True)
        self.autoScale.setObjectName(_fromUtf8("autoScale"))
        self.verticalLayout_2.addWidget(self.autoScale)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_11 = QtGui.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_6.addWidget(self.label_11)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.analysisLayer = QtGui.QComboBox(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.analysisLayer.sizePolicy().hasHeightForWidth())
        self.analysisLayer.setSizePolicy(sizePolicy)
        self.analysisLayer.setObjectName(_fromUtf8("analysisLayer"))
        self.verticalLayout_8.addWidget(self.analysisLayer)
        self.horizontalLayout_6.addLayout(self.verticalLayout_8)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.customScale = QtGui.QRadioButton(self.verticalLayoutWidget_2)
        self.customScale.setObjectName(_fromUtf8("customScale"))
        self.verticalLayout_2.addWidget(self.customScale)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.label_4 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.label_4.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_11.addWidget(self.label_4)
        self.maxCustomRadius = QtGui.QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.maxCustomRadius.setEnabled(False)
        self.maxCustomRadius.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.maxCustomRadius.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.maxCustomRadius.setPrefix(_fromUtf8(""))
        self.maxCustomRadius.setDecimals(0)
        self.maxCustomRadius.setMaximum(999999999.0)
        self.maxCustomRadius.setObjectName(_fromUtf8("maxCustomRadius"))
        self.horizontalLayout_11.addWidget(self.maxCustomRadius)
        self.label_5 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.label_5.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_11.addWidget(self.label_5)
        self.maxCustomValue = QtGui.QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.maxCustomValue.setEnabled(False)
        self.maxCustomValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.maxCustomValue.setDecimals(3)
        self.maxCustomValue.setMaximum(999999999.0)
        self.maxCustomValue.setObjectName(_fromUtf8("maxCustomValue"))
        self.horizontalLayout_11.addWidget(self.maxCustomValue)
        self.verticalLayout_2.addLayout(self.horizontalLayout_11)
        self.line_4 = QtGui.QFrame(self.frame)
        self.line_4.setGeometry(QtCore.QRect(10, 160, 479, 3))
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.verticalLayoutWidget_5 = QtGui.QWidget(self.frame)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(10, 170, 481, 105))
        self.verticalLayoutWidget_5.setObjectName(_fromUtf8("verticalLayoutWidget_5"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_6.setMargin(0)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.label_7 = QtGui.QLabel(self.verticalLayoutWidget_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_6.addWidget(self.label_7)
        self.label_9 = QtGui.QLabel(self.verticalLayoutWidget_5)
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout_6.addWidget(self.label_9)
        self.legendCustomValues = QtGui.QLineEdit(self.verticalLayoutWidget_5)
        self.legendCustomValues.setObjectName(_fromUtf8("legendCustomValues"))
        self.verticalLayout_6.addWidget(self.legendCustomValues)
        self.onlyLegend = QtGui.QCheckBox(self.verticalLayoutWidget_5)
        self.onlyLegend.setEnabled(True)
        self.onlyLegend.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.onlyLegend.setChecked(False)
        self.onlyLegend.setObjectName(_fromUtf8("onlyLegend"))
        self.verticalLayout_6.addWidget(self.onlyLegend)
        self.frame_2 = QtGui.QFrame(ProportionalCircles)
        self.frame_2.setGeometry(QtCore.QRect(10, 600, 501, 171))
        self.frame_2.setFrameShape(QtGui.QFrame.Box)
        self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayoutWidget_3 = QtGui.QWidget(self.frame_2)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 481, 155))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_10 = QtGui.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout_3.addWidget(self.label_10)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.memoryOutput = QtGui.QRadioButton(self.verticalLayoutWidget_3)
        self.memoryOutput.setChecked(True)
        self.memoryOutput.setObjectName(_fromUtf8("memoryOutput"))
        self.horizontalLayout_4.addWidget(self.memoryOutput)
        self.shapefileOutput = QtGui.QRadioButton(self.verticalLayoutWidget_3)
        self.shapefileOutput.setChecked(False)
        self.shapefileOutput.setObjectName(_fromUtf8("shapefileOutput"))
        self.horizontalLayout_4.addWidget(self.shapefileOutput)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_3 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_3.setEnabled(False)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_5.addWidget(self.label_3)
        self.label_8 = QtGui.QLabel(self.verticalLayoutWidget_3)
        self.label_8.setEnabled(False)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_5.addWidget(self.label_8)
        self.horizontalLayout_8.addLayout(self.verticalLayout_5)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.circlesFileName = QtGui.QLineEdit(self.verticalLayoutWidget_3)
        self.circlesFileName.setEnabled(False)
        self.circlesFileName.setReadOnly(True)
        self.circlesFileName.setObjectName(_fromUtf8("circlesFileName"))
        self.horizontalLayout_3.addWidget(self.circlesFileName)
        self.selectFileName = QtGui.QToolButton(self.verticalLayoutWidget_3)
        self.selectFileName.setEnabled(False)
        self.selectFileName.setObjectName(_fromUtf8("selectFileName"))
        self.horizontalLayout_3.addWidget(self.selectFileName)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.legendFileName = QtGui.QLineEdit(self.verticalLayoutWidget_3)
        self.legendFileName.setEnabled(False)
        self.legendFileName.setReadOnly(True)
        self.legendFileName.setObjectName(_fromUtf8("legendFileName"))
        self.verticalLayout_4.addWidget(self.legendFileName)
        self.horizontalLayout_9.addLayout(self.verticalLayout_4)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_9)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.addCanevas = QtGui.QCheckBox(self.verticalLayoutWidget_3)
        self.addCanevas.setEnabled(False)
        self.addCanevas.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.addCanevas.setChecked(True)
        self.addCanevas.setObjectName(_fromUtf8("addCanevas"))
        self.verticalLayout_3.addWidget(self.addCanevas)
        self.frame_3 = QtGui.QFrame(ProportionalCircles)
        self.frame_3.setGeometry(QtCore.QRect(10, 10, 501, 291))
        self.frame_3.setFrameShape(QtGui.QFrame.Box)
        self.frame_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_3.setLineWidth(1)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.verticalLayoutWidget_8 = QtGui.QWidget(self.frame_3)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(10, 10, 481, 303))
        self.verticalLayoutWidget_8.setObjectName(_fromUtf8("verticalLayoutWidget_8"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.verticalLayoutWidget_8)
        self.verticalLayout_10.setSpacing(6)
        self.verticalLayout_10.setMargin(0)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_10.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.inputLayer = QtGui.QComboBox(self.verticalLayoutWidget_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputLayer.sizePolicy().hasHeightForWidth())
        self.inputLayer.setSizePolicy(sizePolicy)
        self.inputLayer.setToolTip(_fromUtf8(""))
        self.inputLayer.setWhatsThis(_fromUtf8(""))
        self.inputLayer.setObjectName(_fromUtf8("inputLayer"))
        self.horizontalLayout.addWidget(self.inputLayer)
        self.verticalLayout_10.addLayout(self.horizontalLayout)
        self.mAttributesGroupBox = QtGui.QGroupBox(self.verticalLayoutWidget_8)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mAttributesGroupBox.sizePolicy().hasHeightForWidth())
        self.mAttributesGroupBox.setSizePolicy(sizePolicy)
        self.mAttributesGroupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.mAttributesGroupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.mAttributesGroupBox.setObjectName(_fromUtf8("mAttributesGroupBox"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.mAttributesGroupBox)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.availAttributesLayout = QtGui.QVBoxLayout()
        self.availAttributesLayout.setObjectName(_fromUtf8("availAttributesLayout"))
        self.label_12 = QtGui.QLabel(self.mAttributesGroupBox)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.availAttributesLayout.addWidget(self.label_12)
        self.availableAttributes = QtGui.QListWidget(self.mAttributesGroupBox)
        self.availableAttributes.setObjectName(_fromUtf8("availableAttributes"))
        self.availAttributesLayout.addWidget(self.availableAttributes)
        self.horizontalLayout_7.addLayout(self.availAttributesLayout)
        self.attributeButtonLayout = QtGui.QVBoxLayout()
        self.attributeButtonLayout.setObjectName(_fromUtf8("attributeButtonLayout"))
        spacerItem3 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.attributeButtonLayout.addItem(spacerItem3)
        self.btnAdd = QtGui.QPushButton(self.mAttributesGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAdd.sizePolicy().hasHeightForWidth())
        self.btnAdd.setSizePolicy(sizePolicy)
        self.btnAdd.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/themes/default/symbologyAdd.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdd.setIcon(icon)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.attributeButtonLayout.addWidget(self.btnAdd)
        self.btnRemove = QtGui.QPushButton(self.mAttributesGroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRemove.sizePolicy().hasHeightForWidth())
        self.btnRemove.setSizePolicy(sizePolicy)
        self.btnRemove.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/themes/default/symbologyRemove.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRemove.setIcon(icon1)
        self.btnRemove.setObjectName(_fromUtf8("btnRemove"))
        self.attributeButtonLayout.addWidget(self.btnRemove)
        spacerItem4 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.attributeButtonLayout.addItem(spacerItem4)
        self.horizontalLayout_7.addLayout(self.attributeButtonLayout)
        self.assignedAttributesLayout = QtGui.QVBoxLayout()
        self.assignedAttributesLayout.setObjectName(_fromUtf8("assignedAttributesLayout"))
        self.Assigened = QtGui.QLabel(self.mAttributesGroupBox)
        self.Assigened.setObjectName(_fromUtf8("Assigened"))
        self.assignedAttributesLayout.addWidget(self.Assigened)
        self.selectedAttributes = QtGui.QListWidget(self.mAttributesGroupBox)
        self.selectedAttributes.setObjectName(_fromUtf8("selectedAttributes"))
        self.assignedAttributesLayout.addWidget(self.selectedAttributes)
        self.horizontalLayout_7.addLayout(self.assignedAttributesLayout)
        self.verticalLayout_10.addWidget(self.mAttributesGroupBox)
        self.selectedFeatures = QtGui.QCheckBox(self.verticalLayoutWidget_8)
        self.selectedFeatures.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.selectedFeatures.setObjectName(_fromUtf8("selectedFeatures"))
        self.verticalLayout_10.addWidget(self.selectedFeatures)

        self.retranslateUi(ProportionalCircles)
        QtCore.QMetaObject.connectSlotsByName(ProportionalCircles)

    def retranslateUi(self, ProportionalCircles):
        ProportionalCircles.setWindowTitle(_translate("ProportionalCircles", "Proportional circles", None))
        self.label_6.setText(_translate("ProportionalCircles", "Scale", None))
        self.autoScale.setText(_translate("ProportionalCircles", "Automatic  (proportional to the area of a reference polygon-layer)", None))
        self.label_11.setText(_translate("ProportionalCircles", "Reference layer", None))
        self.customScale.setText(_translate("ProportionalCircles", "Custom", None))
        self.label_4.setText(_translate("ProportionalCircles", "Radius (in meters)", None))
        self.label_5.setText(_translate("ProportionalCircles", "Value", None))
        self.label_7.setText(_translate("ProportionalCircles", "Custom values in the legend (automatic if empty)", None))
        self.label_9.setText(_translate("ProportionalCircles", "     (Example : 900;300;100)", None))
        self.onlyLegend.setText(_translate("ProportionalCircles", "create only the legend", None))
        self.label_10.setText(_translate("ProportionalCircles", "Output :", None))
        self.memoryOutput.setText(_translate("ProportionalCircles", "Memory", None))
        self.shapefileOutput.setText(_translate("ProportionalCircles", "Shapefile", None))
        self.label_3.setText(_translate("ProportionalCircles", "Circles", None))
        self.label_8.setText(_translate("ProportionalCircles", "Legend", None))
        self.selectFileName.setText(_translate("ProportionalCircles", "...", None))
        self.addCanevas.setText(_translate("ProportionalCircles", "add the layers to the canvas", None))
        self.label.setText(_translate("ProportionalCircles", "Layer", None))
        self.mAttributesGroupBox.setTitle(_translate("ProportionalCircles", "Values", None))
        self.label_12.setText(_translate("ProportionalCircles", "Available attributes", None))
        self.Assigened.setText(_translate("ProportionalCircles", "Selected attributes", None))
        self.selectedFeatures.setText(_translate("ProportionalCircles", "Extend the analysis to the hole layer (if selected features)", None))

