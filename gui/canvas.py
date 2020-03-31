# -*- coding: utf-8 -*-e
import matplotlib as mpl
mpl.use("Qt5Agg")
import matplotlib.dates as mdate

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from PyQt5.QtWidgets import QSizePolicy

import os
FONT = FontProperties(fname=(os.getcwd() + "/deps/font/wqy-microhei.ttc"), size=10)


class BaseCanvas(FigureCanvas):
    '''
    基类画布
    '''
    def __init__(self, figure):
        super(BaseCanvas, self).__init__(figure)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class HistoryDataCanvas(BaseCanvas):
    '''
    静态路径信息画布，继承自基类画布
    '''
    def __init__(self):
        fig = Figure()
        fig.set_facecolor("white")
        fig.set_edgecolor("black")
        self.axes = fig.add_subplot(111)
        self.axes.set_title("商品历史数据图", fontproperties=FONT, fontsize=14)
        self.axes.set_xlabel("时间轴", fontproperties=FONT, fontsize=10)
        self.axes.set_xticks([])
        self.axes.set_ylabel("价格数据/￥", fontproperties=FONT, fontsize=10)
        self.axes.set_yticks([100 * i for i in range(11)])
        # self.axes.hold(False)
        super(HistoryDataCanvas, self).__init__(figure=fig)

    def compute_initial_figure(self):
        pass
