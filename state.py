import pandas as pd
import numpy as np

path_to_average_by_state = 'average_by_state.csv'

# load
df_merged = pd.read_csv(path_to_average_by_state)
numeric_columns = df_merged.select_dtypes(include='number').columns
state_columns = numeric_columns.drop(['stars', 'review_count'])

# corr
correlations1 = df_merged[numeric_columns].corr().loc['stars', state_columns]
correlations2 = df_merged[numeric_columns].corr().loc['review_count', state_columns]

print(correlations1)
print(correlations2)


# min max median success metric print
df = pd.read_csv('burgers_business_state.csv')
df.fillna(0, inplace=True)  # 缺失值用0填充
df = df.replace({True: 1, False: 0})
df['success_metric'] = df['stars'] * np.log(df['review_count'] + 1)
X = df.drop(['stars', 'review_count', 'success_metric'], axis=1)
y = df['success_metric']

max_success_metric = df['success_metric'].max()

min_success_metric = df['success_metric'].min()

median_success_metric = df['success_metric'].median()

mean_success_metric = df['success_metric'].mean()

state_stats = df.groupby('state')['success_metric'].agg(['max', 'min', 'median', 'mean']).reset_index()

state_stats.columns = ['state', 'max_success_metric', 'min_success_metric', 'median_success_metric', 'mean_success_metric']

pd.set_option('display.max_columns', None)
print(state_stats)