import pandas as pd
from sqlalchemy import create_engine
import numpy as np

# Open DB connection
URI = 'postgres://opqzovyyohuuia:2537236190151ec6c22687f68d4a016d092389178f489ade0c01000db792e8f3@ec2-50-17-90-177.compute-1.amazonaws.com:5432/ddbsga4dabbm0c'
engine = create_engine(URI)
conn = engine.connect()

fname = 'prob2.xlsx'
df = pd.read_excel(fname)

# Write a pandas dataframe into the database
df.to_sql('prob2data', con=conn, if_exists='replace', index=False)

# Execute a SQL query using pandas
df = pd.read_sql_query('SELECT * FROM prob2data', con=conn)

# Tranform table and grab column names from first row
colnames = df.T.iloc[0]
df = df.T
df = df.drop('Unnamed: 0', axis=0)
df.columns = colnames
df.index = np.arange(df.shape[0])

# Do some data cleaning
df.loc[df['ca'] == 'No major Vessels', 'ca'] = 0
df['male'] = df['sex'] == 'MALE'
df['disease'] = df['target'] == 'Disease'
cols = ['age', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach',
       'exang', 'oldpeak', 'slope', 'ca', 'thal','male', 'disease']
for col in cols:
    df[col] = pd.to_numeric(df[col])
df['male'] = df['male'].astype(int)
df['disease'] = df['disease'].astype(int)
df = df.dropna(axis=0, how='any')
df = df.drop(labels=['sex','target'], axis=1)

# Write cleaned data to new data table
df.to_sql('prob2data_clean', con=conn, if_exists='replace', index=False)

# Close DB connection
conn.close()
engine.dispose()

