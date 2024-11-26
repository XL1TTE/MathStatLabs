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



partition_first_fx_theory_x, partition_first_fx_theory_y  = MathStatistics.Distributions.Normal_Distribution.Generate_pdf_data(expectation=partition_first_mean, variance=partition_first_variance_NoShifted)
partition_first_fx_theory_buildData =  GraphicsBuilder.Graphics.BuildData(partition_first_fx_theory_x, partition_first_fx_theory_y, color='Yellow')
partition_first_fx_histogram_data = GraphicsBuilder.Graphics.Calculate_data_for_Histagram(partition_first_data)

partition_second_fx_theory_x, partition_second_fx_theory_y  = MathStatistics.Distributions.Normal_Distribution.Generate_pdf_data(expectation=partition_second_mean, variance=partition_second_variance_NoShifted)
partition_second_fx_theory_buildData =  GraphicsBuilder.Graphics.BuildData(partition_second_fx_theory_x, partition_second_fx_theory_y, color='Red')
partition_second_fx_histogram_data = GraphicsBuilder.Graphics.Calculate_data_for_Histagram(partition_second_data)

partition_third_fx_theory_x, partition_third_fx_theory_y  = MathStatistics.Distributions.Normal_Distribution.Generate_pdf_data(expectation=partition_third_mean, variance=partition_third_variance_NoShifted)
partition_third_fx_theory_buildData =  GraphicsBuilder.Graphics.BuildData(partition_third_fx_theory_x, partition_third_fx_theory_y, color='Blue')
partition_third_fx_histogram_data = GraphicsBuilder.Graphics.Calculate_data_for_Histagram(partition_third_data)


GraphicsBuilder.Graphics.Build_Mixed_Hist_Linear_Figure([partition_first_fx_histogram_data], [partition_first_fx_theory_buildData] ,outpath="Images//FirstPartition//histogram_theoryfx.png")
GraphicsBuilder.Graphics.Build_Mixed_Hist_Linear_Figure([partition_second_fx_histogram_data], [partition_second_fx_theory_buildData] ,outpath="Images//SecondPartition//histogram_theoryfx.png")
GraphicsBuilder.Graphics.Build_Mixed_Hist_Linear_Figure([partition_third_fx_histogram_data], [partition_third_fx_theory_buildData] ,outpath="Images//ThirdPartition//histogram_theoryfx.png")


partition_first_Fx_theory_x, partition_first_Fx_theory_y = MathStatistics.Distributions.Normal_Distribution.Generate_cdf_data(expectation=partition_first_mean, variance=partition_first_variance_NoShifted)
partition_first_Fx_theory_buildData =  GraphicsBuilder.Graphics.BuildData(partition_first_Fx_theory_x, partition_first_Fx_theory_y, color='Yellow')

partition_first_sample_Fx = [MathStatistics.Distributions.Normal_Distribution.Cumulative_distribuion_function_emp(x, partition_first_data) for x in partition_first_data]
partition_first_sample_Fx_Build_Data = GraphicsBuilder.Graphics.BuildData(partition_first_data, partition_first_sample_Fx)
GraphicsBuilder.Graphics.Build_Mixed_Linear_Step_Figure([partition_first_sample_Fx_Build_Data], [partition_first_Fx_theory_buildData], outpath="Images//FirstPartition//Fx_theory_sample.png")


partition_second_Fx_theory_x, partition_second_Fx_theory_y = MathStatistics.Distributions.Normal_Distribution.Generate_cdf_data(expectation=partition_second_mean, variance=partition_second_variance_NoShifted)
partition_second_Fx_theory_buildData =  GraphicsBuilder.Graphics.BuildData(partition_second_Fx_theory_x, partition_second_Fx_theory_y, color='Red')

partition_second_sample_Fx = [MathStatistics.Distributions.Normal_Distribution.Cumulative_distribuion_function_emp(x, partition_second_data) for x in partition_second_data]
partition_second_sample_Fx_Build_Data = GraphicsBuilder.Graphics.BuildData(partition_second_data, partition_second_sample_Fx)
GraphicsBuilder.Graphics.Build_Mixed_Linear_Step_Figure([partition_second_sample_Fx_Build_Data], [partition_second_Fx_theory_buildData], outpath="Images//SecondPartition//Fx_theory_sample.png")

partition_third_Fx_theory_x, partition_third_Fx_theory_y = MathStatistics.Distributions.Normal_Distribution.Generate_cdf_data(expectation=partition_third_mean, variance=partition_third_variance_NoShifted)
partition_third_Fx_theory_buildData =  GraphicsBuilder.Graphics.BuildData(partition_third_Fx_theory_x, partition_third_Fx_theory_y, color='Blue')

partition_third_sample_Fx = [MathStatistics.Distributions.Normal_Distribution.Cumulative_distribuion_function_emp(x, partition_third_data) for x in partition_third_data]
partition_third_sample_Fx_Build_Data = GraphicsBuilder.Graphics.BuildData(partition_third_data, partition_third_sample_Fx)
GraphicsBuilder.Graphics.Build_Mixed_Linear_Step_Figure([partition_third_sample_Fx_Build_Data], [partition_third_Fx_theory_buildData], outpath="Images//ThirdPartition//Fx_theory_sample.png")


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

partition_first_CI_SL_BuildData = GraphicsBuilder.Graphics.BuildData(x, y, color='Yellow')

x,y = MathStatistics.Get_MeanConfidenceIntervalLenght_SignificanceLevel_Relation_Data(partition_second_data, partition_second_mean, partition_second_variance_NoShifted)

partition_second_CI_SL_BuildData = GraphicsBuilder.Graphics.BuildData(x, y, color='red')

x,y = MathStatistics.Get_MeanConfidenceIntervalLenght_SignificanceLevel_Relation_Data(partition_third_data, partition_third_mean, partition_third_variance_NoShifted)
partition_third_CI_SL_BuildData = GraphicsBuilder.Graphics.BuildData(x, y, color='blue')


DataBuilds = [partition_first_CI_SL_BuildData, partition_second_CI_SL_BuildData, partition_third_CI_SL_BuildData]

GraphicsBuilder.Graphics.Build_Many_Linear_InOne_Plot(DataBuilds, outpath="CI_lenght.png") 


