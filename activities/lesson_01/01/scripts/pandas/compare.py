import pandas as pd
import time

timeInit = time.time()
df_movies = pd.read_csv('../dataset/ml-20m/movies.csv')
timeEnd = time.time()

print(f"Time to load the dataset with Pandas: {timeEnd - timeInit:.4f} seconds")
print(df_movies.head())