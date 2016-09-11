


import numpy as np
import matplotlib as mpl
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg, NavigationToolbar2QT
from mpl_toolkits.mplot3d import axes3d
import sys
import re

class FunctionViewer(QtGui.QWidget):

    def __init__(self, parent=None):
        super(FunctionViewer, self).__init__()
        self.setWindowTitle("FunctionViewer")
        self.functions = []
        self.initUI()

    def show(self):
        super(FunctionViewer, self).show()

        # Get initial geometry of the widget:
        qr = self.frameGeometry()

        # Show it at the center of the screen
        cp = QtGui.QDesktopWidget().availableGeometry().center()

        # Move the window's center at the center of the screen
        qr.moveCenter(cp)

        # Then move it at the top left
        translation = qr.topLeft()

        self.move(translation)

    def initUI(self):
        #------- Manager for FunctionFig -------#
        self.functionFig = FunctionFig(self)
        self.function_manager = QtGui.QWidget()
        self.function_tool = NavigationToolbar2QT(self.functionFig, self)
        function_grid = QtGui.QGridLayout()
        function_grid.addWidget(self.function_tool, 0, 0)
        function_grid.addWidget(self.functionFig, 1, 0)
        self.function_manager.setLayout(function_grid)

        #------- Widgets -------#
        #--- Labels ---#
        func_label       = MyQLabel('Enter Function:', ha= 'center')
        step_label       = MyQLabel('Enter Steps:', ha= 'center')
        domain_label     = MyQLabel('Domain:', ha= 'center')
        color_label      = MyQLabel('Color:', ha= 'center')
        markersize_label = MyQLabel('Marker size')

        #--- Edits ---#
        self.func_edit   = QtGui.QLineEdit('exp(x)')
        self.step_edit   = QtGui.QLineEdit('0.2')
        self.domain_edit = QtGui.QLineEdit('-1, 1')
        self.color_edit  = QtGui.QLineEdit('blue')
        self.markersize_edit = QtGui.QLineEdit('5')

        #- Edits' Disposition -#
        self.markersize_edit.setFixedWidth(80)

        #--- Buttons ---#
        plot_btn = QtGui.QPushButton('Plot')

        #- Buttons Actions -#
        plot_btn.clicked.connect(self.functionFig.plot_func)

        #--- CheckBoxes ---#
        self.marker_check = QtGui.QCheckBox('Mark every values')

        #--- CheckBoxes' Actions ---#
        self.marker_check.stateChanged.connect(self.functionFig.plot_func)

        #--- ComboBoxes ---#
        self.marker_combo = QtGui.QComboBox()

        #--- ComboBoxes' Items ---#
        marker_list = ['o', '.', '*']
        self.marker_combo.addItems(marker_list)


        #------- Markers' settings GroupBox -------#
        marker_group = QtGui.QGroupBox('Markers')
        marker_grid = QtGui.QGridLayout()
        marker_grid.addWidget(self.marker_combo, 0, 0, 1, 2)
        marker_grid.addWidget(markersize_label, 1, 0)
        marker_grid.addWidget(self.markersize_edit, 1, 1)
        marker_grid.addWidget(self.marker_check, 2, 0, 1, 2)
        marker_group.setLayout(marker_grid)

        #------- Master Grid -------#
        master_grid = QtGui.QGridLayout()
        master_grid.addWidget(self.function_manager, 0, 0, 12, 1)
        master_grid.addWidget(func_label, 1, 1)
        master_grid.addWidget(self.func_edit, 2, 1)
        master_grid.addWidget(step_label, 3, 1)
        master_grid.addWidget(self.step_edit, 4, 1)
        master_grid.addWidget(domain_label, 5, 1)
        master_grid.addWidget(self.domain_edit, 6, 1)
        master_grid.addWidget(color_label, 7, 1)
        master_grid.addWidget(self.color_edit, 8, 1)
        master_grid.addWidget(marker_group, 9, 1)
        master_grid.addWidget(plot_btn, 10, 1)
        master_grid.setRowStretch(11, 100)
        master_grid.setColumnStretch(0, 100)
        self.setLayout(master_grid)

class FunctionFig(FigureCanvasQTAgg):
    '''
    This is the function which holds the function plot
    '''
    def __init__(self, ui):
        fig_width, fig_height = 10, 10
        fig = mpl.figure.Figure(figsize=(fig_width, fig_height), facecolor='white')
        super(FunctionFig, self).__init__(fig)
        self.initFig()
        self.ui = ui

    def initFig(self):
        self.ax = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])

    def plot_func(self):
        self.ax.cla()

        # Getting the information from the GUI
        current_func  = self.ui.func_edit.text()
        current_step  = float(self.ui.step_edit.text())
        domain_input  = self.ui.domain_edit.text()
        current_color = self.ui.color_edit.text()
        marker        = self.ui.marker_combo.currentText()
        marker_size   = float(self.ui.markersize_edit.text())
        marker_state  = self.ui.marker_check.isChecked()


        self.ax.set_title(current_func, y= 1.02)
        self.ax.set_xlabel(' X ')
        self.ax.set_ylabel(' Y ')

        #TODO: domain expressed with pi
        if 'pi' in domain_input:
            str_limits = domain_input.split(',')
            for i in range(len(domain_input)):
                if 'pi' in str_limits[i]:
                    str_limits[i] = str_limits[i] - 'pi'

        # Basic float or int domain
        else:
            str_limits = domain_input.split(',')
            float_limits = [float(i) for i in str_limits]
            #print(float_limits)

        # Making an array from the first domain limit to the other one
        # with de step defined in the GUI
        values = np.arange(float_limits[0], float_limits[1] + current_step, current_step)


        current_func = current_func.replace('(', '/').replace(')', '/')
        current_func = current_func.split('/')

        possible_input_dimensions = ['x', 'y', 'z', 'X', 'Y', 'Z']

        for i in range(len(current_func)):
            if len(current_func[i]) == 1 and current_func[i] in possible_input_dimensions:
                ind = i
                print(ind)
                print(current_func)
                for n in range(i):
                    ind -= 1
                    if n == 0:
                        plot_input = getattr(np, current_func[ind])(values)
                        print(current_func[ind])
                    else:
                        plot_input = getattr(np, current_func[ind])(plot_input)
                        print(current_func[ind])

        if marker_state:
            self.ax.plot(values, plot_input, color= current_color, marker= marker, markersize= marker_size)
        else:
            self.ax.plot(values, plot_input, color= current_color)

        self.ax.set_xlim(values[0], values[-1])
        self.draw()


#--- Class For Alignment ---#
class  MyQLabel(QtGui.QLabel):
    def __init__(self, label, ha='left',  parent=None):
        super(MyQLabel, self).__init__(label,parent)
        if ha == 'center':
            self.setAlignment(QtCore.Qt.AlignCenter)
        elif ha == 'right':
            self.setAlignment(QtCore.Qt.AlignRight)
        else:
            self.setAlignment(QtCore.Qt.AlignLeft)
if __name__ == '__main__':


    app = QtGui.QApplication(sys.argv)

    ui = FunctionViewer()
    ui.show()

    sys.exit(app.exec_())