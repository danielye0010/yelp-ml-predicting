import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# read file
df = pd.read_csv('burgers_business.csv')

# missing data filled with 0
df.fillna(0, inplace=True)

# True/False to 1/0
df = df.replace({True: 1, False: 0})

# y - success metric
df['success_metric'] = df['stars'] * np.log(df['review_count'] + 1)
X = df.drop(['stars', 'review_count', 'success_metric'], axis=1)
y = df['success_metric']

# train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'Support Vector Regression': SVR()
}

performance = {}
# train 3 model
for name, model in models.items():
    model.fit(X_train, y_train)  # 训练模型
    y_pred = model.predict(X_test)  # 进行预测
    mse = mean_squared_error(y_test, y_pred)  # 计算均方误差
    r2 = r2_score(y_test, y_pred)  # 计算 R^2 分数
    performance[name] = {'MSE': mse, 'R2': r2}  # 存储性能指标

# metric to DataFrame
performance_df = pd.DataFrame(performance)
print(performance_df)

svr_model = SVR()
svr_model.fit(X, y)

# save bext svm to file
joblib.dump(svr_model, 'svr_model.joblib')