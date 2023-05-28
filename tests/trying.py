import datetime

import polars as pl

from skimpy_ext.skimpy import Skim

df = pl.DataFrame(
    {
        "a": [1, 2, 3],
        "b": [4.4, 5, 6],
        "c": ["a", "b", "c"],
        "d": [True, False, True],
        "e": [
            datetime.datetime(2023, 3, 1),
            datetime.datetime(2023, 2, 1),
            datetime.datetime(2023, 2, 1),
        ],
    }
)

skim_class = Skim(df)
skim_class.skim()
