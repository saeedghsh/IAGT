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

import cv2
import yaml
import sys, os
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

#####################################################
##################### functions #####################
#####################################################

def parseAnnotationYaml(data):
    if 'annotations' in data.keys(): #checks if there is any annotation
        if data['annotations'] != None: #checks if the annotation is not empty
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
        else:
            return False
    else:
        return False

def drawAnnotationPatch(patches, lines, constellations, annotation):
    keys , p = annotation.keys() , []
    while 'category' in keys: keys.remove('category')
    while 'id' in keys: keys.remove('id')
    if annotation['category'] == 'circle':
        # cir = [ [cx1,cy1,r1], [cx2,cy2,r2], ... ]
        c = [float(s) for s in annotation['cen'].split()
             if s.replace(".", "", 1).isdigit()]
        r = float(annotation['rad'])
        patches.append( mpatches.Circle(np.array(c), r, ec="none") )
        
    elif annotation['category'] == 'polygon':
        # pol = [ [[px1,py1], [px2,py2], ...] , ...]
        for k in sorted(keys): p.append( [float(s) for s in annotation[k].split()
                                          if s.replace(".", "", 1).isdigit()] )
        patches.append( mpatches.Polygon(np.array(p), ec="none") )
        
    elif annotation['category'] == 'line':
        # lin = [ [[px1,py1], [px2,py2]] , ...]
        for k in sorted(keys): p.append( [float(s) for s in annotation[k].split()
                                  if s.replace(".", "", 1).isdigit()] )
        lines.append( mlines.Line2D(np.array(p)[:,0], np.array(p)[:,1], lw=1., alpha=1.0))
                
    elif annotation['category'] == 'constellation':
        # con = [ [[px1,py1], [px2,py2], ...] , ...]
        for k in sorted(keys): p.append( [float(s) for s in annotation[k].split()
                                  if s.replace(".", "", 1).isdigit()] )
        constellations.append(np.array(p))
    else:
        print "unknown category"    
    return patches, lines, constellations

def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)


#####################################################
#####################################################
#####################################################

#### Initiating

## Open file
imageName = "../SampleImages/test1.png"
image = cv2.imread(imageName)
# image = cv2.imread("../SampleImages/octagon_BW_deformed_noisy.png")

## Check whether if an annotation file exists, and preparing the data
yamlName = imageName[:-3]+'yaml'
if os.path.isfile(yamlName):
    print "look! yaml is there..."
    data = yaml.load(open(yamlName, 'r'))
    print parseAnnotationYaml(data)
else:
    print "no yaml file found: someone should creat it..."
    data = {}
    data['image'] = imageName
    data['date'] = str(time.localtime().tm_year) + '-' +\
                   str(time.localtime().tm_mon) + '-' + \
                   str(time.localtime().tm_mday)
    
#### Plotting 
fig = plt.figure()
ax = fig.add_subplot(111)
# ax.imshow(image, cmap='gray' ,interpolation='nearest', origin='lower')

## connection mouse curser to figure
cid = fig.canvas.mpl_connect('button_press_event', onclick)
                       
patches, lines, constellations = [], [], []

for a in data['annotations']:
    patches, lines, constellations = drawAnnotationPatch(patches, lines, constellations, a)

colors = 100*np.random.rand(len(patches))
collection = PatchCollection(patches, cmap=plt.cm.jet, alpha=8.)
collection.set_array(np.array(colors))
ax.add_collection(collection)
for l in lines: ax.add_line(l)
colors = 100*np.random.rand(len(constellations))
for (col,ps) in zip(colors,constellations):
    plt.scatter(ps[:,0], ps[:,1] , c=[col]*len(ps[:,0]), cmap=plt.cm.jet)
    # TODO: color of constellations does not change!
plt.axis('equal')
plt.axis('off')
plt.show()



#TODO:
# Line segment annotation
# Square annotation
# Circle annotation
# Oval annotation


# #### saving to yaml file
# with open(yamlName, 'w') as outfile:
#     outfile.write( yaml.dump(data, default_flow_style=False) )
