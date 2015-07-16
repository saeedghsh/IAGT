# "
# Copyright (C) 2015 Saeed Gholami Shahbandi. All rights reserved.

# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this program. If not, see
# <http://www.gnu.org/licenses/>
# "

import sys, os, platform, time

import numpy as np
from numpy.linalg import det

import cv2
import yaml

import PySide
from PySide import QtCore, QtGui

sys.path.append('../gui/')
import isagt # isagt.Ui_MainWindow
import myCanvasLib as MCL
reload(MCL)


class MainWindow(QtGui.QMainWindow, isagt.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = isagt.Ui_MainWindow()
        self.ui.setupUi(self)

        ## Matplotlib Setting
        self.main_widget = self.ui.graphicsView #QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout(self.main_widget)
        self.myCanvas = MCL.MyMplCanvas(self.main_widget)#, width=5, height=4, dpi=100)
        self.layout.addWidget(self.myCanvas)
        self.main_widget.setFocus()
        # self.setCentralWidget(self.main_widget)
        self.myCanvas.mpl_connect('button_press_event', self.mouseClick)
        
        ## Push buttons
        self.ui.loadButton.clicked.connect(self.loadFileLists)
        self.ui.aboutButton.clicked.connect(self.about)
        self.ui.navGoto.clicked.connect(self.navGoTo)
        self.ui.navNext.clicked.connect(self.navNext)
        self.ui.navPrev.clicked.connect(self.navPrev)
        self.ui.annotateAdd.clicked.connect(self.grabAnnotation)
        self.ui.annotateReset.clicked.connect(self.resetAnnotation)
        self.ui.annotationRemove.clicked.connect(self.annotationRemove)
        ## Radio buttons
        self.ui.loadYaml.toggled.connect(self.startNewImage)
        self.ui.unwrapFlag.toggled.connect(self.startNewImage)
        self.ui.displayAnnotation.toggled.connect(self.startNewImage)

        ## 
        self.yamlList, self.imagList = None, None
        self.sorting = True

    #########################################################################
    ############################ Loading Stage ##############################
    #########################################################################
    def loadFileLists(self):
        self.path = []
        # Loading file(s) name(s)
        if self.ui.loadOption.currentText() == 'Folder':
            self.path = QtGui.QFileDialog.getExistingDirectory()
            content = [ f for f in os.listdir(self.path)
                        if os.path.isfile(os.path.join(self.path,f)) ]
            filesNames = [os.path.join(self.path,f) for f in content]

        elif self.ui.loadOption.currentText() == 'Single File':
            filesNames = QtGui.QFileDialog.getOpenFileName()

        # sort file names into yamls and images
        # remove empty strings and none image files
        yamlFormats = ['yaml', 'YAML', 'Yaml']
        imagFormats = ['.png', '.PNG', '.jpg', '.JPG', 'JPEG', 'jpeg', '.bmp']
        yamlList, imagList = [], []
        for i in range(len(filesNames)-1,-1,-1):
            if len(filesNames[i]) == 0:
                pass #filesNames.pop(i)
            elif filesNames[i][-4:] in yamlFormats:
                yamlList.append(filesNames[i])
            elif filesNames[i][-4:] in imagFormats:
                imagList.append(filesNames[i])

        # if there is amy image loaded        
        if len(imagList) > 0:
            # enabling buttons
            self.ui.groupCategory.setEnabled(True)
            self.ui.groupNavigation.setEnabled(True)
            self.ui.groupAnnotation.setEnabled(True)
            self.ui.groupAnnotationList.setEnabled(True)
            self.ui.groupAnnotationID.setEnabled(True)
            self.ui.annotationList

            # loading fileLists
            yamlList.sort(), imagList.sort()
            self.imagList = imagList
            self.imagIndx = 0
            self.yamlList = yamlList 

            self.startNewImage()
            
    def loadYamlLists(self):
        if len(self.path) > 0:
            content = [ f for f in os.listdir(self.path)
                        if os.path.isfile(os.path.join(self.path,f)) ]
            filesNames = [os.path.join(self.path,f) for f in content]

        # sort file names into yamls and images
        # remove empty strings and none image files
        yamlList = []
        yamlFormats = ['yaml', 'YAML', 'Yaml']
        for i in range(len(filesNames)-1,-1,-1):
            if len(filesNames[i]) == 0:
                pass #filesNames.pop(i)
            elif filesNames[i][-4:] in yamlFormats:
                yamlList.append(filesNames[i])

        yamlList.sort()
        self.yamlList = yamlList

    def startNewImage(self):
        
        self.circ, self.poly, self.line, self.cons =[],[],[],[]

        ### setting navigation counter
        self.ui.textAddress.setText(self.imagList[self.imagIndx])
        self.ui.navigationCounter.setText(str(self.imagIndx+1)+'/'+str(len(self.imagList)))
        
        ### plotting the image
        image = cv2.imread(self.imagList[self.imagIndx])
        if self.ui.unwrapFlag.isChecked():
            if self.ui.unwrapOption.currentText() == 'Fisheye - Downward':
                pass # unrwape image
            elif self.ui.unwrapOption.currentText() == 'Fisheye - Forward':
                pass # unrwape image
            elif self.ui.unwrapOption.currentText() == 'OminCam':
                pass # unrwape image
        else:
            self.image = image
        self.myCanvas.plotImage(self.image)        

        ### Loading Yaml file
        if self.ui.loadYaml.isChecked():
           self.loadYamlFile()

        ### update 
        self.updateAnnotationList()        

        ### plot available annotations
        if self.ui.displayAnnotation.isChecked():
            self.plotAllAnnotations()
        ### initializing-emptying the temp list
        self.resetAnnotation() # => self.temp = []
        
        
    def loadYamlFile(self):
        self.yamlIndx =  None
        imagName = self.imagList[self.imagIndx].split('/')[-1]
        imagName = imagName.split('.')[0]
        for idx in range(len(self.yamlList)):
            yamlName = self.yamlList[idx].split('/')[-1]
            yamlName = yamlName.split('.')[0]
            if yamlName == imagName:
                self.yamlIndx = idx
                break

        if self.yamlIndx is not None:
            data = yaml.load(open(self.yamlList[self.yamlIndx], 'r'))
            #checks if there is any annotation
            if 'annotations' in data.keys():
                #checks if the annotation is not empty
                if data['annotations'] is not None:
                    self.circ, self.poly, self.line, self.cons = self.parseYaml(data)
        else:
            print "yaml not found"

    def parseYaml(self, data):
        ann = data['annotations']
        cir, pol, lin, con = [],[],[],[]
        for i in range(len(ann)):
            # removing none point keys
            keys , p = ann[i].keys() , []

            while 'category' in keys: keys.remove('category')
            while 'id' in keys: keys.remove('id')

            if ann[i]['category'] == 'circle':
                # cir = [ [cx1,cy1,r1], [cx2,cy2,r2], ... ]
                c = [float(s) for s in ann[i]['cen'].split()
                     if s.replace(".", "", 1).isdigit()]
                cir.append([ c[0],c[1] , float(ann[i]['rad']) ])

            elif ann[i]['category'] == 'polygon':
                # pol = [ [[px1,py1], [px2,py2], ...] , ...]
                for k in keys: p.append( [float(s) for s in ann[i][k].split()
                                          if s.replace(".", "", 1).isdigit()] )
                if self.sorting ==True:
                    pol.append(self.sortPointsCCW(p))
                else:
                    pol.append(p)

            elif ann[i]['category'] == 'line':
                # lin = [ [[px1,py1], [px2,py2]] , ...]
                for k in keys: p.append( [float(s) for s in ann[i][k].split()
                                          if s.replace(".", "", 1).isdigit()] )
                lin.append(p)

            elif ann[i]['category'] == 'constellation':
                # con = [ [[px1,py1], [px2,py2], ...] , ...]
                for k in keys: p.append( [float(s) for s in ann[i][k].split()
                                          if s.replace(".", "", 1).isdigit()] )
                con.append(p)

            else:
                print "unknown category"
        return cir, pol, lin, con


            
    #########################################################################
    ############################# Annotations ###############################
    #########################################################################
    def mouseClick(self, event):
        # print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        #     event.button, event.x, event.y, event.xdata, event.ydata)
        self.temp.append([event.xdata, event.ydata])

        # drawing temp points
        self.myCanvas.plotCons([[event.xdata, event.ydata]], symbolID=4)
        
        if event.button == 2:
            print 'I could wrap up everything here, right?'
            # self.grabAnnotation()
        
    def grabAnnotation(self):        
        if self.ui.catPoly.isChecked():
            if self.sorting == True:
                self.poly.append( self.sortPointsCCW(self.temp) )
            else:
                self.poly.append( self.temp )
            self.plotAnnotations(poly=self.poly[-1], polyIdx=len(self.poly))

        elif self.ui.catConstellation.isChecked():
            self.cons.append(self.temp)
            self.plotAnnotations(cons=self.cons[-1], consIdx=len(self.cons))

        elif self.ui.catLine.isChecked():
            self.line.append(self.temp)
            self.plotAnnotations(line=self.line[-1], lineIdx=len(self.line))

        elif self.ui.catCircle.isChecked():
            if len(self.temp) == 2:
                # if 2 points are given, the 1st is the center and 2nd is on the perimeter
                [x0,y0] , [x1,y1] = self.temp[0] , self.temp[1]
                r = np.sqrt( (x0-x1)**2 + (y0-y1)**2 )                
            elif len(self.temp) > 2:
                # if 3 points are given, they are all considered on the perimeter
                # http://mathworld.wolfram.com/Circle.html
                [x1,y1], [x2,y2], [x3,y3] = self.temp[0] , self.temp[1], self.temp[2]
                a = np.array([ [x1,y1,1], [x2,y2,1], [x3,y3,1] ])
                d = np.array([ [x1**2+y1**2,y1,1], [x2**2+y2**2,y2,1], [x3**2+y3**2,y3,1] ])
                e = np.array([ [x1**2+y1**2,x1,1], [x2**2+y2**2,x2,1], [x3**2+y3**2,x3,1] ])
                f = np.array([ [x1**2+y1**2,x1,y1], [x2**2+y2**2,x2,y2], [x3**2+y3**2,x3,y3] ])
                a,d,e,f = det(a), -det(d), det(e), -det(f)
                x0, y0 = -d/(2*a) , -e/(2*a)
                r = np.sqrt( ((d**2 + e**2)/ (4*(a**2))) - (f/a))
            
            self.circ.append([x0,y0,r])
            self.plotAnnotations(circ=self.circ[-1], circIdx=len(self.circ))

        self.resetAnnotation() # => self.temp = []
        self.updateAnnotationList()
        self.resetDrawing()
        
    def updateAnnotationList (self):
        self.ui.annotationList.clear()
        
        idx = 0
        for (obj,i) in zip(self.circ, range(len(self.circ))):
            string =  'circle#'+str(i)# +': '
            # string = string + ' c=('+str(obj[0])+','+str(obj[1])+') , r='+str(obj[2])
            self.ui.annotationList.insertItem(idx, string)
            idx=+1

        for (obj,i) in zip(self.poly,range(len(self.poly))):
            string = 'polygon#' + str(i) + ': ' + str(len(obj)) + ' points'
            self.ui.annotationList.insertItem(idx, string)
            idx=+1
                           
        for (obj,i) in zip(self.line,range(len(self.line))):
            string =  'line#' + str(i)# +': '
            # string = string + 'p1(' + str(obj[0][0]) + ',' + str(obj[0][1])
            # string = string + 'p2(' + str(obj[1][0]) + ',' + str(obj[1][1])
            self.ui.annotationList.insertItem(idx, string)
            idx=+1

        for (obj,i) in zip(self.cons,range(len(self.cons))):
            string = 'constalation#' + str(i) + ': ' + str(len(obj)) + ' points'
            self.ui.annotationList.insertItem(idx, string)
            idx=+1
            
        self.ui.annotationList.sortItems()

    def annotationRemove(self):
        # idx = self.ui.annotationList.currentRow()        
        listItem = self.ui.annotationList.currentItem()
        text = listItem.text()
        idx = int(text[text.find('#')+1 : text.find(':')])
        
        if text[:4] == 'circ':
            self.circ.pop(idx)
        elif text[:4] == 'poly':
            self.poly.pop(idx)
        elif text[:4] == 'line':
            self.line.pop(idx)
        elif text[:4] == 'cons':
            self.cons.pop(idx)

        self.updateAnnotationList()
        self.resetDrawing()

    def resetDrawing(self):
        self.myCanvas.axes.cla()
        self.myCanvas.plotImage(self.image)
        if self.ui.displayAnnotation.isChecked():
            self.plotAllAnnotations()
            
    def resetAnnotation(self):
        self.temp = []

    def plotAllAnnotations(self):
        for idx in range(len(self.circ)): self.myCanvas.plotCirc(self.circ[idx],idx)
        for idx in range(len(self.poly)): self.myCanvas.plotPoly(self.poly[idx],idx)
        for idx in range(len(self.line)): self.myCanvas.plotLine(self.line[idx],idx)
        for idx in range(len(self.cons)): self.myCanvas.plotCons(self.cons[idx],idx)

    def plotAnnotations(self,
                        circ=None,circIdx=None , poly=None,polyIdx=None,
                        line=None,lineIdx=None , cons=None,consIdx=None):
        if circ is not None: self.myCanvas.plotCirc(circ,circIdx)
        if poly is not None: self.myCanvas.plotPoly(poly,polyIdx)
        if line is not None: self.myCanvas.plotLine(line,lineIdx)
        if cons is not None: self.myCanvas.plotCons(cons,consIdx)

    def saveAnnotation2Yaml(self):
        ### preparing yaml and image names
        imagName = self.imagList[self.imagIndx].split('/')[-1]
        imagExtension = imagName.split('.')[-1]
        yamlName = self.imagList[self.imagIndx][:-len(imagExtension)]+'yaml'

        ### preparing annotations list
        annotations = []
        for [x,y,r] in self.circ:
            annotations.append({'category': 'circle',
                                'cen': str(x)+' , '+str(y),
                                'rad': r,
                                'id': None})
        
        for pts in self.poly:
            d = {'p'+str(i+1):str(pts[i][0])+' , '+str(pts[i][1])
                 for i in range(len(pts))}
            d['category'] = 'polygon'
            d['id'] = None
            annotations.append(d)
            
        for [[x1,y1],[x2,y2]] in self.line:
            annotations.append({'category': 'line',
                                'p1': str(x1)+' , '+str(y1),
                                'p2': str(x2)+' , '+str(y2),
                                'id': None})
            
        for pts in self.cons:
            d = {'p'+str(i+1):str(pts[i][0])+' , '+str(pts[i][1])
                 for i in range(len(pts))}
            d['category'] = 'constellation'
            d['id'] = None
            annotations.append(d)
            
        ### setting data and saving yaml file
        data = {'date':[str(time.localtime().tm_year)+'-'+
                        str(time.localtime().tm_mon)+'-'+
                        str(time.localtime().tm_mday)],
                'image': imagName,
                'annotations': annotations}

        if len(annotations) != 0:
            with open(yamlName, 'w') as outfile:
                outfile.write( yaml.dump(data, default_flow_style=False) )

            ### Adding newly saved yaml file to the list
            self.loadYamlLists()

    #########################################################################
    ############################# Navigations ###############################
    #########################################################################
    def navNext(self): self.navGoTo(mode='next')
    def navPrev(self): self.navGoTo(mode='prev')
    def navGoTo(self, mode='goto'):
        self.saveAnnotation2Yaml()
        
        if mode == 'prev':
            idx = self.imagIndx - 1 # python value decrease by button
            idx = idx%len(self.imagList) # handling overflow
            idx += 1 # UI value
            self.ui.navigationCounter.setText(str(idx)+'/'+str(len(self.imagList)))
        elif mode == 'next':
            idx = self.imagIndx + 1# python value increase by button
            idx = idx%len(self.imagList) # handling overflow
            idx += 1 # UI value 
            self.ui.navigationCounter.setText(str(idx)+'/'+str(len(self.imagList)))

        idx = self.ui.navigationCounter.toPlainText().split('/')[0]
        if idx.isdigit():
            if -1 < int(idx)-1 < len(self.imagList):
                self.imagIndx = int(idx)-1 # compensating for python starting at 0
                self.startNewImage()



    #########################################################################
    ################################ MISC ###################################
    #########################################################################
    def sortPointsCCW(self, points):
        
        def dis (p1,p2):
            return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

        # removing collocating points within the range
        tolerance = 2 #np.spacing(1)
        for i in range(len(points)-1,-1,-1):
            for j in range(i-1,-1,-1):
                if dis(points[i],points[j]) < tolerance:
                    points.pop(i)
                    break                

        # Sorting 
        pts = np.array(points)
        cen = np.mean(pts,axis=0)
        angle2pts = [np.arctan2(p[1]-cen[1], p[0]-cen[0])
                     for p in np.array(pts)]
        return np.array([v for (t,v) in sorted(zip(angle2pts,pts))])


    def about(self):
        QtGui.QMessageBox.about(self, "About Image Annotation for Ground Truth",
                                """<b>Version</b> %s
                                <p>Copyright &copy; 2015 Saeed Gholami Shahbandi.
                                All rights reserved in accordance with
                                BSD 3-clause - NO WARRANTIES!
                                <p>This GUI facilitates the process of 
                                manually generating ground truth for semantic annotation of images.
                                The results are stored in YAML format.
                                <p>Python %s - PySide version %s - Qt version %s on %s""" % (__version__,
                                                                                             platform.python_version(), PySide.__version__, QtCore.__version__,
                                                                                             platform.system()))
