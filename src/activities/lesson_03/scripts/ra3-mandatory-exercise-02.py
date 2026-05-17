# %%
# AUTHOR: David Cueli
# DATE: 2024-06-17
# DESCRIPTION: This notebook contains the mandatory exercises for RA3 step by step
# ======================================================================================================================================
# RA3, MANDATOR EXERCISE 2: Data profiling and analyisis of data
# ======================================================================================================================================
# STEP 0.1: Requires
# --------------------------------------------------------------------------------------------------------------------------------------
# import sys
import time
import polars as pl

from config.paths import REPORTS_DIR

# %%
# STEP 0.2: Globals variables (It's much better to use a secret manager, but for the sake of simplicity, we'll use a global variable)
# --------------------------------------------------------------------------------------------------------------------------------------
totInitTime = time.time()
PATH_DATASET = "../dataset/nasa-dataset.csv"

# %%
# STEP 0.3: Helpers functions (It's much better to use a utils.py file, but for the sake of simplicity, we'll define them here as well)
# --------------------------------------------------------------------------------------------------------------------------------------
def LBr(pHowMany: int = 1):
  for i in range(0, pHowMany):
    print(f"+ ")

def Bra(pHowMany: int = 0):
  LBr(pHowMany)
  print(f"+ --------------------------------------------------------------------------------------------------------------------------------------")

def Ket(pHowMany: int = 0):
  LBr(pHowMany)
  print(f"+ ======================================================================================================================================")

# %%
# STEP 0.4: Load the dataset with Polars
# --------------------------------------------------------------------------------------------------------------------------------------
Ket()
print(f"+ Load '{PATH_DATASET}' from the Asteroid dataset ")
Bra()
print(f"+ Loading with Polars...")
LBr()

tInit = time.time()
nasaAsteroids_df_lz = pl.scan_csv(
  PATH_DATASET,
  schema_overrides={ "pdes": pl.String }
)
df_sample = nasaAsteroids_df_lz.limit(5).collect_schema()
tEnd = time.time()

# Show the structure of the dataset and the time it took to load it
print(df_sample)
Bra()
print(f"+ Time to load the dataset with Polars: {tEnd - tInit:.4f} seconds")
Bra()

# %%
# Show the first few rows and the structure of the dataset
LBr()
print(nasaAsteroids_df_lz.head(5).collect_schema())
Ket()


# %%
# EXERCISE 1.1: Identification and Cleaning of Duplicates
# OTX (Original TeXt): "Identifica y elimina filas duplicadas"
# ======================================================================================================================================
LBr()
print(f"+ Step 1.1: Remove duplicate rows...")
Bra()
LBr()

# Count the initial rows from original file
rows_bef = nasaAsteroids_df_lz.select(pl.len()).collect().item()

# Apply the duplicate removal
nasaAsteroids_df_lz = nasaAsteroids_df_lz.unique()

# Count the rows after the duplicate removal
rows_aft = nasaAsteroids_df_lz.select(pl.len()).collect().item()

# print(f"+ Rows with invalid/negative MOID: ............ {qtyInvalidMOID}")
# print(f"+ Rows missing critical orbital parameters: ...     {qtyNoOrbParams}")

print(f"+ Rows total before ........................... {rows_bef}")
print(f"+ Rows total after ............................ {rows_aft}")
print(f"+ ____________________________________________________")
print(f"+ Total of duplicates removed .................      {rows_bef - rows_aft}")
LBr()


# %%
# EXERCISE 1.2: Check data integrity (Ranges and Formats)
# OTX (Original TeXt): "Comprueba la integridad de los datos en columnas como el precio, el ID, el nombre, etc. (valida formatos, rangos, etc.)."
# ======================================================================================================================================
Ket()
print(f"+ Step 1.2: Validating data integrity")
print(f"+ Checking for critical anomalies...")
Bra()
LBr()

