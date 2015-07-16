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


import yaml, os
import scipy.io

def loadFileList(path):
    content = [ f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path,f)) ]
    filesNames = [os.path.join(path,f) for f in content]
    yamlFormats = ['yaml', 'YAML', 'Yaml']
    yamlList = []
    for i in range(len(filesNames)-1,-1,-1):
        if len(filesNames[i]) == 0:
            pass 
        elif filesNames[i][-4:] in yamlFormats:
            yamlList.append(filesNames[i])
            
    return yamlList

def parseYaml(data):
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

def loadYamlFile(yamlName):
    data = yaml.load(open(yamlName, 'r'))
    circ, poly, line, cons = None, None, None, None
    #checks if there is any annotation
    if 'annotations' in data.keys():
        #checks if the annotation is not empty
        if data['annotations'] is not None:
            circ, poly, line, cons = parseYaml(data)
    return circ, poly, line, cons
                


# ############################################
# ############################################
# ############################################
path = '../SampleImages' #os.path.curdir
yamlList = loadFileList(path)
for f in yamlList:
    circ, poly, line, cons = loadYamlFile(f)
    if circ is not None:
        d = {}
        for i in range(len(circ)):
            d['circle_'+str(i+1)] = circ[i]
        for i in range(len(line)):
            d['line_'+str(i+1)] = line[i]
        for i in range(len(poly)):
            d['polygon_'+str(i+1)] = poly[i]
        for i in range(len(cons)):
            d['constellation_'+str(i+1)] = cons[i]
        scipy.io.savemat(f+'.mat' , d)
        
    
