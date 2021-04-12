import matplotlib.pyplot as plt
# from matplotlib.tri import Triangulation
from matplotlib.patches import Polygon
import numpy as np

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# def update_polygon(tri):
#     if tri == -1:
#         points = [0, 0, 0]
#     else:
#         points = triang.triangles[tri]
#     xs = triang.x[points]
#     ys = triang.y[points]
#     '''
#     # 一
#     a = [1, 2, 3]
#     b = [11, 22, 33]
#     np.column_stack((a, b))
#     Out[21]:
#     array([[1, 11],
#            [2, 22],
#            [3, 33]])
#     # 二
#     np.column_stack(([[1], [2], [3]], [[11], [12], [13]]))
#     Out[22]:
#     array([[1, 11],
#            [2, 12],
#            [3, 13]])
#     # 三
#     a_array = np.array([[1], [2], [3]])
#     b_array = np.array([[2], [3], [4]])
#     np.column_stack((a_array, b_array))
#     Out[26]:
#     array([[1, 2],
#            [2, 3],
#            [3, 4]])
#     '''
#     polygon.set_xy(np.column_stack([xs, ys]))
#
#
# def on_mouse_move(event):
#     if event.inaxes is None:
#         point = -1
#     else:
#         point = trifinder(event.xdata, event.ydata)
#     update_polygon(point)
#     plt.title('In point %i' % point)
#     event.canvas.draw()
#
# n_angles = 16
# n_radii = 5
# min_radius = 0.25
#
# '''
# numpy.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)
# 产生从start到stop的等差数列，num为元素个数，默认50个。endpoint表示是否包含终点
# '''
# radii = np.linspace(min_radius, 0.95, n_radii)
# angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)
#
# '''
# np.repeat用于将numpy数组重复。numpy.repeat(a, repeats, axis=None)：若axis=None，对于多维数组而言，可以将多维数组变化为一维数组，然后再根据repeats参数扩充数组元素；若axis=M，表示数组在轴M上扩充数组元素。
# '''
# angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
# angles[:, 1::2] += np.pi / n_angles
#
# x = (radii*np.cos(angles)).flatten()
# y = (radii*np.sin(angles)).flatten()
# triang = Triangulation(x, y)
# triang.set_mask(np.hypot(x[triang.triangles].mean(axis=1), y[triang.triangles].mean(axis=1)) < min_radius)
# # Use the triangulation's default TriFinder object.
# trifinder = triang.get_trifinder()
#
# # Setup plot and callbacks.
# '''
# subplot(pos, **kwargs)
#
# '''
# plt.subplot(111, aspect='equal')
# plt.triplot(triang, 'bo-')
# polygon = Polygon([[0, 0], [0, 0]], facecolor='y')  # dummy data for (xs, ys)
#
#
# def draw(link_matrix, label_list, value_list):
#     update_polygon(-1)
#
#     # 添加常见的图形对象。这些对象称为块(patch).完整的patch集合位于matplotlib.patches中
#     # 绘制patch对象图形：plt.gca().add_patch(patch_name)
#     plt.gca().add_patch(polygon)
#     plt.gcf().canvas.mpl_connect('motion_notify_event', on_mouse_move)
#     plt.show()


# 有向邻接矩阵

class Scale:
    def __init__(self, fig, link_matrix, label_list, value_list, base_scale=1.5):
        self.fig = fig
        self.base_scale = base_scale
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.press = None

        self.link_matrix = link_matrix
        self.label_list = label_list
        self.value_list = value_list
        # 用于onMotion()中的高亮显示
        # self.polygon = Polygon([[0, 0], [0, 0]], facecolor="y")  # 使用Polygon方法改变颜色
        # plt.gca().add_patch(self.polygon)
        # self.scatter = scatter

        self.fig.canvas.mpl_connect('scroll_event', self.enter_axes)
        self.fig.canvas.mpl_connect("button_press_event", self.enter_axes)
        self.fig.canvas.mpl_connect('button_press_event', self.onPress)
        self.fig.canvas.mpl_connect('button_release_event', self.onRelease)
        self.fig.canvas.mpl_connect('motion_notify_event', self.onMotion)

        self.fig.canvas.mpl_connect('pick_event', self.onpick3)

    def enter_axes(self, event):
        # print(f"enter axes {event.inaxes}")
        axtemp = event.inaxes
        self.cur_xlim=axtemp.get_xlim()
        self.cur_ylim=axtemp.get_ylim()
        # print(f"x {self.cur_xlim} y {self.cur_ylim}")
        xdata = event.xdata
        ydata = event.ydata

        if event.button == "up":
           scale_factor = 1/self.base_scale
        elif event.button == "down":
           scale_factor = self.base_scale
        else:
            scale_factor = 1

        new_width = (self.cur_xlim[1] - self.cur_xlim[0]) * scale_factor
        new_height = (self.cur_ylim[1] - self.cur_ylim[0]) * scale_factor

        relx = (self.cur_xlim[1] - xdata) / (self.cur_xlim[1] - self.cur_xlim[0])
        rely = (self.cur_ylim[1] - ydata) / (self.cur_ylim[1] - self.cur_ylim[0])

        axtemp.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
        axtemp.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])

        self.fig.canvas.draw_idle()

    def onPress(self, event):
        axtemp = event.inaxes
        if event.inaxes != axtemp:
            return
        self.cur_xlim = axtemp.get_xlim()
        self.cur_ylim = axtemp.get_ylim()
        self.press = self.x0, self.y0, event.xdata, event.ydata
        self.x0, self.y0, self.xpress, self.ypress = self.press

    def onMotion(self, event):
        if self.press is None:
            # return
            # 高亮显示
            # bools_list = list(map(lambda x: x.contains_point((event.x, event.y)), self.scatter))
            # try:
            #     ind = bools_list.index(True)
            #     bar = self.scatter[ind]
            #     bbox = bar.get_bbox()
            #     x0, x1, y0, y1 = bbox.x0, bbox.x1, bbox.y0, bbox.y1
            #     xs = (x0, x1, x1, x0)
            #     ys = (y1, y1, y0, y0)
            #
            # except ValueError:
            #     xs = (0, 0, 0, 0)
            #     ys = (0, 0, 0, 0)
            # self.polygon.set_xy(list(zip(xs, ys)))  # 将xs和ys一一对应，生成矩形四个端点的坐标。第一个端点是从矩形的左上角开始的
            # event.canvas.draw()
            return

        if event.inaxes != event.inaxes:
            return
        dx = event.xdata - self.xpress
        dy = event.ydata - self.ypress
        self.cur_xlim -= dx
        self.cur_ylim -= dy
        event.inaxes.set_xlim(self.cur_xlim)
        event.inaxes.set_ylim(self.cur_ylim)

    def onRelease(self, event):
        self.press = None
        event.inaxes.figure.canvas.draw_idle()

    def onpick3(self, event):
        ind = event.ind
        # print('onpick3 scatter:', ind, np.take(x, ind), np.take(y, ind))
        print('onpick3 scatter:', ind)
        point = event.artist
        print('onpick points:', point)

        plt.title(self.label_list[ind[0]])

