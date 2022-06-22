import glob
import os
import ipywidgets as widgets
import joblib
import pandas as pd

TEMP_SAVE_FOLDER = "_guiml"


class GUIML:
    def __init__(self, notebook_name):
        self.notebook_name = notebook_name
        self.setting_path = TEMP_SAVE_FOLDER+"/"+notebook_name+".bin"

        if not os.path.exists(TEMP_SAVE_FOLDER):
            os.mkdir(TEMP_SAVE_FOLDER)

        if not os.path.exists(self.setting_path):
            self.setting_dict = {}
        else:
            self.setting_dict = joblib.load(self.setting_path)

    def _save(self):
        joblib.dump(self.setting_dict, self.setting_path)

    def select_csv(self, regex="database/*.csv"):
        file_path_list = glob.glob(regex)

        value = file_path_list[0]
        if "csv_path" in self.setting_dict:
            candidate_path = self.setting_dict["csv_path"]

            if candidate_path in file_path_list:
                value = candidate_path

        self.select_csv_w = widgets.Select(
            options=file_path_list,
            description='Select database file',
            disabled=False,
            value=value
        )
        try:
            return display(self.select_csv_w)
        except:
            return self.select_csv_w

    def load_csv(self):
        self.setting_dict["csv_path"] = self.select_csv_w.value
        df = pd.read_csv(self.setting_dict["csv_path"])
        self.df = df
        self._save()
        return df

    def select_columns(self, df=None):
        if df is None:
            df = self.df
        else:
            self.df = df

        if not "use_cols" in self.setting_dict:
            self.setting_dict["use_cols"] = []
            self.setting_dict["non_use_cols"] = list(df.columns)

        for c in df.columns:
            if c not in self.setting_dict["use_cols"]:
                if c not in self.setting_dict["non_use_cols"]:
                    self.setting_dict["non_use_cols"].append(c)

        def add_button_clicked(b):
            self.setting_dict["use_cols"].extend(self.non_use_col_w.value)
            self.use_col_w.options = self.setting_dict["use_cols"]

            for v in self.non_use_col_w.value:
                self.setting_dict["non_use_cols"].remove(v)
            self.non_use_col_w.options = self.setting_dict["non_use_cols"]

        def remove_button_clicked(b):
            self.setting_dict["non_use_cols"].extend(self.use_col_w.value)
            self.non_use_col_w.options = self.setting_dict["non_use_cols"]

            for v in self.use_col_w.value:
                self.setting_dict["use_cols"].remove(v)

            self.use_col_w.options = self.setting_dict["use_cols"]

        add_button = widgets.Button(
            description="Add", command=add_button_clicked)
        remove_button = widgets.Button(description="Remove")

        self.non_use_col_w = widgets.SelectMultiple(
            description='Non-use',
            options=self.setting_dict["non_use_cols"],
            disabled=False
        )
        self.use_col_w = widgets.SelectMultiple(
            description='Use',
            options=self.setting_dict["use_cols"],
            disabled=False
        )

        add_button.on_click(add_button_clicked)
        remove_button.on_click(remove_button_clicked)
        return display(widgets.HBox([self.non_use_col_w, self.use_col_w]),
                       widgets.HBox([remove_button, add_button]))

    def get_selected_column_df(self, df=None):
        if df is None:
            df = self.df

        self.setting_dict["use_cols"] = list(self.use_col_w.options)
        self.setting_dict["non_use_cols"] = list(self.non_use_col_w.options)

        self._save()
        return df[self.setting_dict["use_cols"]]
