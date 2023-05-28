import polars as pl

from skimpy_ext.skimpy import Skim

df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

skim_class = Skim(df)
skim_class.skim()
