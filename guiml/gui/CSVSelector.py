from ..GUIML import GUIML
import glob
import pandas as pd
import ipywidgets as widgets


class CSVSelector(GUIML):
    def __init__(self, save_name="guiml"):
        super().__init__(save_name)

    def __call__(self, regex="database/*.csv"):
        """
        select box of csv files 
        """
        file_path_list = glob.glob(regex)

        # set default value
        value = file_path_list[0]

        # set default value (by loading dict)
        if "current_csv" in self.setting:
            candidate_path = self.setting["current_csv"]
            if candidate_path in file_path_list:
                value = candidate_path

        # widget
        self._select_csv_w = widgets.Select(
            options=file_path_list,
            description='Select database file',
            disabled=False,
            value=value
        )

        # reset setting button
        def button_clicked(b):
            self.setting = {}
            self._save()
            self.setting["csv"] = {}
            self.csv = "unknown_csv"
            self.setting["current_csv"] = self.csv

        # widgets
        button = widgets.Button(description="Reset settings")
        button.on_click(button_clicked)

        return display(self._select_csv_w, button)

    def get_filename(self):
        self.setting["current_csv"] = self._select_csv_w.value
        file_name = self._select_csv_w.value

        if file_name not in self.setting["csv"]:
            self.setting["csv"][file_name] = {}

        self._save()
        return self._select_csv_w.value

    def load(self):
        """
        load csv data
        """

        # set current csv
        self.setting["current_csv"] = self._select_csv_w.value
        self.csv = self._select_csv_w.value

        # make new dict for the csv
        if self.csv not in self.setting["csv"]:
            self.setting["csv"][self.csv] = {}

        # load
        df = pd.read_csv(self.csv)
        #self.df = df

        self.setting["current_csv"] = self.csv

        self._save()
        return df
