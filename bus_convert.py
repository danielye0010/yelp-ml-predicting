import pandas as pd
import json


# read and convert json to csv
def process_attributes(attr):
    if isinstance(attr, dict):
        return {k: process_attributes(v) for k, v in attr.items()}
    else:
        if isinstance(attr, bool):
            return int(attr)
        return attr


file_path_business = r"C:\Users\Daniel Ye\Desktop\yelp_Fall2023\yelp_Fall2023\business.json"

with open(file_path_business, 'r', encoding='utf-8') as file:  # 指定utf-8编码
    data = [json.loads(line) for line in file]

df_business = pd.DataFrame(data)

df_burgers = df_business[df_business['categories'].str.contains('Burgers', na=False)]

df_burgers.loc[:, 'attributes'] = df_burgers['attributes'].apply(process_attributes)

attributes_expanded = df_burgers['attributes'].apply(pd.Series)

df_burgers = pd.concat([df_burgers.drop('attributes', axis=1), attributes_expanded], axis=1)

required_columns = ['state', 'business_id', 'stars', 'review_count'] + list(attributes_expanded.columns)
df_burgers_final = df_burgers[required_columns]

df_burgers_final.to_csv('burgers_business.csv', index=False)
