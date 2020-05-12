import pandas as pd
from sqlalchemy import create_engine
import numpy as np

URI = 'postgres://opqzovyyohuuia:2537236190151ec6c22687f68d4a016d092389178f489ade0c01000db792e8f3@ec2-50-17-90-177.compute-1.amazonaws.com:5432/ddbsga4dabbm0c'

engine = create_engine(URI)

conn = engine.connect()

# Execute a SQL query using pandas
#df = pd.read_sql_query('select 1', con=conn)

df = pd.DataFrame(np.random.rand(10,5))


# Write a pandas dataframe into the database
df.to_sql('table_name2', con=conn)



#conn.close()

#engine.dispose()


