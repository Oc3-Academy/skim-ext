import polars as pl


class Skim:
    def __init__(self, df: pl.DataFrame) -> None:
        self.df = df

    def describe_print(self):
        print(self.df.describe())
