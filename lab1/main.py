from CsvHelper import Managers
from dataclasses import dataclass

from MathHelper import MathStatistics

from GraphicsHelper import GraphicsBuilder

import numpy

@dataclass
class DataSample:
    value: float
    frequency: int

data = Managers.CsvManager.Scenaries.ReadInType(filepath="test1.csv", OutType=DataSample)

data = [float(x.value) for x in data]

partition_first_data = sorted(data[:10])
partition_second_data = sorted(data[:50])
partition_third_data = sorted(data)
del data

partition_first_mean = MathStatistics.GetExpectedValue(partition_first_data)
partition_second_mean = MathStatistics.GetExpectedValue(partition_second_data)
partition_third_mean = MathStatistics.GetExpectedValue(partition_third_data)

partition_first_variance_NoShifted = MathStatistics.GetVariance_NoShifted(partition_first_data)
partition_second_variance_NoShifted = MathStatistics.GetVariance_NoShifted(partition_second_data)
partition_third_variance_NoShifted = MathStatistics.GetVariance_NoShifted(partition_third_data)

partition_first_variance_Shifted = MathStatistics.GetVariance_Shifted(partition_first_data)
partition_second_variance_Shifted = MathStatistics.GetVariance_Shifted(partition_second_data)
partition_third_variance_Shifted = MathStatistics.GetVariance_Shifted(partition_third_data)

# quartiles = [0, 0.25, 0.5, 0.75, 1]

# print(MathStatistics.Get_median_value_for_sample(partition_third_data))
# print(MathStatistics.GetExpectedValue(partition_third_data))
# for q in quartiles:
#     print(MathStatistics.Get_Nth_Quantile(partition_third_data, p=q), q)

partition_first_fx = [MathStatistics.Distributions.Normal_Distribution.Probability_density_function(x, partition_first_mean, partition_first_variance_NoShifted) for x in partition_first_data]
partition_first_buildData =  GraphicsBuilder.Graphics.BuildData(partition_first_data, partition_first_fx, color='Yellow')

partition_second_fx = [MathStatistics.Distributions.Normal_Distribution.Probability_density_function(x, partition_second_mean, partition_second_variance_NoShifted) for x in partition_second_data]
partition_second_buildData =  GraphicsBuilder.Graphics.BuildData(partition_second_data, partition_second_fx, color='Red')

partition_third_fx = [MathStatistics.Distributions.Normal_Distribution.Probability_density_function(x, partition_third_mean, partition_third_variance_NoShifted) for x in partition_third_data]
partition_third_buildData =  GraphicsBuilder.Graphics.BuildData(partition_third_data, partition_third_fx, color='Blue')


BuildDatas_probability_density_functions = [partition_first_buildData, partition_second_buildData, partition_third_buildData]

# GraphicsBuilder.Graphics.Build_Many_Linear_InOne_Plot(BuildDatas=BuildDatas_probability_density_functions, outpath="Images//Combined_samples_prob_func.png", label_x="Values", label_y="Probability")

# GraphicsBuilder.Graphics.BuildHistogramFigure(partition_first_data, outpath="Images//FirstPartition//first_sample_hist.png")
# GraphicsBuilder.Graphics.BuildHistogramFigure(partition_second_data, outpath="Images//SecondPartition//second_sample_hist.png")
# GraphicsBuilder.Graphics.BuildHistogramFigure(partition_third_data, outpath="Images//ThirdPartition//third_sample_hist.png")


# GraphicsBuilder.Graphics.Build_Mixed_Hist_Linear_Figure(partition_first_data, partition_first_fx, outpath="Images//FirstPartition//first_sample_hist_linear.png")
# GraphicsBuilder.Graphics.Build_Mixed_Hist_Linear_Figure(partition_second_data, partition_second_fx, outpath="Images//SecondPartition//second_sample_hist_linear.png")
# GraphicsBuilder.Graphics.Build_Mixed_Hist_Linear_Figure(partition_third_data, partition_third_fx, outpath="Images//ThirdPartition//third_sample_hist_linear.png")


partition_first_fx = [MathStatistics.Distributions.Normal_Distribution.Cumulative_distribution_function(x, partition_first_mean, partition_first_variance_NoShifted) for x in partition_first_data]
partition_first_buildData =  GraphicsBuilder.Graphics.BuildData(partition_first_data, partition_first_fx, color='Yellow')

partition_second_fx = [MathStatistics.Distributions.Normal_Distribution.Cumulative_distribution_function(x, partition_second_mean, partition_second_variance_NoShifted) for x in partition_second_data]
partition_second_buildData =  GraphicsBuilder.Graphics.BuildData(partition_second_data, partition_second_fx, color='Red')

