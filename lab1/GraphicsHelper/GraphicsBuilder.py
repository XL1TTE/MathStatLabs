import matplotlib.pyplot as plt
import seaborn as sns
import math


class Graphics:

    class HistagramData:
        def __init__(self, heights: list[float | int], start_points: list[float | int], bar_width: float | int):
            self.Heights = heights
            self.StartPoints = start_points
            self.BarWidth = bar_width

            self.Shift_bar_start_points()

        Heights: list[float | int]
        StartPoints: list[float | int]
        BarWidth: float | int

        def Shift_bar_start_points(self):
            for point in range(0, len(self.StartPoints)):
                self.StartPoints[point] += self.BarWidth / 2

    @staticmethod
    def BuildLinierFigure(x: list, y: list, outpath: str, 
                           label_x: str = None, 
                           label_y: str = None,
                           color: str = 'black',
                           figure_title: str = "Scatter"):
        
        sns.set_theme(style='whitegrid')

        axes = plt.subplot()
        axes.plot(x, y, color=color, linewidth=2)
        axes.set_title(figure_title)
        axes.set_xlabel(label_x)
        axes.set_ylabel(label_y)

        plt.savefig(outpath)
        plt.close()

    @staticmethod
    def Compile_Data_For_Hist_Figure(x: list) :
        
        def InInterval(x: float, start: float, end: float) -> bool:
            return x >= start and x < end

        data = sorted(x)
        
        partition_count = 1 + int(3.322*math.log10(len(x))) 
        interval_lenght = (data[-1] - data[0]) / partition_count

        heights: list[float | int] = []  
        start_points: list[float | int] = []

        current = data[0]
        for i in range(partition_count):
            delta={"left": current, "right": current + interval_lenght}

            freq=sum(1 for x in data if InInterval(x, current, current + interval_lenght))

            height= freq / (len(data) * interval_lenght)

            heights.append(height)
            start_points.append(delta['left'])

            current += interval_lenght
        return Graphics.HistagramData(heights=heights, start_points=start_points, bar_width=interval_lenght)

    @staticmethod
    def BuildHistogramFigure(x: list, outpath: str):
        
        data: Graphics.HistagramData = Graphics.Compile_Data_For_Hist_Figure(x=x)
        
        plt.figure()

        plt.bar(x=data.StartPoints, height=data.Heights, width=data.BarWidth, color='black')

        sns.set_theme(style='whitegrid')
        plt.savefig(outpath)
        plt.close()

    @staticmethod
    def Build_Mixed_Hist_Linear_Figure(x: list, y: list, figure_title: str, outpath: str = "Mixed_plot.png"):
        data: Graphics.HistagramData = Graphics.Compile_Data_For_Hist_Figure(x=x)
        
        plt.figure()

        axes = plt.subplot()

        axes.plot(x, y, color='black', linewidth=2)
        axes.set_title(figure_title)
        
        plt.bar(x=data.StartPoints, height=data.Heights, width=data.BarWidth, color='blue')

        plt.savefig(outpath)
        plt.close()