# def on_mouse_scroll(event):
#     axtemp = event.inaxes
#     x_min, x_max = axtemp.get_xlim()
#     fanwei = (x_max - x_min) / 10
#     if event.button == 'up':
#         axtemp.set(xlim=(x_min + fanwei, x_max - fanwei))
#         axtemp.set(ylim=(x_min + fanwei, x_max - fanwei))
#     elif event.button == 'down':
#         axtemp.set(xlim=(x_min - fanwei, x_max + fanwei))
#         axtemp.set(ylim=(x_min - fanwei, x_max + fanwei))
#
#     event.canvas.draw()
#
# def onclick(event):
#     print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
#           ('double' if event.dblclick else 'single', event.button,
#            event.x, event.y, event.xdata, event.ydata))
# def on_mouse_move(event):
#     if event.inaxes is None:
#         point = (-1,-1)
#     else:
#         point = (event.xdata, event.ydata)
#     print(point)
#     polygon.set_xy(np.column_stack(point))
#     plt.title('In point %i' % point[0])
#     event.canvas.draw()
# polygon = Polygon([[0, 0], [0, 0]], facecolor='y')  # dummy data for (xs, ys)

# 设置窗口大小


# 定义函数，给每一个patch都设置标签说明
def label(x, y, text):
    plt.text(x, y, text, ha="center", va="center",  size=8, alpha=0.5, weight="light")


def draw(link_matrix, label_list, value_list):
    plt.close()  # 先关闭上一个再重新打开
    fig = plt.figure("关键节点展示图", figsize=(7, 7))
    fig.patch.set_facecolor((0.2,0.2,0.2,0.2))
    # 点的个数
    num = len(label_list)

    angles = np.linspace(0, 2 * np.pi, num, endpoint=False)
    radii = 0.01
    x = (radii * np.cos(angles))
    y = (radii * np.sin(angles))
    # 画线
    for row in range(len(link_matrix)):
        for col in range(len(link_matrix[0])):
            if link_matrix[row][col] == 1 and row != col:
                xs = (x[row], x[col])
                ys = (y[row], y[col])
                plt.plot(xs, ys, color='blue', linewidth=0.2, zorder=-1)

    # 画点
    pointsize = [3000*c for c in value_list]
    # colormap内容见https://blog.csdn.net/lly1122334/article/details/88535217
    my_scatter = plt.scatter(x, y, s=pointsize, c=pointsize, cmap=plt.cm.Reds, picker=True, zorder=1)

    # text
    radii2 = 0.0105
    xs = (radii2 * np.cos(angles))
    ys = (radii2 * np.sin(angles))
    # 节点名称
    label_list1 = [c.split("+")[-1] for c in label_list]

    # 节点所在文件
    # label_list2 = [c.split("+")[0] for c in label_list]
    # for i in range(num):
    #     label(xs[i],ys[i],label_list1[i])

    # 箭头标注
    # for i in range(num):
    #     plt.annotate(s=label_list1[i], xy=(x[i], y[i]), xytext=(xs[i], ys[i]), arrowprops={"arrowstyle": "->"}, alpha=0.5)

    # 添加常见的图形对象。这些对象称为块(patch).完整的patch集合位于matplotlib.patches中
    # 绘制patch对象图形：plt.gca().add_patch(patch_name)
    # plt.gca().add_patch(polygon)
    # plt.gcf().canvas.mpl_connect('motion_notify_event', on_mouse_move)
    # plt.gcf().canvas.mpl_connect('scroll_event', on_mouse_scroll)
    # plt.gcf().canvas.mpl_connect('button_press_event', onclick)
    # plt.gcf().canvas.mpl_connect('motion_notify_event', onMotion)

    # 鼠标事件处理
    scale = Scale(fig, link_matrix, label_list, value_list)

    # 去掉边框
    plt.axis('off')

    # # 去掉边缘空白
    # fig.set_tight_layout(True)

    plt.show()
