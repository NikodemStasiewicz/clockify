import pandas as pd
from openpyxl import Workbook
import os

csv_file = 'Clockify_Time_Report_Detailed_28_08_2023-03_09_2023.csv'
df = pd.read_csv(csv_file)

df['Duration (timedelta)'] = pd.to_timedelta(df['Duration (h)'])

pivot_df = df.pivot_table(values='Duration (timedelta)', index='User', columns='Project', aggfunc='sum', fill_value=pd.Timedelta(seconds=0))

pivot_df = pivot_df.apply(lambda x: x / pd.Timedelta(hours=1))

pivot_df['Total Hours'] = pivot_df.sum(axis=1)

excel_filename = 'summed_clockify_data.xlsx'
wb = Workbook()
ws = wb.active
ws.title = 'Summed Clockify Data'

headers = list(pivot_df.columns)
ws.append(['User'] + headers)  

for index, row in pivot_df.iterrows():
    data_row = [index] + [row[col] for col in headers]
    ws.append(data_row)

wb.save(excel_filename)
print(f"Summed data saved to {excel_filename}")

os.system(excel_filename)
