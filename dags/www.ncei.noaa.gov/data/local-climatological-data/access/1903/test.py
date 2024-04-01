import pandas as pd

df = pd.read_csv('02972099999.csv')

new_df = df.iloc[:,[1,2,3,8,9,10]]
new_df.iloc[:, 0] = new_df.iloc[:, 0].str[5:7]
new_df = new_df.groupby(['LATITUDE', 'LONGITUDE']).agg(list)

print(new_df.columns)
