import pandas as pd

series = pd.read_csv('DATA_trial', header=None, usecols=(0,1))

df = series.split(',')

print(df)