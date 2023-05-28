from collections import Counter

import polars as pl
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class Skim:
    def __init__(self, df: pl.DataFrame, header_style: str = "bold cyan") -> None:
        self.df = df
        self.header_style = header_style
        self.console = Console()

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
        tables_list = [data_summary_table, data_type_table, groupe_type_table]
        #         if "category" in df.dtypes.astype(str).to_list():
        #            tables_list.append(cat_sum_table)
        grid.add_row(Columns(tables_list))
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
        tab_data = Counter(df.dtypes)

        group_types = []
        for key, val in tab_data.items():
            if (
                str(key).startswith("Int")
                or str(key).startswith("UInt")
                or str(key).startswith("Float")
            ):
                key = "Numeric"
            elif (
                str(key).startswith("Date")
                or str(key).startswith("Time")
                or str(key).startswith("Durat")
            ):
                key = "Temporal"
            elif str(key).startswith("Utf8"):
                key = "String"
            elif str(key).startswith("Bool"):
                key = "Boolean"
            elif str(key).startswith("Categor"):
                key = "Categorical"
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
        ...

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
