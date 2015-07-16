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

import sys
from PySide import QtGui
sys.path.append('gui/') # for import isagt in MWL
sys.path.append('lib/')
import myWindowLib as MWL

__version__ = '0.9'

# if ''name'' == "''main''":
app = QtGui.QApplication(sys.argv)
mySW = MWL.MainWindow()
mySW.show()
app.exec_()
# sys.exit(app.exec_())



# TODO - HP
# why the image is upside down?
# unwrapping fishheye
# allow window resize
# list dependencies and installation instructions for different platform
# creat visual instructions.

# TODO: - LP
# helpers
# add zooming
# proper commenting for pydoc


