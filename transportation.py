import pandas as pd

# Load the data
file_path = r"C:\Users\Daniel Ye\Desktop\yelp_Fall2023\yelp_Fall2023\Trips_by_Distance.csv"
df = pd.read_csv(file_path)

df['Date'] = pd.to_datetime(df['Date'])

# Filter the DataFrame to include only the relevant columns
columns_of_interest = ['Date', 'State Postal Code', 'Population Not Staying at Home',
                       'Number of Trips', 'Number of Trips <1', 'Number of Trips 1-3',
                       'Number of Trips 3-5', 'Number of Trips 5-10', 'Number of Trips 10-25',
                       'Number of Trips 25-50', 'Number of Trips 50-100', 'Number of Trips 100-250',
                       'Number of Trips 250-500', 'Number of Trips >=500']
df = df[columns_of_interest]

# Group by 'State Postal Code' and calculate the mean for each group
df_avg = df.groupby('State Postal Code').mean()

# If you're not interested in Date anymore, you can drop it after grouping.
df_avg = df_avg.drop('Date', axis=1)

# Reset the index so 'State Postal Code' becomes a column again
df_avg.reset_index(inplace=True)

# Save the averages to a new CSV file
df_avg.to_csv('transportation_data.csv', index=False)
