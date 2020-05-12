import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import sklearn.gaussian_process as gp
from sklearn.gaussian_process.kernels import RBF, ConstantKernel



URI = 'postgres://opqzovyyohuuia:2537236190151ec6c22687f68d4a016d092389178f489ade0c01000db792e8f3@ec2-50-17-90-177.compute-1.amazonaws.com:5432/ddbsga4dabbm0c'

engine = create_engine(URI)
conn = engine.connect()

fname = 'prob1.xlsx'
df = pd.read_excel(fname)

# Write a pandas dataframe into the database
df.to_sql('prob1data', con=conn, if_exists='replace')

# Execute a SQL query using pandas
df = pd.read_sql_query('SELECT * FROM prob1data', con=conn, index_col='index', parse_dates='DATE')

X = df.DATE[:, None]
y = df.Variable_of_Interest
Xi = df.index[:, None]

X1, X2, y1, y2 = train_test_split(Xi, y, random_state=0, train_size=0.8)

ind1 = np.argsort(X1, axis=0)
ind2 = np.argsort(X2, axis=0)

X1 = X1[ind1].flatten()[:, None]
X2 = X2[ind2].flatten()[:, None]
y1 = y1.iloc[ind1[:,0]]
y2 = y2.iloc[ind2[:,0]]

kernel = gp.kernels.ConstantKernel(1.0, (1e-1, 1e3)) * gp.kernels.RBF(10.0, (1e-3, 1e3))
model = gp.GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10, alpha=0.1, normalize_y=False)
model.fit(X1, y1)
params = model.kernel_.get_params()
print(params)
y_pred, sigma = model.predict(X2, return_std=True)
MSE = ((y_pred-y2)**2).mean()
print('MSE =', MSE)
    
plt.figure()
plt.scatter(X1, y1, s=3.0, c='b', label=r'Train')
plt.scatter(X2, y_pred, s=3.0, c='r', label=r'Test')
plt.fill(np.concatenate([X2, X2[::-1]]),
         np.concatenate([y_pred - 1.9600 * sigma,
                        (y_pred + 1.9600 * sigma)[::-1]]),
         alpha=.5, fc='b', ec='None', label='95% confidence interval')
plt.xlabel('$Xi$')
plt.ylabel('$y$')
plt.ylim(-10, 20)
plt.legend(loc='upper left')
plt.show()

conn.close()

engine.dispose()


