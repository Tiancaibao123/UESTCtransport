from PyQt5.QtWidgets import QSizePolicy, QMainWindow, QApplication, QGridLayout

from PyQt5.QtCore import pyqtSlot

from Ui_MainWIndow import Ui_MainWindow

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt

MAX_VALUE = 1000


class MainWindow(QMainWindow):
    def __init__(self, matrix):

        super(MainWindow, self).__init__()
        self.UI = Ui_MainWindow()
        self.UI.setupUi(self)
        # 图片指示器
        self.counter = 0
        # 记录最短路径
        self.shorts = []
        # 记录路径
        self.path = []
        # 邻接矩阵
        self.matrix = matrix
        # 记录被访问的节点
        self.visited = []

        self.init(0)

        # 添加画布
        self.fig_line = Myplot2D()
        layout = QGridLayout()
        layout.addWidget(self.fig_line)
        self.UI.frame.setLayout(layout)

        self.dijkstra(0)
        self.print_path(0)

    # 初始化
    def init(self, start: int):
        self.clear_list()

        # 初始化被访问节点
        for i in range(len(self.matrix)):
            self.visited.append(False)
            self.shorts.append(MAX_VALUE)
            self.path.append(str(start) + "-->" + str(i))

    #
    @pyqtSlot()
    def on_btn_next_clicked(self):
        self.plot_algorithm()
        self.counter += 1
        if self.counter > 6:
            self.counter = 0


    # 迪杰斯特拉算法
    def dijkstra(self, start: int):
        index = -1

        self.shorts[start] = 0
        self.visited[start] = True

        for i in range(len(self.matrix)):
            min = MAX_VALUE
            # 找到起点最近的未被访问的节点
            for j in range(len(self.matrix)):
                if (not self.visited[j]) and self.matrix[start][j] < min:
                    index = j
                    min = self.matrix[start][j]

            if not self.visited[index]:
                # 更改最接距离
                self.shorts[index] = min
                self.visited[index] = True

            # 判断直接访问还是简介访问近一点
            for m in range(len(self.matrix)):
                if (not self.visited[m]) and (self.matrix[start][index] + self.matrix[index][m] <= self.matrix[start][m]):
                    self.matrix[start][m] = self.matrix[start][index] + self.matrix[index][m]
                    self.path[m] = self.path[index] + "-->" + str(m)

    # 清零
    def clear_list(self):
        self.shorts.clear()
        self.path.clear()
        self.visited.clear()

    # 打印路径
    def print_path(self, start: int):
        for i in range(len(self.matrix)):
            if i == start:
                continue
            if self.shorts[i] == MAX_VALUE:
                print(str(start) + "不可以直达" + str(i))
            else:
                print(str(start) + "可以直达" + str(i) + ", 长度是" + str(self.shorts[i]) + "最短路径是" + self.path[i])

    # 算法可视化
    def plot_algorithm(self):
        self.fig_line.axes_2D.cla()
        file_name = "img/" + str(self.counter) + ".png"
        img = plt.imread(file_name)
        self.fig_line.axes_2D.imshow(img)
        self.fig_line.draw()


class Myplot2D(FigureCanvas):
    def __init__(self, parent=None, width=15, height=10, dpi=100):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置支持中文
        plt.rcParams['axes.unicode_minus'] = False  # 设置-号

        self.fig = plt.figure(figsize=(width, height), dpi=dpi)  # 创建一个新的图框

        FigureCanvas.__init__(self, self.fig)  # 激活图框，必须要有这句话！！
        self.setParent(parent)  # 设定父类，！注：暂不指定父类，用来以后修改继承从而增加新的功能
        self.axes_2D = self.fig.add_subplot(111)  # 打开一个分图片显示区域
        self.fig.subplots_adjust(hspace=0.3, wspace=0.3)

        # 设置画布的尺寸策略
        FigureCanvas.setSizePolicy(self, QSizePolicy.Ignored, QSizePolicy.Ignored)


if __name__ == "__main__":
    import sys
    matrix = [[1000, 6, 1000, 2, 1000, 1000, 1000],
              [1000, 1000, 5, 1000, 1000, 3, 1000],
              [1000, 1000, 1000, 1000, 1000, 1000, 3],
              [1000, 7, 1000, 1000, 5, 1000, 1000],
              [1000, 1000, 1000, 1000, 1000, 5, 1],
              [1000, 1000, 3, 1000, 1000, 1000, 1000],
              [1000, 1000, 1000, 1000, 1000, 1000, 1000]]

    app = QApplication(sys.argv)
    win = MainWindow(matrix)
    win.show()
    sys.exit(app.exec())