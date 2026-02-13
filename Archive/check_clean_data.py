import pandas as pd

df = pd.read_excel('PEG 12H allowance - FY2025 (Clean).xlsx')

print('First row data:')
print('=' * 80)
for col in df.columns:
    value = df.iloc[0][col]
    print(f'{col}: {value}')

print('\n' + '=' * 80)
print(f'Total rows: {len(df)}')
print(f'\nTotal Renumeration column data type: {df["Total Renumeration"].dtype}')
print(f'First 5 values in Total Renumeration: {df["Total Renumeration"].head().tolist()}')
