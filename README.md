# Skimpy Extended

A light weight tool for creating summary statistics from dataframes.

This is a replica of the original Skimpy package, but for polars!

**skimpy** is a light weight tool that provides
summary statistics about variables in data frames within the console or your interactive Python window.
Think of it as a super-charged version of `df.describe()`.
[You can find the documentation here](https://aeturrell.github.io/skimpy/).

# MVP TODOs

- [x] Info tables
- [x] Support for numerical data
- [ ] Support for categorical data
- [ ] Support for timeseries data
- [ ] Support for boolean data
- [ ] Remove zero-variance columns
- [ ] Identifies rare categories and groups
- [ ] Find outliers based on Inter Quartile Range
- [ ] Detects possibly mixed data types columns
- [ ] Detects high cardinality features
- [ ] Detects high correlated features
- [ ] Detects duplicated rows (may be an option to pass when call the Skimpy class)
- [ ] Indicate skewed ditributions
- [ ] Detects imbalanced classes
- [ ] Detects feature leakage