partition_third_fx = [MathStatistics.Distributions.Normal_Distribution.Cumulative_distribution_function(x, partition_third_mean, partition_third_variance_NoShifted) for x in partition_third_data]
partition_third_buildData =  GraphicsBuilder.Graphics.BuildData(partition_third_data, partition_third_fx, color='Blue')

BuildDatas_cumulative_functions = [partition_first_buildData, partition_second_buildData, partition_third_buildData]

# GraphicsBuilder.Graphics.Build_Many_Linear_InOne_Plot(BuildDatas=BuildDatas_cumulative_functions, outpath="Images//Combined_sample_cumulative_func.png", label_x="Values", label_y="Probabilities")


partition_first_Mean_CI = MathStatistics.Get_ConfidenceInterval_of_Mean(partition_first_data, 0.05, partition_first_mean, partition_first_variance_NoShifted)
partition_first_Variance_CI = MathStatistics.Get_ConfidenceInterval_of_Variance(partition_first_data, 0.05, partition_first_variance_NoShifted)

partition_second_Mean_CI = MathStatistics.Get_ConfidenceInterval_of_Mean(partition_second_data, 0.05, partition_second_mean, partition_second_variance_NoShifted)
partition_second_Variance_CI = MathStatistics.Get_ConfidenceInterval_of_Variance(partition_second_data, 0.05, partition_second_variance_NoShifted)

partition_third_Mean_CI = MathStatistics.Get_ConfidenceInterval_of_Mean(partition_third_data, 0.05, partition_third_mean, partition_third_variance_NoShifted)
partition_third_Variance_CI = MathStatistics.Get_ConfidenceInterval_of_Variance(partition_third_data, 0.05, partition_third_variance_NoShifted)


print(f"Для первой выборки:\nВыборочное среднее: {partition_first_mean}\nВыборочная несмещенная дисперсия: {partition_first_variance_NoShifted}\nДоверительный интервал для математического ожидания: ({partition_first_Mean_CI.a}, {partition_first_Mean_CI.b})\nДоверительный интервал для дисперсии: ({partition_first_Variance_CI.a}, {partition_first_Variance_CI.b})")

print(f"Для второй выборки:\nВыборочное среднее: {partition_second_mean}\nВыборочная несмещенная дисперсия: {partition_second_variance_NoShifted}\nДоверительный интервал для математического ожидания: ({partition_second_Mean_CI.a}, {partition_second_Mean_CI.b})\nДоверительный интервал для дисперсии: ({partition_second_Variance_CI.a}, {partition_second_Variance_CI.b})")

print(f"Для третьей выборки:\nВыборочное среднее: {partition_third_mean}\nВыборочная несмещенная дисперсия: {partition_third_variance_NoShifted}\nДоверительный интервал для математического ожидания: ({partition_third_Mean_CI.a}, {partition_third_Mean_CI.b})\nДоверительный интервал для дисперсии: ({partition_third_Variance_CI.a}, {partition_third_Variance_CI.b})")



x,y = MathStatistics.Get_MeanConfidenceIntervalLenght_SignificanceLevel_Relation_Data(partition_first_data, partition_first_mean, partition_first_variance_NoShifted)

partition_first_MeanConfidenceIL_SignificaneLevel_BuildData = GraphicsBuilder.Graphics.BuildData(x, y, color='Yellow')

x,y = MathStatistics.Get_MeanConfidenceIntervalLenght_SignificanceLevel_Relation_Data(partition_second_data, partition_second_mean, partition_second_variance_NoShifted)

partition_second_MeanConfidenceIL_SignificaneLevel_BuildData = GraphicsBuilder.Graphics.BuildData(x, y, color='red')

x,y = MathStatistics.Get_MeanConfidenceIntervalLenght_SignificanceLevel_Relation_Data(partition_third_data, partition_third_mean, partition_third_variance_NoShifted)
partition_third_MeanConfidenceIL_SignificaneLevel_BuildData = GraphicsBuilder.Graphics.BuildData(x, y, color='blue')


DataBuilds = [partition_first_MeanConfidenceIL_SignificaneLevel_BuildData, partition_second_MeanConfidenceIL_SignificaneLevel_BuildData, partition_third_MeanConfidenceIL_SignificaneLevel_BuildData]

GraphicsBuilder.Graphics.Build_Many_Scatter_InOne_Plot(DataBuilds, outpath="test.png") 
