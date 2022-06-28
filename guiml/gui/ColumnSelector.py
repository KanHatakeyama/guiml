from ..GUIML import GUIML
import pandas as pd
import ipywidgets as widgets


class ColumnSelector(GUIML):
    def __init__(self, save_name="guiml"):
        super().__init__(save_name)

    def __call__(self, df):
        """
        Select box to choose columns for ML
        """
        # initial vals
        if not "use_cols" in self.setting["csv"][self.csv]:
            self.setting["csv"][self.csv]["use_cols"] = []
            self.setting["csv"][self.csv]["non_use_cols"] = list(df.columns)
            self.setting["csv"][self.csv]["target_col"] = None

        for c in df.columns:
            if c not in self.setting["csv"][self.csv]["use_cols"]:
                if c not in self.setting["csv"][self.csv]["non_use_cols"]:
                    self.setting["csv"][self.csv]["non_use_cols"].append(c)

        # button click
        def add_button_clicked(b):
            self.setting["csv"][self.csv]["use_cols"].extend(
                self._non_use_col_w.value)
            self._use_col_w.options = self.setting["csv"][self.csv]["use_cols"]

            for v in self._non_use_col_w.value:
                self.setting["csv"][self.csv]["non_use_cols"].remove(v)
            self._non_use_col_w.options = self.setting["csv"][self.csv]["non_use_cols"]

        def remove_button_clicked(b):
            self.setting["csv"][self.csv
                                ]["non_use_cols"].extend(self._use_col_w.value)
            self._non_use_col_w.options = self.setting["csv"][self.csv]["non_use_cols"]

            for v in self._use_col_w.value:
                self.setting["csv"][self.csv]["use_cols"].remove(v)

            self._use_col_w.options = self.setting["csv"][self.csv]["use_cols"]

        # widgets
        add_button = widgets.Button(description="->")
        remove_button = widgets.Button(description="<-")

        self._non_use_col_w = widgets.SelectMultiple(
            description='Non-use',
            options=self.setting["csv"][self.csv]["non_use_cols"],
            disabled=False
        )
        value = self.setting["csv"][self.csv]["use_cols"]
        self._use_col_w = widgets.SelectMultiple(
            description='Use',
            options=self.setting["csv"][self.csv]["use_cols"],
            value=value,
            disabled=False
        )

        add_button.on_click(add_button_clicked)
        remove_button.on_click(remove_button_clicked)

        # target
        self._target_col_w = widgets.Select(
            description='Target',
            options=list(df.columns),
            value=self.setting["csv"][self.csv]["target_col"]
        )

        self.df = df
        return display(
            self._target_col_w,
            widgets.HBox([self._non_use_col_w, self._use_col_w]),
            widgets.HBox([remove_button, add_button]),
        )

    def load(self):
        """
        select explanatory and target variables
        """

        self.setting["csv"][self.csv]["use_cols"] = list(
            self._use_col_w.options)
        self.setting["csv"][self.csv]["non_use_cols"] = list(
            self._non_use_col_w.options)
        self.setting["csv"][self.csv]["target_col"] = self._target_col_w.value

        self._save()

        cols = [self.setting["csv"][self.csv]["target_col"]]
        cols.extend(self.setting["csv"][self.csv]["use_cols"])
        return self.df[cols]
