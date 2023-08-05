from collections import Counter

import polars as pl
import numpy as np
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

HIST_BINS = 6
UNICODE_HIST = {
    0: " ",
    1 / 8: "▁",
    1 / 4: "▂",
    3 / 8: "▃",
    1 / 2: "▄",
    5 / 8: "▅",
    3 / 4: "▆",
    7 / 8: "▇",
    1: "█",
}


class Skim:
    def __init__(self, df: pl.DataFrame, header_style: str = "bold cyan") -> None:
        self.df = df
        self.header_style = header_style
        self.console = Console()
        self.numeric_columns = []
        self.categorical_columns = []
        self.temporal_columns = []
        self.string_columns = []
        self.bool_columns = []

    def skim(self):
        """Skim a data frame and return statistics.

        skim is an alternative to pandas.DataFrame.describe(), quickly providing
        an overview of a data frame. It produces a different set of summary
        functions based on the types of columns in the dataframe. You may get
        better results from ensuring that you set the datatypes in your dataframe
        you want before running skim.
        The colour_kwargs (str) are defined in _dataframe_to_rich_table.

        Args:
            df_in (pd.DataFrame): Dataframe to skim
            header_style (str): A style to use for headers. See Rich API Styles.
            colour_kwargs (dict[str]): colour keyword arguments for rich table

        Examples
        --------
        Skim a dataframe

        >>> df = pd.DataFrame(
                {
                 'col1': ['Philip', 'Turanga', 'bob'],
                 'col2': [50, 100, 70],
                 'col3': [False, True, True]
                })
        >>> df["col1"] = df["col1"].astype("string")
        >>> skim(df)
        """

        # Make a copy so as not to mess with dataframe
        df = self.df.clone()

        # Create table of "Data summary"
        data_summary_table = self._data_summary_table(df)
        data_type_table = self._data_types_table(df)
        groupe_type_table = self._group_types_table(df)
        numeric_type_table = self._numeric_variable_summary_table(df)

        #        # Categorys
        #        if "category" in df.dtypes.astype(str).to_list():
        #            xf = pd.DataFrame(df.dtypes.astype(str))
        #            cat_sum_table = Table(
        #                title="Categories", show_header=True, header_style=header_style
        #            )
        #            header_string = f"[{header_style}]Categorical Variables[/{header_style}]"
        #            cat_sum_table.add_column(header_string)
        #            cat_names = list(xf[xf[0] == "category"].index)
        #            for cat in cat_names:
        #                cat_sum_table.add_row(cat)
        #        # Summaries of cols of specific types
        #        types_funcs_dict = {
        #            "number": _numeric_variable_summary_table,
        #            "category": _category_variable_summary_table,
        #            "datetime": _datetime_variable_summary_table,
        #            "string": _string_variable_summary_table,
        #            "bool": _bool_variable_summary_table,
        #        }
        #        list_of_tabs = []
        #        for col_type, summary_func in types_funcs_dict.items():
        #            xf = df.select_dtypes(col_type)
        #            if not xf.empty:
        #                sum_df = summary_func(xf)
        #                list_of_tabs.append(
        #                    _dataframe_to_rich_table(
        #                        col_type, _round_dataframe(sum_df)  # , **colour_kwargs
        #                    )
        #                )
        #        # Put all of the info together
        grid = Table.grid(expand=True)
        general_info_table = [
            data_summary_table,
            data_type_table,
            groupe_type_table,
        ]
        stats_table = [numeric_type_table]
        #         if "category" in df.dtypes.astype(str).to_list():
        #            tables_list.append(cat_sum_table)
        grid.add_row(Columns(general_info_table))
        grid.add_row(Columns(stats_table))
        #        grid.add_column(justify="left")
        #        for sum_tab in list_of_tabs:
        #            grid.add_row(sum_tab)
        # Weirdly, iteration over list of tabs misses last entry
        #        grid.add_row(list_of_tabs[-1])
        self.console.print(Panel(grid, title="Running Polars Papaaa!", subtitle="End"))

    def _data_summary_table(self, df):
        tab_data = {"Number of rows": df.shape[0], "Number of columns": df.shape[1]}
        data_summary_table = Table(
            title="Data Summary", show_header=True, header_style=self.header_style
        )
        data_summary_table.add_column("dataframe")
        data_summary_table.add_column("Values")
        for key, val in tab_data.items():
            data_summary_table.add_row(key, str(val))

        return data_summary_table

    def _data_types_table(self, df):
        # Create table of "Data types"
        data_type_table = Table(
            title="Data Types", show_header=True, header_style=self.header_style
        )
        tab_data = Counter(df.dtypes)

        data_type_table.add_column("Data Type")
        data_type_table.add_column("Count")
        for key, val in tab_data.items():
            data_type_table.add_row(str(key), str(val))

        return data_type_table

    def _group_types_table(self, df):
        # Create table of "Group type"
        group_type_table = Table(
            title="Group Data Type", show_header=True, header_style=self.header_style
        )
        dtype_data = df.dtypes
        columns = df.columns
        group_types = []
        for col, dtype_ in zip(columns, dtype_data):
            if (
                str(dtype_).startswith("Int")
                or str(dtype_).startswith("UInt")
                or str(dtype_).startswith("Float")
            ):
                key = "Numeric"
                self.numeric_columns.append(col)
            elif (
                str(dtype_).startswith("Date")
                or str(dtype_).startswith("Time")
                or str(dtype_).startswith("Durat")
            ):
                key = "Temporal"
                self.temporal_columns.append(col)
            elif str(dtype_).startswith("Utf8"):
                key = "String"
                self.string_columns.append(col)
            elif str(dtype_).startswith("Bool"):
                key = "Boolean"
                self.bool_columns.append(col)
            elif str(dtype_).startswith("Categor"):
                key = "Categorical"
                self.categorical_columns.append(col)
            else:
                key = "Other"
            group_types.append(key)

        tab_data = Counter(group_types)

        group_type_table.add_column("Group Data Type")
        group_type_table.add_column("Count")
        for key, val in tab_data.items():
            group_type_table.add_row(str(key), str(val))

        return group_type_table

    def _numeric_variable_summary_table(self, df):
        """Summarise numeric variables.

        Summarise numeric variables. This is a helper function for skim.
        """
        df_describe = (
            df.select([pl.col(column) for column in self.numeric_columns])
            .describe(percentiles=(0.0, 0.1, 0.25, 0.5, 0.75, 0.99, 1.0))
            .transpose(include_header=True)
        )

        # the first row after the transposing is the column names
        df_describe.columns = df_describe.row(0)
        df_transposed = df_describe[1:]

        final_df_formatted = df_transposed.with_columns(
            [
                pl.all().exclude("describe").cast(pl.Float64, strict=False).round(2),
            ]
        )

        numeric_type_table = Table(
            title="Numeric Stats", show_header=True, header_style=self.header_style
        )

        numeric_type_table.add_column("Columns")
        numeric_type_table.add_column("Count")
        numeric_type_table.add_column("Null Count")
        numeric_type_table.add_column("Mean")
        numeric_type_table.add_column("Std")
        numeric_type_table.add_column("Min")
        numeric_type_table.add_column("Max")
        numeric_type_table.add_column("Median")
        numeric_type_table.add_column("Pct 0%")
        numeric_type_table.add_column("Pct 10%")
        numeric_type_table.add_column("Pct 25%")
        numeric_type_table.add_column("Pct 50%")
        numeric_type_table.add_column("Pct 75%")
        numeric_type_table.add_column("Pct 99%")
        numeric_type_table.add_column("Pct 100%")
        numeric_type_table.add_column("Hist")

        for row in final_df_formatted.rows():
            numeric_type_table.add_row(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                str(row[4]),
                str(row[5]),
                str(row[6]),
                str(row[7]),
                str(row[8]),
                str(row[9]),
                str(row[10]),
                str(row[11]),
                str(row[12]),
                str(row[13]),
                str(row[14]),
                self._create_unicode_hist(df, str(row[0])),
            )

        return numeric_type_table

    def _create_unicode_hist(self, df: pl.DataFrame, column: str) -> str:
        """Create unicode histogram.

        Create unicode histogram. This is a helper function for skim.
        """
        series = df.select(pl.col(column)).to_numpy()
        hist, _ = np.histogram(series, density=True, bins=HIST_BINS)
        hist = hist / hist.max()
        # now do value counts
        key_vector = np.array(list(UNICODE_HIST.keys()), dtype="float")
        ucode_to_print = "".join(
            [UNICODE_HIST[self._find_nearest(key_vector, val)] for val in hist]
        )
        return ucode_to_print

    def _find_nearest(self, array, value: float | int):
        """Find the nearest numerical match to value in an array.

        Args:
            array (np.ndarray): An array of numbers to match with.
            value (float): Single value to find an entry in array that is close.

        Returns:
            np.array: The entry in array that is closest to value.
        """
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    def _category_variable_summary_table(self, df):
        """Summarise category variables.

        Summarise category variables. This is a helper function for skim.
        """
        ...

    def _datetime_variable_summary_table(self, df):
        """Summarise datetime variables.

        Summarise datetime variables. This is a helper function for skim.
        """
        ...

    def _string_variable_summary_table(self, df):
        """Summarise string variables.

        Summarise string variables. This is a helper function for skim.
        """
        ...

    def _bool_variable_summary_table(self, df):
        """Summarise boolean variables.

        Summarise boolean variables. This is a helper function for skim.
        """
        ...
