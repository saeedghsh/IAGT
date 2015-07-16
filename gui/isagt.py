# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'isagt.ui'
#
# Created: Thu Jul 16 07:44:22 2015
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(1263, 958)
        MainWindow.setMouseTracking(True)
        MainWindow.setAcceptDrops(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loadButton = QtGui.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(10, 10, 111, 31))
        self.loadButton.setObjectName("loadButton")
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 100, 931, 741))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setObjectName("graphicsView")
        self.loadYaml = QtGui.QRadioButton(self.centralwidget)
        self.loadYaml.setGeometry(QtCore.QRect(320, 10, 191, 31))
        self.loadYaml.setChecked(True)
        self.loadYaml.setAutoExclusive(False)
        self.loadYaml.setObjectName("loadYaml")
        self.textAddress = QtGui.QTextBrowser(self.centralwidget)
        self.textAddress.setGeometry(QtCore.QRect(260, 60, 681, 31))
        self.textAddress.setObjectName("textAddress")
        self.loadOption = QtGui.QComboBox(self.centralwidget)
        self.loadOption.setGeometry(QtCore.QRect(130, 10, 131, 31))
        self.loadOption.setAutoFillBackground(False)
        self.loadOption.setObjectName("loadOption")
        self.loadOption.addItem("")
        self.loadOption.addItem("")
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 40, 1241, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.displayAnnotation = QtGui.QRadioButton(self.centralwidget)
        self.displayAnnotation.setGeometry(QtCore.QRect(10, 60, 181, 31))
        self.displayAnnotation.setChecked(True)
        self.displayAnnotation.setAutoExclusive(False)
        self.displayAnnotation.setObjectName("displayAnnotation")
        self.groupCategory = QtGui.QGroupBox(self.centralwidget)
        self.groupCategory.setEnabled(False)
        self.groupCategory.setGeometry(QtCore.QRect(10, 850, 271, 41))
        self.groupCategory.setObjectName("groupCategory")
        self.catPoly = QtGui.QCheckBox(self.groupCategory)
        self.catPoly.setGeometry(QtCore.QRect(80, 0, 97, 22))
        self.catPoly.setChecked(True)
        self.catPoly.setAutoExclusive(True)
        self.catPoly.setObjectName("catPoly")
        self.catConstellation = QtGui.QCheckBox(self.groupCategory)
        self.catConstellation.setGeometry(QtCore.QRect(80, 20, 121, 22))
        self.catConstellation.setAutoExclusive(True)
        self.catConstellation.setObjectName("catConstellation")
        self.catLine = QtGui.QCheckBox(self.groupCategory)
        self.catLine.setGeometry(QtCore.QRect(200, 20, 71, 22))
        self.catLine.setAutoExclusive(True)
        self.catLine.setObjectName("catLine")
        self.catCircle = QtGui.QCheckBox(self.groupCategory)
        self.catCircle.setGeometry(QtCore.QRect(200, 0, 71, 22))
        self.catCircle.setAutoExclusive(True)
        self.catCircle.setObjectName("catCircle")
        self.groupNavigation = QtGui.QGroupBox(self.centralwidget)
        self.groupNavigation.setEnabled(False)
        self.groupNavigation.setGeometry(QtCore.QRect(350, 850, 291, 61))
        self.groupNavigation.setObjectName("groupNavigation")
        self.navPrev = QtGui.QPushButton(self.groupNavigation)
        self.navPrev.setGeometry(QtCore.QRect(90, 0, 98, 27))
        self.navPrev.setObjectName("navPrev")
        self.navNext = QtGui.QPushButton(self.groupNavigation)
        self.navNext.setGeometry(QtCore.QRect(190, 0, 98, 27))
        self.navNext.setObjectName("navNext")
        self.navGoto = QtGui.QPushButton(self.groupNavigation)
        self.navGoto.setGeometry(QtCore.QRect(90, 30, 98, 27))
        self.navGoto.setObjectName("navGoto")
        self.navigationCounter = QtGui.QTextEdit(self.groupNavigation)
        self.navigationCounter.setGeometry(QtCore.QRect(190, 30, 101, 31))
        self.navigationCounter.setObjectName("navigationCounter")
        self.groupAnnotation = QtGui.QGroupBox(self.centralwidget)
        self.groupAnnotation.setEnabled(False)
        self.groupAnnotation.setGeometry(QtCore.QRect(710, 850, 191, 61))
        self.groupAnnotation.setObjectName("groupAnnotation")
        self.annotateReset = QtGui.QPushButton(self.groupAnnotation)
        self.annotateReset.setGeometry(QtCore.QRect(90, 30, 98, 27))
        self.annotateReset.setObjectName("annotateReset")
        self.annotateAdd = QtGui.QPushButton(self.groupAnnotation)
        self.annotateAdd.setGeometry(QtCore.QRect(90, 0, 98, 27))
        self.annotateAdd.setObjectName("annotateAdd")
        self.line_3 = QtGui.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(670, 840, 20, 71))
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtGui.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(300, 840, 20, 71))
        self.line_4.setFrameShape(QtGui.QFrame.VLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.groupAnnotationList = QtGui.QGroupBox(self.centralwidget)
        self.groupAnnotationList.setEnabled(False)
        self.groupAnnotationList.setGeometry(QtCore.QRect(960, 60, 301, 831))
        self.groupAnnotationList.setObjectName("groupAnnotationList")
        self.annotationList = QtGui.QListWidget(self.groupAnnotationList)
        self.annotationList.setGeometry(QtCore.QRect(0, 20, 291, 401))
        self.annotationList.setObjectName("annotationList")
        self.annotationRemove = QtGui.QPushButton(self.groupAnnotationList)
        self.annotationRemove.setGeometry(QtCore.QRect(0, 430, 291, 27))
        self.annotationRemove.setObjectName("annotationRemove")
        self.groupAnnotationID = QtGui.QGroupBox(self.groupAnnotationList)
        self.groupAnnotationID.setGeometry(QtCore.QRect(10, 460, 281, 91))
        self.groupAnnotationID.setObjectName("groupAnnotationID")
        self.annotationIDtext = QtGui.QPlainTextEdit(self.groupAnnotationID)
        self.annotationIDtext.setGeometry(QtCore.QRect(0, 20, 271, 31))
        self.annotationIDtext.setObjectName("annotationIDtext")
        self.annotationIdAdd = QtGui.QPushButton(self.groupAnnotationID)
        self.annotationIdAdd.setGeometry(QtCore.QRect(10, 60, 121, 27))
        self.annotationIdAdd.setObjectName("annotationIdAdd")
        self.annotationIdDelete = QtGui.QPushButton(self.groupAnnotationID)
        self.annotationIdDelete.setGeometry(QtCore.QRect(147, 60, 121, 27))
        self.annotationIdDelete.setObjectName("annotationIdDelete")
        self.line_5 = QtGui.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(940, 60, 20, 841))
        self.line_5.setFrameShape(QtGui.QFrame.VLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.aboutButton = QtGui.QPushButton(self.centralwidget)
        self.aboutButton.setGeometry(QtCore.QRect(1150, 10, 98, 27))
        self.aboutButton.setObjectName("aboutButton")
        self.unwrapOption = QtGui.QComboBox(self.centralwidget)
        self.unwrapOption.setEnabled(False)
        self.unwrapOption.setGeometry(QtCore.QRect(700, 10, 171, 31))
        self.unwrapOption.setObjectName("unwrapOption")
        self.unwrapOption.addItem("")
        self.unwrapOption.addItem("")
        self.unwrapOption.addItem("")
        self.unwrapFlag = QtGui.QRadioButton(self.centralwidget)
        self.unwrapFlag.setEnabled(False)
        self.unwrapFlag.setGeometry(QtCore.QRect(560, 10, 151, 31))
        self.unwrapFlag.setChecked(False)
        self.unwrapFlag.setAutoExclusive(False)
        self.unwrapFlag.setObjectName("unwrapFlag")
        self.AdvanceOptionS = QtGui.QPushButton(self.centralwidget)
        self.AdvanceOptionS.setEnabled(False)
        self.AdvanceOptionS.setGeometry(QtCore.QRect(897, 10, 161, 27))
        self.AdvanceOptionS.setObjectName("AdvanceOptionS")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1263, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.loadOption.setCurrentIndex(0)
        self.unwrapOption.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Image Annotation for Ground Truth", None, QtGui.QApplication.UnicodeUTF8))
        self.loadButton.setText(QtGui.QApplication.translate("MainWindow", "Load Image(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.loadYaml.setText(QtGui.QApplication.translate("MainWindow", "Load YAML file (if exists)", None, QtGui.QApplication.UnicodeUTF8))
        self.loadOption.setItemText(0, QtGui.QApplication.translate("MainWindow", "Folder", None, QtGui.QApplication.UnicodeUTF8))
        self.loadOption.setItemText(1, QtGui.QApplication.translate("MainWindow", "Single File", None, QtGui.QApplication.UnicodeUTF8))
        self.displayAnnotation.setText(QtGui.QApplication.translate("MainWindow", "Display all annotations", None, QtGui.QApplication.UnicodeUTF8))
        self.groupCategory.setTitle(QtGui.QApplication.translate("MainWindow", "Category:", None, QtGui.QApplication.UnicodeUTF8))
        self.catPoly.setText(QtGui.QApplication.translate("MainWindow", "Polygon", None, QtGui.QApplication.UnicodeUTF8))
        self.catConstellation.setText(QtGui.QApplication.translate("MainWindow", "Constellation", None, QtGui.QApplication.UnicodeUTF8))
        self.catLine.setText(QtGui.QApplication.translate("MainWindow", "Line", None, QtGui.QApplication.UnicodeUTF8))
        self.catCircle.setText(QtGui.QApplication.translate("MainWindow", "Circle", None, QtGui.QApplication.UnicodeUTF8))
        self.groupNavigation.setTitle(QtGui.QApplication.translate("MainWindow", "Navigation:", None, QtGui.QApplication.UnicodeUTF8))
        self.navPrev.setText(QtGui.QApplication.translate("MainWindow", "Previous", None, QtGui.QApplication.UnicodeUTF8))
        self.navNext.setText(QtGui.QApplication.translate("MainWindow", "Next", None, QtGui.QApplication.UnicodeUTF8))
        self.navGoto.setText(QtGui.QApplication.translate("MainWindow", "Go To", None, QtGui.QApplication.UnicodeUTF8))
        self.groupAnnotation.setTitle(QtGui.QApplication.translate("MainWindow", "Annotation:", None, QtGui.QApplication.UnicodeUTF8))
        self.annotateReset.setText(QtGui.QApplication.translate("MainWindow", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.annotateAdd.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.groupAnnotationList.setTitle(QtGui.QApplication.translate("MainWindow", "Annotations:", None, QtGui.QApplication.UnicodeUTF8))
        self.annotationRemove.setText(QtGui.QApplication.translate("MainWindow", "Remove selected annotation", None, QtGui.QApplication.UnicodeUTF8))
        self.groupAnnotationID.setTitle(QtGui.QApplication.translate("MainWindow", "Identity:", None, QtGui.QApplication.UnicodeUTF8))
        self.annotationIdAdd.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.annotationIdDelete.setText(QtGui.QApplication.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutButton.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.unwrapOption.setItemText(0, QtGui.QApplication.translate("MainWindow", "Fisheye - Downward", None, QtGui.QApplication.UnicodeUTF8))
        self.unwrapOption.setItemText(1, QtGui.QApplication.translate("MainWindow", "Fisheye - Forward", None, QtGui.QApplication.UnicodeUTF8))
        self.unwrapOption.setItemText(2, QtGui.QApplication.translate("MainWindow", "OminCam", None, QtGui.QApplication.UnicodeUTF8))
        self.unwrapFlag.setText(QtGui.QApplication.translate("MainWindow", "Unrwap image(s)", None, QtGui.QApplication.UnicodeUTF8))
        self.AdvanceOptionS.setText(QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))

