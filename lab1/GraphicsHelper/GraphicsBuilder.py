import matplotlib.pyplot as plt
import math


class Graphics:


    class BuildData:
        def __init__(self, x, y, color:str = "black"):
            self.X = x
            self.Y = y
            self.Color = color
        X: list[float | int]
        Y: list[float | int]
        Color: str

    class HistogramData:
        def __init__(self, heights: list[float | int], start_points: list[float | int], bar_width: float | int, color: str = 'Black'):
            self.Heights = heights
            self.StartPoints = start_points
            self.BarWidth = bar_width
            self.Color = color

            self.Shift_bar_start_points()

        Heights: list[float | int]
        StartPoints: list[float | int]
        BarWidth: float | int

        def Shift_bar_start_points(self):
            for point in range(0, len(self.StartPoints)):
                self.StartPoints[point] += self.BarWidth / 2

    @staticmethod
    def BuildLinierFigure( data: BuildData,
                           outpath: str | None = None,
                           label_x: str = None, 
                           label_y: str = None,
                           figure_title: str = "Scatter",):
        
        plt.figure()
        
        plt.title(figure_title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)


        x,y = data.X, data.Y
        plt.plot(x, y, color=data.Color, linewidth=2)

        if(outpath != None):
            plt.savefig(outpath)
            plt.close()
        else:
            plt.show()
            plt.close()


    @staticmethod
    def BuildStepFigure( data: BuildData,
                           outpath: str | None = None,
                           label_x: str = None, 
                           label_y: str = None,
                           figure_title: str = "Scatter",):
        
        plt.figure()
        
        plt.title(figure_title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)


        x,y = data.X, data.Y
        plt.step(x, y, color=data.Color, linewidth=2)

        if(outpath != None):
            plt.savefig(outpath)
            plt.close()
        else:
            plt.show()
            plt.close()

    @staticmethod
    def Calculate_data_for_Histagram(values: list) :

        data = sorted(values)
        
        partition_count = 1 + int(3.322*math.log10(len(values))) 
        
        interval_lenght = (data[-1] - data[0]) / partition_count

        heights: list[float | int] = []  
        start_points: list[float | int] = []

        current = data[0]
        for i in range(partition_count):
            delta={"left": current, "right": current + interval_lenght}

            freq=sum(1 for x in data if (x >= current and x < current + interval_lenght))

            height= freq / (len(data) * interval_lenght)

            heights.append(height)
            start_points.append(delta['left'])

            current += interval_lenght
        return Graphics.HistogramData(heights=heights, start_points=start_points, bar_width=interval_lenght)

    @staticmethod
    def BuildHistogramFigure(hist_data: HistogramData, figure_title:str = "Historgram", label_x: str = "X", label_y:str = "Y", outpath: str | None = None, color: str = 'Black'):
        
        plt.figure()

        plt.bar(x=hist_data.StartPoints, height=hist_data.Heights, width=hist_data.BarWidth, color=color)

        if(outpath != None):
            plt.savefig(outpath)
            plt.close()
        else:
            plt.show()
            plt.close()

    @staticmethod
    def Build_Mixed_Hist_Linear_Figure(hist_data: list[HistogramData], linear_build_data: list[BuildData], figure_title: str = "Plot", outpath: str | None = None,
                                       label_y: str = "Y", label_x: str = "X"):
        
        plt.figure()

        plt.title(figure_title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)

        for data in hist_data:
            start_points, heights, bar_width = data.StartPoints, data.Heights, data.BarWidth
            plt.bar(x=start_points, height=heights, width=bar_width, color=data.Color)

        for data in linear_build_data:
            x, y = data.X, data.Y
            plt.plot(x, y, color=data.Color, linewidth=2)

        if(outpath != None):
            plt.savefig(outpath)
            plt.close()

        else:
            plt.show()
            plt.close()

    @staticmethod
    def Build_Mixed_Linear_Step_Figure(step_data: list[BuildData], linear_build_data: list[BuildData], figure_title: str = "Plot", outpath: str | None = None,
                                       label_y: str = "Y", label_x: str = "X"):
        
        plt.figure()

        plt.title(figure_title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)

        for data in step_data:

            plt.step(x=data.X, y=data.Y, color=data.Color, linewidth=2)

        for data in linear_build_data:
            x, y = data.X, data.Y
            plt.plot(x, y, color=data.Color, linewidth=2)

        if(outpath != None):
            plt.savefig(outpath)
            plt.close()

        else:
            plt.show()
            plt.close()

    @staticmethod
    def Build_Many_Linear_InOne_Plot(BuildDatas: list[BuildData], outpath: str | None = None, title: str = "Plot", label_x: str = "X", label_y:str = "Y"):

        plt.figure()

        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)

        for data in BuildDatas:
            plt.plot(data.X, data.Y, color=data.Color, linewidth=2)
            

        if(outpath != None):   
            plt.savefig(outpath)
            plt.close()
        else:
            plt.show()
            plt.close()

    @staticmethod
    def Build_Many_Scatter_InOne_Plot(BuildDatas: list[BuildData], outpath: str | None = None, title: str = "Plot", label_x: str = "X", label_y:str = "Y"):

        plt.figure()

        plt.title(title)
        plt.xlabel(label_x)
        plt.ylabel(label_y)

        for data in BuildDatas:

            plt.scatter(data.X, data.Y, color=data.Color, linewidth=2)

        if(outpath != None):
            plt.savefig(outpath)
            plt.close()
        else:
            plt.show()
            plt.close()
