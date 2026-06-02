import pandas as pd
import time

timeInit = time.time()
df_movies = pd.read_csv('../dataset/ml-20m/ratings.csv')
timeEnd = time.time()

print(f"+ =======================================================================")
print(f"+ ")
print(f"+ Loaded <ratings.csv> dataset")
print(f"+ Time to load the dataset with Pandas: {timeEnd - timeInit:.4f} seconds")
print(f"+ ")
print(f"+ =======================================================================")


print(df_movies.head())