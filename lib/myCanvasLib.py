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

import numpy as np

import PySide
from PySide import QtGui  # QtGui.QMainWindow, QtGui.QPushButton, QtGui.QApplication

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'

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
        self.axes.axis('off')        
        self.axes.hold(False)

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
        self.axes.set_xlim([0, np.shape(image)[1]])
        self.axes.set_ylim([0, np.shape(image)[0]])
        self.draw()

    def plotPoly(self, points, idx=None ):
        # colors = 100*np.random.rand(len(self.patches))
        collection = PatchCollection([mpatches.Polygon(np.array(points),
                                                       ec="none")],
                                     alpha=self.AnnotationAlpha)
        # collection.set_array(np.array(colors))
        self.axes.add_collection(collection)
        
        if idx is not None:
            x0 = np.array(points)[:,0].mean()
            y0 = np.array(points)[:,1].mean()
            self.axes.text(x0,y0, str(idx), fontsize=15)

        self.draw()
        
    def plotCirc(self, circ, idx=None):
        [cx,cy,r] = circ
        # colors = 100*np.random.rand(len(self.patches))
        collection = PatchCollection([mpatches.Circle(np.array([cx,cy]),
                                                      r, ec="none")],
                                     alpha=self.AnnotationAlpha)
        # collection.set_array(np.array(colors))
        self.axes.add_collection(collection)

        if idx is not None:
            self.axes.text(cx,cy, str(idx) , fontsize=15)

        self.draw()
        
    def plotLine(self, points, idx=None):
        self.axes.add_line(mlines.Line2D(np.array(points)[:,0],
                                         np.array(points)[:,1],
                                         lw=1.,
                                         alpha=self.AnnotationAlpha))

        if idx is not None:
            x0 = np.array(points)[:,0].mean()
            y0 = np.array(points)[:,1].mean()
            self.axes.text(x0,y0, str(idx) , fontsize=15)
            
        self.draw()
        
    def plotCons(self, points, idx=None, symbolID=1):
        pts = np.array(points)
        syms = [ 'ro','go','bo','ko',
                 'r*','g*','b*','k*',
                 'r^','g^','b^','k^',]
        self.axes.hold(True)
        self.axes.plot(pts[:,0],pts[:,1] , syms[symbolID]) 
        # self.axes.scatter(pts[:,0],pts[:,1])

        if idx is not None:
            x0 = np.array(points)[:,0].mean()
            y0 = np.array(points)[:,1].mean()
            self.axes.text(x0,y0, str(idx) , fontsize=15)

        self.draw()
        self.axes.hold(False)
