import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from scipy import interpolate

# took data from 1880 to 1966... looks a bit more suited for this task
#                              ~~~ Алгоритм: ~~~
# найти к-во экстремумов? можно ли вообще это как-то математически сделать... 
# смена знака производной?.. но тут как бы нет функции
# если больше двух, то
	# найти эти экстремумы и показать их на графике
	# построить огибающие
	# найти среднее между огибающими
	# вычесть это среднее из текущей кривой
	# таким образом получается новая текущая кривая, отобразить ее

f = open("data.txt", 'r')
data = []
for line in f:
    s = [x for x in line.split(',')]
    if s[0] == "GCAG":
        data.append([int(s[1]), float(s[2])])

temp_by_year = np.transpose(data)
year = temp_by_year[0]
temperature = temp_by_year[1]

plt.plot(year, temperature, color='blue')

# for local maxima
max_indexes = argrelextrema(temperature, np.greater)
max_temperature = []
max_year = []
for each in max_indexes:
    max_temperature.append(temp_by_year[1][each])
    max_year.append(temp_by_year[0][each])
print(max_temperature)
print(max_year)
plt.plot(max_year, max_temperature, "v", label="max", color='red')

# for local minima
min_indexes = argrelextrema(temperature, np.less)
min_temperature = []
min_year = []
for each in min_indexes:
    min_temperature.append(temp_by_year[1][each])
    min_year.append(temp_by_year[0][each])

# min interpolation

min_year = np.array(min_year[0])
# print("min_year = ", min_year)
min_temperature = np.array(min_temperature[0])
print("min_temperature = ", min_temperature)

plt.plot(min_year, min_temperature, "^", label="max", color='green')

min_year_r = min_year[::-1]
min_temperature_r = min_temperature[::-1]
tck_min = interpolate.splrep(min_year_r, min_temperature_r)
# print(tck)

plt.plot(tck_min[0], tck_min[1], "-", label="interp", color='yellow')

# max interpolation

max_year = np.array(max_year[0])
# print("max_year = ", max_year)
max_temperature = np.array(max_temperature[0])
# print("max_temperature = ", max_temperature)

max_year_r = max_year[::-1]
max_temperature_r = max_temperature[::-1]
tck_max = interpolate.splrep(max_year_r, max_temperature_r)
print(tck_max)

plt.plot(tck_max[0], tck_max[1], "-", label="interp", color='pink')

plt.show()