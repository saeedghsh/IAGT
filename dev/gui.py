import sys, os, platform
import time
import thread
import numpy as np
import cv2
import yaml

import PySide
from PySide import QtCore, QtGui  # QtGui.QMainWindow, QtGui.QPushButton, QtGui.QApplication

import isagt # isagt.Ui_MainWindow
__version__ = '0.1'


def parseAnnotationYaml(data):
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
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure()#figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
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
        # cmap='gray', interpolation='bilinear',
        # cmap=cm.RdYlGn, origin='lower',
        # vmax=abs(image).max(), vmin=-abs(image).max()
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
        # self.constellations.append(np.array(points))
        # n = len(self.constellations)
        # syms = [ 'ro','go','bo','ko' , 'r^','g^','b^','k^']
        # for pts, mk in zip(self.constellations , syms[:n]):
            # self.axes.plot(pts[:,0],pts[:,1] , mk)
        # for pts in self.constellations: self.axes.scatter(pts[:,0], pts[:,1])
        
        # self.axes.scatter(np.array(points)[:,0], np.array(points)[:,1])
        self.draw()


##############################################################

class MainWindow(QtGui.QMainWindow, isagt.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = isagt.Ui_MainWindow()
        self.ui.setupUi(self)

        ######### Matplotlib Setting
        self.main_widget = self.ui.graphicsView #QtGui.QWidget(self)
        self.layout = QtGui.QVBoxLayout(self.main_widget)
        self.myCanvas = MyMplCanvas(self.main_widget)#, width=5, height=4, dpi=100)
        self.layout.addWidget(self.myCanvas)
        self.main_widget.setFocus()
        # self.setCentralWidget(self.main_widget)
        self.myCanvas.mpl_connect('button_press_event', self.mouseClick)
        
        ######### Push buttons
        self.ui.loadButton.clicked.connect(self.loadFiles)
        self.ui.aboutButton.clicked.connect(self.about)
        self.ui.navGoto.clicked.connect(self.navGoTo)
        self.ui.navNext.clicked.connect(self.navNext)
        self.ui.navPrev.clicked.connect(self.navPrev)
        self.ui.annotateAdd.clicked.connect(self.grabAnnotation)
        self.ui.annotateReset.clicked.connect(self.resetAnnotation)
        ######### Radio buttons
        self.ui.loadYaml.toggled.connect(self.startNewImage)
        self.ui.unwrapFlag.toggled.connect(self.startNewImage)
        self.ui.displayAnnotation.toggled.connect(self.startNewImage)

        ######### 
        self.yamlList, self.imagList = None, None
        
    #### loading stage
    def loadFiles(self):

        # Loading file(s) name(s)
        if self.ui.loadOption.currentText() == 'Folder':
            path = QtGui.QFileDialog.getExistingDirectory()
            content = [ f for f in os.listdir(path)
                        if os.path.isfile(os.path.join(path,f)) ]
            filesNames = [os.path.join(path,f) for f in content]

        elif self.ui.loadOption.currentText() == 'Single File':
            filesNames = QtGui.QFileDialog.getOpenFileName()

        # sort file names into yamls and images
        # remove empty strings and none image files
        yamlList, imagList = [], []
        yamlFormats = ['yaml', 'YAML', 'Yaml']
        imagFormats = ['.png', '.PNG', '.jpg', '.JPG', 'JPEG', 'jpeg', '.bmp']
        for i in range(len(filesNames)-1,-1,-1):
            if len(filesNames[i]) == 0:
                pass #filesNames.pop(i)
            elif filesNames[i][-4:] in yamlFormats:
                yamlList.append(filesNames[i])
            elif filesNames[i][-4:] in imagFormats:
                imagList.append(filesNames[i])

        # Initialtion an enabling buttons if there is amy image loaded
        
        if len(imagList) > 0:
            yamlList.sort(), imagList.sort()
            self.yamlList, self.imagList = yamlList, imagList
            self.ui.groupCategory.setEnabled(True)
            self.ui.groupNavigation.setEnabled(True)
            self.ui.groupAnnotation.setEnabled(True)
            self.ui.groupAnnotationList.setEnabled(True)
            self.ui.groupAnnotationID.setEnabled(True)

            self.imagIndx = 0

            self.startNewImage()
            
        else:
            pass

    def startNewImage(self):
        # this function is [always?] hosted by other functins
        # such as "loadFiles", "navGoTo"
        # be careful not to lock it up!

        ### plotting the image
        self.ui.textAddress.setText(self.imagList[self.imagIndx])
        self.ui.navigationCounter.setText(str(self.imagIndx+1)+'/'+str(len(self.imagList)))

        image = cv2.imread(self.imagList[self.imagIndx])
        if self.ui.unwrapFlag.isChecked():
            #TODO
            if self.ui.unwrapOption.currentText() == 'Fisheye - Downward':
                pass # unrwape image
            elif self.ui.unwrapOption.currentText() == 'Fisheye - Forward':
                pass # unrwape image
            elif self.ui.unwrapOption.currentText() == 'OminCam':
                pass # unrwape image
            self.image = image
        self.myCanvas.plotImage(self.image)        

        ### Loading Yaml file
        self.circ, self.poly, self.line, self.cons =[],[],[],[]
        if self.ui.loadYaml.isChecked():
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
                        circ, poly, line, cons = parseAnnotationYaml(data)
                        self.circ, self.poly, self.line, self.cons = circ,poly,line,cons
            else:
                print "yaml not found"

        ### plot available annotations
        if self.ui.displayAnnotation.isChecked():
            self.plotAllAnnotations()


        ### initializing-emptying the temp list
        self.temp = []

    #### annotations
   
 
    def mouseClick(self, event):
        print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
            event.button, event.x, event.y, event.xdata, event.ydata)
        self.temp.append([event.xdata, event.ydata])
        
    def grabAnnotation(self):
        if self.ui.catPoly.isChecked():
            # TODO: sort points in correct order
            self.poly.append(self.temp)
            self.plotAnnotations(poly=self.poly[-1])

        elif self.ui.catConstellation.isChecked():
            # TODO: sort points in correct order
            self.cons.append(self.temp)
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
        data = {'date':[time.localtime().tm_year,
                        time.localtime().tm_mon,
                        time.localtime().tm_mday],
                'image': imagName,
                'annotations': annotations}
        
        with open(yamlName, 'w') as outfile:
            outfile.write( yaml.dump(data, default_flow_style=False) )




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

