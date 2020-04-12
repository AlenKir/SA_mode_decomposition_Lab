import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# took data from 1880 to 1966... looks a bit more suited for this task
#                              ~~~ Алгоритм: ~~~
# найти к-во экстремумов?
# если больше двух, то
	# найти эти экстремумы и показать их на графике
	# построить огибающие
	# найти среднее между огибающими
	# вычесть это среднее из текущей кривой
	# таким образом получается новая текущая кривая, отобразить ее

# prep data

f = open("data.txt", 'r')
data = []
for line in f:
    s = [x for x in line.split(',')]
    if s[0] == "GCAG":
        data.append([int(s[1]), float(s[2])])

temp_by_year = np.transpose(data)
year = temp_by_year[0]
temperature = temp_by_year[1]

iterations = 1

while iterations < 5:
    print("Итерация {}".format(iterations))
    
    print("Years: {}".format(year))
    print("Temps: {}".format(temperature))
    plt.plot(year, temperature, label='data', color='blue')
    
    # for local maxima
    max_indexes = argrelextrema(temperature, np.greater)
    max_temperature = []
    max_year = []
    for each in max_indexes:
        max_temperature.append(temp_by_year[1][each])
        max_year.append(temp_by_year[0][each])
    # print(max_temperature)
    # print(max_year)
    plt.plot(max_year, max_temperature, "v", color='red')
    
    # for local minima
    min_indexes = argrelextrema(temperature, np.less)
    min_temperature = []
    min_year = []
    for each in min_indexes:
        min_temperature.append(temp_by_year[1][each])
        min_year.append(temp_by_year[0][each])
    plt.plot(min_year, min_temperature, "^", color='green')
    
    # correcting min and max format
    
    min_year = np.array(min_year[0])
    # print("min_year = ", min_year)
    min_temperature = np.array(min_temperature[0])
    # print("min_temperature = {}".format(min_temperature))
    
    max_year = np.array(max_year[0])
    max_temperature = np.array(max_temperature[0])
    
    min_year_r = min_year[::-1]
    min_temperature_r = min_temperature[::-1]
    max_year_r = max_year[::-1]
    max_temperature_r = max_temperature[::-1]
    
    if (len(max_year) <=3 or len(min_year) <=3):
        print("Выполнен критерий останова.Количество максимумов - {}, минимумов - {}."
              .format(len(max_year), len(min_year)))
        break
    
    # interpolation: min and max
    
    x = min_year_r
    y = min_temperature_r
    cubic_interp_min = interp1d(x, y, kind='cubic')
    xnew_min = np.linspace(min_year_r[0], min_year[0])
    plt.plot(xnew_min, cubic_interp_min(xnew_min), '--', label='min spline')
    
    x = max_year_r
    y = max_temperature_r
    cubic_interp_max = interp1d(x, y, kind='cubic')
    xnew_max = np.linspace(max_year_r[0], max_year[0])
    plt.plot(xnew_max, cubic_interp_max(xnew_max), '--', label='max spline')
    
    max_line = cubic_interp_max(xnew_max)
    min_line = cubic_interp_min(xnew_min)
    # print("Up line - {}, x - {}".format(max_line, xnew_max))
    # print("Bottom line - {}, x - {}".format(min_line, xnew_min))
    
    # print(len(max_line))
    # print(len(min_line))
    
    average = []
    for i in range(0, len(max_line)):
        average.append((min_line[i] + max_line[i])/2)
    # print(average)
    plt.plot(xnew_max, average, '-', label = 'average', color='black')
    plt.legend()
    plt.show()
    
    if xnew_max[0] < xnew_min[0]:
        year = np.array(xnew_max)
    else:
        year = np.array(xnew_min)
    temperature = np.array(average)
    temp_by_year = [year, temperature]
    
    iterations +=1
