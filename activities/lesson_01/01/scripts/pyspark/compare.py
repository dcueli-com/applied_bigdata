from pyspark.sql import SparkSession
import time

timeInit = time.time()

# Spark no hace nada hasta que lee el archivo, el dataset en este caso está en 
# 'data/ratings.csv'. Cuando escribimos df = spark.read.csv(...), la sesión 
# de Spark <spark> no lee el archivo de realmente, sino que anota el plan 
# de lo que tiene que hacer.
# 
# Es decir, cuando pedimos un resultado con un 'show()' o un 'count()', la 
# sesión revisa lo anotado y optimiza el camino más rápido. 
# 
# Creamos la sesión de Spark
spark = SparkSession.builder \
  .appName("ComprLibs") \
  .master("local[*]") \
  .config("spark.driver.memory", "64g") \
  .getOrCreate()

# Cargamos el dataset (lazyload)
df_spark = spark.read.csv(
  '../dataset/ml-20m/movies.csv', 
  header=True, 
  inferSchema=True
)

# Obligamos a Spark a leer el archivo contando las filas
total_filas = df_spark.count()
timeEnd = time.time()
print(f"Time to load the dataset with PySpark: {timeEnd - timeInit:.4f} seconds")

# Mostramos las primeras 5 filas del DataFrame
df_spark.show(5)