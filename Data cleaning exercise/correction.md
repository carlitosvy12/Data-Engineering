# Exercise Correction: Data Cleaning Lab
**Student:** Carlos Vicente  
**Exercise:** E-commerce Customer Orders Data Cleaning  
**Date:** December 18, 2025

---

## Overall Assessment

**Grade: 9.5/10**

This is an excellent and well-structured data cleaning exercise. The code demonstrates strong understanding of pandas operations, data quality principles, and best practices in data engineering. The implementation is clean, efficient, and includes comprehensive validation through data quality tests.

The code successfully addresses all major data quality issues and provides clear before/after metrics to validate the cleaning effectiveness.

---

## Strengths

### 1. **Excellent Code Organization**
- Professional structure with clear, numbered steps and visual separators.
- Descriptive comments and section headers.
- Timestamp tracking for execution monitoring.
- Clean and readable variable naming.

### 2. **Comprehensive Data Quality Framework**
- **Outstanding:** Implemented six data quality tests covering all major dimensions:
  - `test_accuracy()` - Age and quantity validation
  - `test_completeness()` - Required fields validation
  - `test_consistency()` - Country format standardization
  - `test_validity()` - Email and date format validation
  - `test_uniqueness()` - OrderID uniqueness check
  - `test_timeliness()` - Recent data validation (5-year window)
- Before/after comparison provides clear validation metrics.
- Well-structured test functions with meaningful return values.

### 3. **Robust Data Cleaning Implementation**
- **Data retrieval:** Direct download from URL with proper error handling.
- **Duplicate removal:** Proper use of `drop_duplicates()`.
- **Text normalization:** Consistent `.strip()` for all string columns.
- **Type conversion:** Proper use of `pd.to_datetime()` and `pd.to_numeric()` with `errors='coerce'`.
- **Country standardization:** `.upper()` for consistency.
- **Negative quantity handling:** Removal of invalid rows.
- **Email validation:** Regex pattern matching for email format.
- **Final output:** Clean data saved to CSV for downstream use.

### 4. **Good Software Engineering Practices**
- Error handling with `response.raise_for_status()`.
- Proper use of `on_bad_lines='skip'` for malformed CSV rows.
- Working on a copy (`df_clean = df_raw.copy()`) to preserve original data.
- Console output with progress indicators.
- Summary statistics at the end.

---

## Areas for Improvement

### 1. **Missing Value Imputation** (-0.3 points)

**Issue:** The code identifies invalid ages but doesn't impute them:

```python
invalid_age = df_clean["CustomerAge"].isna()
print(f"  - Edades inválidas encontradas: {invalid_age.sum()}")
# But then doesn't fill them!
```

**Recommendation:** Add imputation strategy for missing ages:
```python
# After identifying invalid ages, impute with median
median_age = df_clean["CustomerAge"].median()
df_clean["CustomerAge"] = df_clean["CustomerAge"].fillna(median_age)
print(f"  - Edades imputadas con mediana: {median_age:.1f}")
```

### 2. **Unnecessary Duplicate Processing on df_raw** (-0.2 points)

**Issue:** These conversions on `df_raw` happen after the cleaning is done:

```python
# This is after all cleaning on df_clean is completed
df_raw["CustomerAge"] = pd.to_numeric(df_raw["CustomerAge"], errors="coerce")
df_raw["OrderDate"] = pd.to_datetime(df_raw["OrderDate"], errors="coerce")
```

**Recommendation:** Either:
- Move these lines to Step 2 (Initial Exploration) before df_clean is created.
- Or remove them since they're not needed for the raw comparison (tests will handle conversion).

