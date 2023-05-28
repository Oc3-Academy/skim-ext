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

    def describe_print(self):
        print(self.df.describe())

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

        # check if the dataframe has a name
        # i don't see why this is necessary
        #           if hasattr(df_in, "name") and "name" not in df_in.columns:
        #               name = df_in.name
        #           else:
        #               name = "dataframe"
        #
        # Make a copy so as not to mess with dataframe
        df = self.df.clone()

        # Perform inference of datatypes
        # I thinks that doesn't need infer type for polars
        #         df = _infer_datatypes(df)

        # Data summary
        tab_1_data = {"Number of rows": df.shape[0], "Number of columns": df.shape[1]}
        dat_sum_table = Table(
            title="Data Summary", show_header=True, header_style=self.header_style
        )
        dat_sum_table.add_column("dataframe")
        dat_sum_table.add_column("Values")
        for key, val in tab_1_data.items():
            dat_sum_table.add_row(key, str(val))

        #        # Data tpes
        types_sum_table = Table(
            title="Data Types", show_header=True, header_style=self.header_style
        )
        tab_2_data = Counter(df.dtypes)

        types_sum_table.add_column("Column Type")
        types_sum_table.add_column("Count")
        for key, val in tab_2_data.items():
            types_sum_table.add_row(str(key), str(val))

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
        tables_list = [dat_sum_table, types_sum_table]
        #         if "category" in df.dtypes.astype(str).to_list():
        #            tables_list.append(cat_sum_table)
        grid.add_row(Columns(tables_list))
        print(tab_1_data, tab_2_data)
        #        grid.add_column(justify="left")
        #        for sum_tab in list_of_tabs:
        #            grid.add_row(sum_tab)
        # Weirdly, iteration over list of tabs misses last entry
        #        grid.add_row(list_of_tabs[-1])
        self.console.print(Panel(grid, title="Running Polars Papaaa!", subtitle="End"))
