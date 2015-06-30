import sys, os, platform
import time
import thread
import numpy as np
import cv2
import yaml

import PySide
from PySide import QtCore, QtGui  # QtGui.QMainWindow, QtGui.QPushButton, QtGui.QApplication

import isagt # isagt.Ui_MainWindow
__version__ = '0.2'


# TODO - HP
# put available annotations in the list field
# how to remove an annotation if deleted
# add id
# extract circles from premeter points
# unwrapping fishheye
# highjack arrow keys# TODO: - MP
# 1. when clicking a new point, it shoud be displayed in Red
# 2. when annotation is grabbed, they should turn green
# 3. loaded annotations in Blue

# TODO: - LP
# helpers
# fix constellation plotting rescale problem
# proper commenting for pydoc
# while the sorting function is in use, it only supports convex polygon

##############################################################
import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
import pylab

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection      

class MyMplCanvas(FigureCanvas):
    """
    Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.).
    But I connected this to graphicsView in the ui
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure()#figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)
        self.axes.axis('off')

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # fig.canvas.mpl_connect('button_press_event', self.onclick)

        self.AnnotationAlpha = 0.4
        
        self.patches, self.lines,  = [],[]
        self.constellations = []
        self.draw()


    def plotImage(self,image):
        self.axes.imshow(image, interpolation='nearest', origin='lower')
        self.draw()

    def plotPoly(self, points):
        # colors = 100*np.random.rand(len(self.patches))
        collection = PatchCollection([mpatches.Polygon(np.array(points),
                                                       ec="none")],
                                     alpha=self.AnnotationAlpha)
        # collection.set_array(np.array(colors))
        self.axes.add_collection(collection)

        self.draw()
        
    def plotCirc(self, circ):
        [cx,cy,r] = circ
        # colors = 100*np.random.rand(len(self.patches))
        collection = PatchCollection([mpatches.Circle(np.array([cx,cy]),
                                                      r, ec="none")],
                                     alpha=self.AnnotationAlpha)
        # collection.set_array(np.array(colors))
        self.axes.add_collection(collection)

        self.draw()
        
    def plotLine(self, points):
        self.axes.add_line(mlines.Line2D(np.array(points)[:,0],
                                         np.array(points)[:,1],
                                         lw=1.,
                                         alpha=self.AnnotationAlpha))
        self.draw()
        
    def plotCons(self, points):
        pts = np.array(points)
        syms = [ 'ro','go','bo','ko',
                 'r^','g^','b^','k^']
        self.axes.hold(True)
        self.axes.plot(pts[:,0],pts[:,1] , syms[0]) 
        # self.axes.scatter(pts[:,0],pts[:,1])
        self.draw()
        self.axes.hold(False)


##############################################################

class MainWindow(QtGui.QMainWindow, isagt.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = isagt.Ui_MainWindow()
        self.ui.setupUi(self)

        ## Matplotlib Setting
        self.main_widget = self.ui.graphicsView #QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout(self.main_widget)
        self.myCanvas = MyMplCanvas(self.main_widget)#, width=5, height=4, dpi=100)
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
        ## Radio buttons
        self.ui.loadYaml.toggled.connect(self.startNewImage)
        self.ui.unwrapFlag.toggled.connect(self.startNewImage)
        self.ui.displayAnnotation.toggled.connect(self.startNewImage)

        ## 
        self.yamlList, self.imagList = None, None
        self.sorting = True
        
        self.annotationList = None
        # self.ui.annotationList.clear(self)
        # self.ui.annotationList.currentRow(self)
        # self.ui.annotationList.currentItem(self)
        # self.ui.annotationList.indexFromItem (self, QListWidgetItem item)
        # self.ui.annotationList.insertItem (self, int row, QListWidgetItem item)
        # self.ui.annotationList.insertItem (self, int row, QString label)
        # self.ui.annotationList.insertItems (self, int row, QStringList labels)

    #### loading stage
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
        # this function is [always?] hosted by other functins
        # such as "loadFileLists", "navGoTo"
        # be careful not to lock it up!

        
        self.annotationList = {}
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
            self.image = image
        self.myCanvas.plotImage(self.image)        

        ### Loading Yaml file
        if self.ui.loadYaml.isChecked():
           self.loadYamlFile()

        #TODO: update the self.annotationList


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


            
    #### annotations
    def mouseClick(self, event):
        # print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        #     event.button, event.x, event.y, event.xdata, event.ydata)
        self.temp.append([event.xdata, event.ydata])
        if event.button == 2:
            print 'I could wrap up evrything here, right?'
            # self.grabAnnotation()
        
    def grabAnnotation(self):
        
        if self.ui.catPoly.isChecked():
            if self.sorting == True:
                self.poly.append( self.sortPointsCCW(self.temp) )
            else:
                self.poly.append( self.temp )
            self.plotAnnotations(poly=self.poly[-1])

        elif self.ui.catConstellation.isChecked():
            self.plotAnnotations(cons=self.cons[-1])

        elif self.ui.catLine.isChecked():
            self.line.append(self.temp)
            self.plotAnnotations(line=self.line[-1])

        elif self.ui.catCircle.isChecked():
            # TODO: solve the equation
            self.circ.append(self.temp)
            self.plotAnnotations(circ=self.circ[-1])

        else:
            QtGui.QMessageBox.about(self, "error",
                                    """readCategory function says: no category?!!""")
        self.resetAnnotation() # => self.temp = []

        #TODO: update the self.annotationList
        self.ui.annotationList


    def resetAnnotation(self):
        self.temp = []

    def plotAllAnnotations(self):
        for obj in self.circ: self.myCanvas.plotCirc(obj)
        for obj in self.poly: self.myCanvas.plotPoly(obj)
        for obj in self.line: self.myCanvas.plotLine(obj)
        for obj in self.cons: self.myCanvas.plotCons(obj)

    def plotAnnotations(self, circ=None, poly=None, line=None, cons=None):
        if circ is not None: self.myCanvas.plotCirc(circ)            
        if poly is not None: self.myCanvas.plotPoly(poly)
        if line is not None: self.myCanvas.plotLine(line)
        if cons is not None: self.myCanvas.plotCons(cons)

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
        
        with open(yamlName, 'w') as outfile:
            outfile.write( yaml.dump(data, default_flow_style=False) )

        ### Adding newly saved yaml file to the list
        # self.yamlList.append(yamlName)
        # self.yamlList.sort()
        self.loadYamlLists()

    #### NAVIGATION functoins
    def navNext(self):
        # TODO: remove this function and connect the Next Button directly to "NavGoTo"
        self.navGoTo(mode='next')

    def navPrev(self):
        # TODO: remove this function and connect the Prev Button directly to "NavGoTo"
        self.navGoTo(mode='prev')

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



    #### MISC
    def sortPointsCCW(self, points):
        
        def dis (p1,p2):
            return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

        # removing collocating points 
        for i in range(len(points)-1,-1,-1):
            for j in range(i-1,-1,-1):
                if dis(points[i],points[j])<np.spacing(1):
                    points.pop(i)
                    break                

        # Sorting 
        pts = np.array(points)
        cen = np.mean(pts,axis=0)
        angle2pts = [np.arctan2(p[1]-cen[1], p[0]-cen[0])
                     for p in np.array(pts)]
        return np.array([v for (t,v) in sorted(zip(angle2pts,pts))])


    def about(self):
        QtGui.QMessageBox.about(self, "About Image Semantic Annotation for Ground Truth",
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

##############################################################

# if ''name'' == "''main''":
app = QtGui.QApplication(sys.argv)
mySW = MainWindow()
mySW.show()
app.exec_()
# sys.exit(app.exec_())

