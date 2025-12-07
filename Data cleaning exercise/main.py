from datetime import datetime
import requests
import pandas as pd
from io import StringIO
import re

print("=" * 70)
print("DATA CLEANING EXERCISE - E-COMMERCE CUSTOMER ORDERS")
print("=" * 70)
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# STEP 1: RETRIEVE DATA FROM WEB SOURCE
# ============================================================================

URL = "https://raw.githubusercontent.com/victorbrub/data-engineering-class/refs/heads/main/pre-post_processing/exercise.csv"

print("[STEP 1] Descargando datos brutos...")
response = requests.get(URL)
response.raise_for_status()
raw_csv_text = response.text

with open("raw_data.csv", "w", encoding="utf-8") as f:
    f.write(raw_csv_text)

print("  - Datos descargados y guardados en raw_data.csv\n")

# ============================================================================
# STEP 2: INITIAL EXPLORATION
# ============================================================================

print("[STEP 2] Exploración inicial...")

df_raw = pd.read_csv(
    StringIO(raw_csv_text),
    sep=",",
    engine="python",
    on_bad_lines="skip"
)

print("  - Dimensiones (filas, columnas):", df_raw.shape)
print("  - Columnas:", list(df_raw.columns))
print("\n  - Primeras filas:")
print(df_raw.head())
print("\n  - Información del DataFrame:")
print(df_raw.info())
print("\n  - Valores nulos por columna:")
print(df_raw.isna().sum())
print()

# ============================================================================
# STEP 3: IDENTIFY QUALITY ISSUES
# ============================================================================

print("[STEP 3] Identificando problemas de calidad de datos...")

num_rows = len(df_raw)
num_dupes = df_raw.duplicated().sum()
nulls_per_col = df_raw.isna().sum()

print(f"  - Número de filas: {num_rows}")
print(f"  - Filas duplicadas: {num_dupes}")
print("  - Nulos por columna:")
print(nulls_per_col)
print()


# ---------------------------------------------------------------------------
# Is there any sensible information?
# Yes. The dataset includes personal data such as full names, emails,
# phone numbers, and countries.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# What kind of problems can we have regarding the nature of this data?
#The dataset has missing values, inconsistent formats, invalid or non-numeric ages, negative quantities...
# ---------------------------------------------------------------------------





# ============================================================================
# STEP 4: DATA CLEANING
# ============================================================================

print("[STEP 4] Limpiando datos...")

df_clean = df_raw.copy()
df_clean = df_clean.drop_duplicates()

for col in df_clean.select_dtypes(include=["object"]).columns:
    df_clean[col] = df_clean[col].astype(str).str.strip()

df_clean["Country"] = df_clean["Country"].str.upper()
df_clean["OrderDate"] = pd.to_datetime(df_clean["OrderDate"], errors="coerce")
df_clean["CustomerAge"] = pd.to_numeric(df_clean["CustomerAge"], errors="coerce")

invalid_age = df_clean["CustomerAge"].isna()
print(f"  - Edades inválidas encontradas: {invalid_age.sum()}")

before = len(df_clean)
df_clean = df_clean[df_clean["Quantity"] >= 0]
after = len(df_clean)
print(f"  - Filas eliminadas por cantidad negativa: {before - after}")

email_pattern = re.compile(r".+@.+\..+")
valid_email_mask = df_clean["Email"].astype(str).str.match(email_pattern)
print(f"  - Emails inválidos: {(~valid_email_mask).sum()}")
df_clean = df_clean[valid_email_mask]

print("  - Limpieza básica completada.\n")

df_raw["CustomerAge"] = pd.to_numeric(df_raw["CustomerAge"], errors="coerce")
df_raw["OrderDate"] = pd.to_datetime(df_raw["OrderDate"], errors="coerce")

# ============================================================================
# STEP 5: FINAL VALIDATION
# ============================================================================

print("[STEP 5] Validación final (data quality tests)...")

def test_accuracy(df):
    cond1 = df["CustomerAge"].between(0, 120)
    cond2 = df["Quantity"] >= 0
    return (cond1 & cond2).mean()

def test_completeness(df):
    required_cols = ["OrderID", "Email", "Country"]
    return df[required_cols].notna().all(axis=1).mean()

def test_consistency(df):
    return (df["Country"] == df["Country"].str.upper()).mean()

def test_validity(df):
    email_ok = df["Email"].astype(str).str.contains("@")
    date_ok = df["OrderDate"].notna()
    return (email_ok & date_ok).mean()

def test_uniqueness(df):
    return df["OrderID"].is_unique

def test_timeliness(df):
    five_years_ago = datetime.now().replace(year=datetime.now().year - 5)
    return (df["OrderDate"] >= five_years_ago).mean()

tests = {
    "Accuracy": test_accuracy,
    "Completeness": test_completeness,
    "Consistency": test_consistency,
    "Validity": test_validity,
    "Uniqueness": test_uniqueness,
    "Timeliness": test_timeliness,
}

print("Resultados de los tests (RAW vs CLEAN):\n")

for name, func in tests.items():
    raw_score = func(df_raw)
    clean_score = func(df_clean)
    print(f"  - {name}: RAW = {raw_score:.2%} | CLEAN = {clean_score:.2%}")

print()

# ============================================================================
# STEP 6: SAVE CLEAN DATA
# ============================================================================

print("[STEP 6] Guardando datos limpios...")
df_clean.to_csv("clean_data.csv", index=False)
print("  - Archivo guardado como clean_data.csv\n")

# ============================================================================
# SUMMARY
# ============================================================================

print("[SUMMARY]")
print(f"  - Filas RAW:   {len(df_raw)}")
print(f"  - Filas CLEAN: {len(df_clean)}")
print("  - Archivo limpio: clean_data.csv\n")

print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
