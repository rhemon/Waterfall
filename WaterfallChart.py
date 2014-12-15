from Tkinter import *

# TODO Responsive Design for Negative Value


class Window(Frame):

    eachPixVal = 0
    canvas = None
    labelWidth = 0
    labelHeight = 0

    def __init__(self, master=None, windowTitle='GUI'):
        self.master = master
        self.windowTitle = windowTitle
        Frame.__init__(self, master)

    def init_win_title(self, windowTitle=''):
        if windowTitle:
            self.master.title(windowTitle)
        else:
            self.master.title(self.windowTitle)
        self.pack(fill=BOTH, expand=1)

    def init_canvas(self, x, y):
        self.canvas = Canvas(self.master, width=600, height=600)

    def init_graph(self, x, y, xLabel, yLabel, title):
        # Drawing lines
        lineY = self.canvas.create_line(50,50,50,550, fill='black')
        lineX = self.canvas.create_line(50,550,550,550, fill='black')

        # Drawing the title
        if title:
            frame = Frame(self.canvas, height=20)
            frame.place(x=220, y=0)
            newLabel = Label(frame, text=title)
            newLabel.pack(fill=BOTH, expand=1)

        # Drawing XLABEL and YLABEL
        if xLabel:
            frame = Frame(self.canvas, height=20)
            frame.place(x=30, y=10)
            newLabel = Label(frame, text=xLabel)
            newLabel.pack(fill=BOTH, expand=1)
        if yLabel:
            frame = Frame(self.canvas, height=20)
            frame.place(x=250, y=585)
            newLabel = Label(frame, text=yLabel)
            newLabel.pack(fill=BOTH, expand=1)


        # Setting up X Axis
        self.labelWidth = (500-(15*len(x)))/len(x)
        start = 50
        for label in x:
            frame = Frame(self.canvas, width=self.labelWidth, height=30)
            frame.place(x=start, y=560)
            newLabel = Label(frame, text=label)
            newLabel.pack(fill=BOTH, expand=1)
            start += self.labelWidth+15

        # Setting up Y Axis
        self.eachPixVal = max(y)/500.0
        startVal = 0
        posX = 5
        posY = 550
        incrementVal = max(y)/len(y)
        self.labelHeight = incrementVal/self.eachPixVal
        numberOfVal = len(y)+1
        while numberOfVal > 0:
            frame = Frame(self.canvas, width=30, height=self.labelHeight)
            frame.place(x=posX, y=posY-12)
            line = self.canvas.create_line(50, posY, 550, posY, dash=(4,4))
            newLabel = Label(frame, text=startVal)
            newLabel.pack(fill=BOTH, expand=1)
            startVal += incrementVal
            posY -= self.labelHeight
            numberOfVal -= 1


    def init_plots(self, y):
        x0 = 50
        last = 0
        y0 = 550
        for each in y:
            width = self.labelWidth

            if each > last:
                height = (each-last)/self.eachPixVal
                rect = self.canvas.create_rectangle(x0,y0,x0+width,y0-height,fill='green')
                line = self.canvas.create_line(x0+width, y0-height, x0+width+15, y0-height, fill='#000088')
                frame = Frame(self.canvas, width=width)
                center=width/2
                frame.place(x=x0+center-(20), y=y0-height+5)
                label = Label(frame, text='+'+str(each-last), fg='white', bg='green')
                label.pack(fill=BOTH, expand=1)
                y0 -= height
            elif each == last:
                height =  last/self.eachPixVal
                rect = self.canvas.create_rectangle(x0,550,x0+width,550-height,fill='blue')
                frame = Frame(self.canvas, width=width)
                center=width/2
                frame.place(x=x0+center-(20), y=550-height+5)
                label = Label(frame, text=last, fg='white', bg='blue')
                label.pack(fill=BOTH, expand=1)
            else:
                height =  (last-each)/self.eachPixVal
                rect = self.canvas.create_rectangle(x0, y0, x0+width, y0+height, fill='red')
                line = self.canvas.create_line(x0+width, y0+height, x0+width+15, y0+height, fill='#000088')
                frame = Frame(self.canvas, width=width)
                center=width/2
                frame.place(x=x0+center-(20), y=(y0+height-25))
                label = Label(frame, text=str(each-last), bg='red', fg='white')
                label.pack(fill=BOTH, expand=1)
                y0 += height

            x0 += width + 15
            last = each


    def pack_canvas(self):
        self.canvas.place(x=0, y=0)


class WaterfallDataError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Waterfall():
    """
    This class is the parent class for both WaterfallXY and WaterfallCF
    Because this class doesn't initialize plots, it only does in the children classes.
    """

    isInitTitleCalled = False

    def __init__(self, data, title='', winTitle='Waterfall Graph', total=True):
        self.total = total
        self.winTitle = winTitle
        self.title = title
        self.root = Tk()
        self.app = Window(master=self.root)
        try:
            self.x = data['x']
            self.y = data['y']
            self.xLabel = data['xLabel']
            self.yLabel = data['yLabel']
        except KeyError, e:
            raise WaterfallDataError(e.message + ' is not entered in data')

        if type(self.x) != list or type(self.y) != list:
            raise WaterfallDataError("The Data for X and Y are not list")
        elif len(self.x) != len(self.y) and not self.total:
            raise WaterfallDataError("X doesn't have the same amount of data as Y")

        self._init_plots()

    def _init_plots(self):
        pass

    def config_title(self, winTitle=''):
        if winTitle:
            self.winTitle = winTitle
        self.app.init_win_title(self.winTitle)
        self.isInitTitleCalled = True

    def display(self):
        if not self.isInitTitleCalled:
            self.app.init_win_title(self.winTitle)

        self.__init_window()
        self.root.mainloop()

    def __init_window(self):
        self.root.geometry("600x620")
        self.root.resizable(False, False)
        self.app.init_canvas(self.x, self.y)
        self.app.init_graph(self.x, self.y, self.xLabel, self.yLabel, self.title)
        self.app.init_plots(self.y)
        self.app.pack_canvas()


class WaterfallXY(Waterfall):
    def _init_plots(self):
        if self.total:
            if len(self.x) > len(self.y):
                self.y.append(self.y[-1])
            else:
                if self.y[-1] != self.y[-2]:
                    raise WaterfallDataError("Total Value seems to be invalid index -2 doesn't match index -1")

def form_yPlots(y):
    yPlots = []
    start = 0
    for each in y:
        start += each
        yPlots.append(start)
    return yPlots


class WaterfallA(Waterfall):
    def _init_plots(self):
        if self.total:
            if len(self.x) > len(self.y):
                self.y.append(0)
                self.y = form_yPlots(self.y)
            else:
                if self.y[-1] != 0:
                    raise WaterfallDataError("Last Value for your amount should be 0, as it will be the total for that case")
                self.y = form_yPlots(self.y)