# [ANALYSIS]
# Count how many rows break the basic rules of physics before renoving them:
# - MOID distance is invalid (must be positive)
qtyInvalidMOID = (nasaAsteroids_df_lz
  .filter(pl.col("moid").is_null() | (pl.col("moid") < 0))
  .select(pl.len())
  .collect()
  .item()
)

# - Count rows that don't have the some orbital parameters
qtyNoOrbParams = (nasaAsteroids_df_lz
  .filter(
    pl.col("e").is_null() | 
    pl.col("a").is_null() | 
    pl.col("q").is_null() | 
    pl.col("i").is_null() | 
    pl.col("tp").is_null()
  )
  .select(pl.len())
  .collect()
  .item()
)

print(f"+ Rows with invalid/negative MOID ............   {qtyInvalidMOID}")
print(f"+ Rows missing critical orbital parameters ...       {qtyNoOrbParams}")

# [DOING]
# Filter the dataset for the rows that no break the basic rules of physics
nasaAsteroids_df_lz = (nasaAsteroids_df_lz
  .filter(
    # Minimal distance intersection with Earth (MOID) must be positive
    (pl.col("moid") >= 0) &
    # Basic rules of physics
    (
      pl.col("e").is_not_null() & 
      pl.col("a").is_not_null() & 
      pl.col("q").is_not_null() & 
      pl.col("i").is_not_null() & 
      pl.col("tp").is_not_null()
    )) 
)
# Update the count of rows after applying the integrity filters
rowsOk = nasaAsteroids_df_lz.select(pl.len()).collect().item()
print(f"+ ____________________________________________________")
print(f"+ Rows that passed integrity filters .......... {rowsOk}")
print(f"+ Total rows discarded in this step ...........  {rows_aft - rowsOk}")
LBr()

# %%
# EXERCISE 1.3: Replace null or invalid values according to NASA best practices
# OTX (Original TeXt): "Reemplaza valores nulos o inválidos según las mejores prácticas para el dataset."
# ======================================================================================================================================
Ket()
print(f"+ Step 1.3: Replacing null or invalid values (NASA & IAU best practices)")
Bra()
LBr()

# 1.3.1 [ANALYSIS]
# Count how many null values there are in the diameter and albedo columns, which are the ones that remain to be fixed
howManyNullsDiamBefore = nasaAsteroids_df_lz.filter(pl.col("diameter").is_null()).select(pl.len()).collect().item()
howManyNullsAlbedoBefore = nasaAsteroids_df_lz.filter(pl.col("albedo").is_null() | (0.0 == pl.col("albedo"))).select(pl.len()).collect().item()

print(f"+ Asteroids with missing Diameter (NULL) ...... {howManyNullsDiamBefore}")
print(f"+ Asteroids with missing/zero Albedo: ......... {howManyNullsAlbedoBefore}")
Bra()
LBr()

# Calculate the truncated average for the diameter using only the known values that are <= 20km, which 
# is a common practice in NASA when they have to estimate missing values for small asteroids
truncateAvg = (nasaAsteroids_df_lz
  .filter((pl.col("diameter").is_not_null()) & (pl.col("diameter") <= 20.0))
  .select(pl.col("diameter").mean())
  .collect()
  .item()
)
print(f"+ Calculated Truncated Average (D <= 20km) ....      {truncateAvg:.4f} km")

# 1.3.2[DOING]
# Apply the mass replacement based on the science of the dataset
nasaAsteroids_df_lz = nasaAsteroids_df_lz.with_columns(
  # Fill the diameter null values with the calculated truncated average
  pl.col("diameter").fill_null(truncateAvg),
  
  # Fill the categorical flags of danger (NEO and PHA) null values with "N" (not a NEO or PHA)
  pl.col("neo").fill_null("N"),
  pl.col("pha").fill_null("N")
).with_columns(
  # Apply the NASA mathematic formula to calculate the real/theoric Albedo 
  # https://ssd.jpl.nasa.gov/glossary/albedo.html
  # The formula is: Albedo = (1328 / (Diameter * 10^(0.2 * H)))^2
  # Where:
  # - Diameter is the diameter of the asteroid in kilometers
  # - H is the absolute magnitude of the asteroid
  # If the albedo is null or 0.0, we calculate it using the formula, otherwise we keep the original value
  pl.when(pl.col("albedo").is_null() | (pl.col("albedo") == 0.0))
  .then(
    (1328 / (pl.col("diameter") * (10 ** (0.2 * pl.col("H"))))) ** 2
  )
  .otherwise(pl.col("albedo"))
  .alias("albedo")
)

