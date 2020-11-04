import sys
import os
import pathlib
import pandas as pd
import datetime
file = sys.argv[1]
import numpy as np
import sklearn.preprocessing as preprocessing
import matplotlib.pyplot as plt


# check if file exists
# if not os.path.isfile(os.path.join(path, "{file}")):
if not os.path.isfile(f'./{file}'):
    print("[!] File doesn't exist. ")
    sys.exit(0)


print(pathlib.Path(file).suffix.lower())
# Make sure its a CSV file
if not pathlib.Path(file).suffix.lower() == ".csv":
    print("[!] Not a CSV file ")
    sys.exit(0)
else:
    df_old = pd.read_csv(file, header=None, index_col=False)



    
starttime = input("> Enter starttime:\n  Accepted format is 'YYYY-MM-DD HH:mm:ss'\n? ")

try:
    starttime_dt = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S")
    pass
except:
    breakpoint()
    print("[!] Datetime not entered correctly")

interval = input("> Simulation Interval:\n  Example acceptable values:\n  1h, 10s, 5m, i.e. any other integer value followed by h,d,s or m\n? ")
time_domain = interval[-1].strip()

if time_domain not in ['h', 'm','s']:
    print("[!] Bad format. Enter simulation step such that the last character is one of 'h', 'm',or 's' ")
    sys.exit(0)
try:
    # interval_val = [int(s) for s in interval.split() if s.isdigit()][0]
    interval_val = int(interval.split(time_domain)[0])
except:
    breakpoint()

# Number of rows to make:
rows_to_make = 0
if time_domain == 'm':
    rows_to_make = int(1440/interval_val)
elif time_domain == 's':
    rows_to_make = int(1440*60/interval_val)
elif time_domain == 'h':
    rows_to_make = int(24/interval_val)
else:
    pass

count = 1
col_1 = [starttime]

col_2 = df_old.iloc[:,1].tolist()

col_2 = preprocessing.minmax_scale(col_2, feature_range=(0, 1), axis=0, copy=True)

while count <= rows_to_make:
    col_1.append(f'+{interval_val}{time_domain}')
    count += 1

# Polyfitting the data

x_col = np.arange(len(col_2))


x = np.arange(rows_to_make)
z = np.polyfit(x_col, col_2, 8)

x = preprocessing.minmax_scale(x, feature_range=(0, rows_to_make), axis=0, copy=True)
eqn = np.poly1d(z)
y_new = []
for x_val in x:
    y_new.append(eqn(x_val))

y_new = preprocessing.minmax_scale(x, feature_range=(0, 1), axis=0, copy=True)


assert len(y_new) == len(x)

name_of_playerfile = input("> Player file name (dont provide extension.\n  It will automatically have *.player extension\n? ")

op = open(f'{name_of_playerfile}.player', 'w+')


for i in range(len(x)):
    op.write(f"{col_1[i]},{y_new[i]}\n")