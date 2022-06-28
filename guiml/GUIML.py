import numpy as np
import os
import ipywidgets as widgets
import joblib
import pandas as pd
import random

TEMP_SAVE_FOLDER = "_guiml"


class GUIML:
    def __init__(self, save_name="guiml",
                 # category_col_name="dataset_category"
                 ):
        """

        """
        category_col_name = "dataset_category"
        self.category_col_name = category_col_name
        self.save_name = save_name
        self.setting_path = TEMP_SAVE_FOLDER+"/"+save_name+".bin"

        # load dict data
        if not os.path.exists(TEMP_SAVE_FOLDER):
            os.mkdir(TEMP_SAVE_FOLDER)

        if not os.path.exists(self.setting_path):
            self.setting = {}
            self.setting["csv"] = {}

        else:
            self.setting = joblib.load(self.setting_path)
            self.csv = self.setting["current_csv"]

    def _save(self):
        joblib.dump(self.setting, self.setting_path)

    def select_columns(self, df=None):
        """
        Select box to choose columns for ML
        """
        if df is None:
            df = self.df
        else:
            self.df = df

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

        return display(
            self._target_col_w,
            widgets.HBox([self._non_use_col_w, self._use_col_w]),
            widgets.HBox([remove_button, add_button]),
        )

    def get_selected_column_df(self, df=None):
        """
        select explanatory and target variables
        """
        if df is None:
            df = self.df

        self.setting["csv"][self.csv]["use_cols"] = list(
            self._use_col_w.options)
        self.setting["csv"][self.csv]["non_use_cols"] = list(
            self._non_use_col_w.options)
        self.setting["csv"][self.csv]["target_col"] = self._target_col_w.value

        self._save()

        cols = [self.setting["csv"][self.csv]["target_col"]]
        cols.extend(self.setting["csv"][self.csv]["use_cols"])
        self.sel_df = df[cols]

        return self.sel_df

    def get_dataset(self, id_selector, sel_df=None):
        """
        automatically prepare dataset by random splitting
        """
        if sel_df is None:
            sel_df = self.sel_df

        sel_df.loc[id_selector.train_ids, self.category_col_name] = "train"
        sel_df.loc[id_selector.test_ids, self.category_col_name] = "test"

        # drop nan
        sel_df = sel_df[sel_df[self.setting["csv"][self.csv]["target_col"]]
                        == sel_df[self.setting["csv"][self.csv]["target_col"]]]

        """
        test_ratio=0.2
        # split train test
        tot_records = sel_df.shape[0]
        n_test = int(tot_records*test_ratio)

        category_list = ["train"]*tot_records
        category_list[:n_test] = ["test"]*n_test
        random.shuffle(category_list)

        sel_df[self.category_col_name] = category_list
        """

        tr_df = sel_df[sel_df[self.category_col_name] == "train"]
        te_df = sel_df[sel_df[self.category_col_name] == "test"]

        # set X and y
        self.tr_X = self._prepare_X(tr_df)
        self.tr_y = tr_df[[self.setting["csv"][self.csv]["target_col"]]]

        self.te_X = self._prepare_X(te_df)
        self.te_y = te_df[[self.setting["csv"][self.csv]["target_col"]]]

        self.tr_y = np.array(self.tr_y.values).reshape(-1)
        self.te_y = np.array(self.te_y.values).reshape(-1)

        self.dataset_df = sel_df

        return self.tr_X, self.te_X, self.tr_y, self.te_y

    def _prepare_X(self, df):
        """
        get explanatory variables
        """

        for col in [self.setting["csv"][self.csv]["target_col"],
                    self.category_col_name,
                    "predicted"]:

            if col in df.columns:
                df = df.drop(col, axis=1)
        return df
