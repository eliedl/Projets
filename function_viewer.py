


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
        func_label = MyQLabel('Enter Function:', ha= 'center')
        step_label = MyQLabel('Enter Steps:', ha= 'center')
        domain_label = MyQLabel('Domain:', ha= 'center')
        color_label = MyQLabel('Color:', ha= 'center')

        #--- Edits ---#
        self.func_edit = QtGui.QLineEdit('exp(x)')
        self.step_edit = QtGui.QLineEdit('0.2')
        self.domain_edit = QtGui.QLineEdit('-1, 1')
        self.color_edit = QtGui.QLineEdit('blue')

        #--- Buttons ---#
        plot_btn = QtGui.QPushButton('Plot')

        #- Buttons Actions -#
        plot_btn.clicked.connect(self.functionFig.plot_func)

        #------- Master Grid -------#
        master_grid = QtGui.QGridLayout()
        master_grid.addWidget(self.function_manager, 0, 0, 11, 1)
        master_grid.addWidget(func_label, 1, 1)
        master_grid.addWidget(self.func_edit, 2, 1)
        master_grid.addWidget(step_label, 3, 1)
        master_grid.addWidget(self.step_edit, 4, 1)
        master_grid.addWidget(domain_label, 5, 1)
        master_grid.addWidget(self.domain_edit, 6, 1)
        master_grid.addWidget(color_label, 7, 1)
        master_grid.addWidget(self.color_edit, 8, 1)
        master_grid.addWidget(plot_btn, 9, 1)
        master_grid.setRowStretch(10, 100)
        master_grid.setColumnStretch(0, 100)
        self.setLayout(master_grid)

class FunctionFig(FigureCanvasQTAgg):

    def __init__(self, ui):
        fig_width, fig_height = 6, 8
        fig = mpl.figure.Figure(figsize=(fig_width, fig_height), facecolor='white')
        super(FunctionFig, self).__init__(fig)
        self.initFig()
        self.ui = ui

    def initFig(self):
        self.ax = self.figure.add_axes([0.05, 0.05, 0.9, 0.9])

    def plot_func(self):
        self.ax.cla()
        current_func = self.ui.func_edit.text()
        current_step = float(self.ui.step_edit.text())
        domain_input = self.ui.domain_edit.text()
        current_color = self.ui.color_edit.text()

        str_limits = re.findall(r"[+-]?\d+(?:\.\d+)?", domain_input)
        float_limits = [float(i) for i in str_limits]
        #print(float_limits)


        values = np.arange(float_limits[0], float_limits[1] + current_step, current_step)
        #print(values)
        current_func = current_func.replace('(', '/').replace(')', '/')
        current_func = current_func.split('/')

        for i in range(len(current_func)):
            if len(current_func[i]) == 1:
                ind = i
                if i > 1:
                    plot_input = getattr(np, current_func[-len(current_func)])(getattr(np, current_func[-len(current_func) + 1])(values))
                elif i == 1:
                    plot_input = getattr(np, current_func[0])(values)


        self.ax.plot(plot_input, color= current_color)
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