# 1.3.3 [CHECK]
# Check there are no rows withou applied the NASA & IUA best practices for the dataset
howManyNullsDiamAfter = nasaAsteroids_df_lz.select(pl.col("diameter").null_count()).collect().item()
howManyNullsAlbedoAfter = nasaAsteroids_df_lz.select(pl.col("albedo").null_count()).collect().item()
rowsOk = nasaAsteroids_df_lz.select(pl.len()).collect().item()

print(f"+ Remaining NULLs in Diameter: ................      {howManyNullsDiamAfter}")
print(f"+ Remaining NULLs in Albedo: ..................   {howManyNullsAlbedoAfter}")
Bra()
LBr()

# 1.3.4 [NORMALIZING COLUMNS]
# Save the asteroids without assigned 'H' magnitude by assigning the average albedo of NASA JPL
nasaAsteroids_df_lz = nasaAsteroids_df_lz.with_columns(pl.col("albedo").fill_null(0.07))

# Medimos el éxito de la operación
howManyNullsAlbedoAfter = nasaAsteroids_df_lz.select(pl.col("albedo").null_count()).collect().item()
rowsOk = nasaAsteroids_df_lz.select(pl.len()).collect().item()

print(f"+ Norm. Albedo NULLs with JPL standard (0.07) .      {howManyNullsAlbedoAfter}")
print(f"+ ____________________________________________________")
print(f"+ Final consolidated rows for analysis: ....... {rowsOk}")
Ket()

# ... (Todo tu código anterior del Paso 1.3.4 permanece intacto arriba)

print(f"+ Norm. Albedo NULLs with JPL standard (0.07) .      {howManyNullsAlbedoAfter}")
print(f"+ ____________________________________________________")
print(f"+ Final consolidated rows for analysis: ....... {rowsOk}")
Ket()


# %%
# RA3, MANDATORY EXERCISE 2: Data profiling and analyisis of data
# ======================================================================================================================================
LBr()
Bra()
print(f"+ Creating profiling report")
Ket()

from ydata_profiling import ProfileReport

# Get the clean dataframe Polars collection
print(f"+ Procesando el plan de Polars y convirtiendo a Pandas... (Esto puede tardar un momento)")
nasaAsteroids_pandas_df = nasaAsteroids_df_lz.collect().to_pandas()

# Configure the report
profile = ProfileReport(
  nasaAsteroids_pandas_df, 
  title="NASA Asteroids Dataset - Cleaning and Profiling report",
  explorative=True,
  vars={"cat": {"words": False, "characters": False}}
 
  # ,
  # # Ignore the heaviest non-linear correlations, which are very expensive to calculate and we don't need them 
  # # for this exercise as Spearman, Kendall, Cramér's V, Phi k
  # # Just allow Pearson, which is a very fast linear correlation calculation.
  # correlations={
  #   "pearson": {"calculate": True},
  #   "spearman": {"calculate": False},
  #   "kendall": {"calculate": False},
  #   "cramers": {"calculate": False},
  #   "phi_k": {"calculate": False},
  # }  
)

# Export the report to an external HTML file
outputPath = REPORTS_DIR / "ra3-mandatory-exercise-02-report.html"
profile.to_file(outputPath)

print(f"+ ")
print(f"+ Profiling report generated in: {outputPath}")
Ket()
totEndTime = time.time()
print(f"+ Total execution time: {totEndTime - totInitTime:.4f} seconds")
