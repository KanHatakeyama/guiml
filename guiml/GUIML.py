import glob
import numpy as np
import os
import ipywidgets as widgets
import joblib
import pandas as pd

import random
from .Chem.Autodescriptor import AutoDescriptor, RDKitDescriptors, GroupContMethod, MordredDescriptor, Fingerprint

TEMP_SAVE_FOLDER = "_guiml"


class GUIML:
    def __init__(self, notebook_name,
                 category_col_name="dataset_category"):
        """

        """
        self.category_col_name = category_col_name
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
        """
        select csv path
        """
        file_path_list = glob.glob(regex)

        value = file_path_list[0]
        if "csv_path" in self.setting_dict:
            candidate_path = self.setting_dict["csv_path"]

            if candidate_path in file_path_list:
                value = candidate_path

        self._select_csv_w = widgets.Select(
            options=file_path_list,
            description='Select database file',
            disabled=False,
            value=value
        )
        try:
            return display(self._select_csv_w)
        except:
            return self._select_csv_w

    def load_csv(self):
        """
        load csv data
        """
        self.setting_dict["csv_path"] = self._select_csv_w.value
        df = pd.read_csv(self.setting_dict["csv_path"])
        self.df = df
        self._save()
        return df

    def select_columns(self, df=None):
        """
        Select box to choose columns for ML
        """
        if df is None:
            df = self.df
        else:
            self.df = df

        # initial vals
        if not "use_cols" in self.setting_dict:
            self.setting_dict["use_cols"] = []
            self.setting_dict["non_use_cols"] = list(df.columns)
            self.setting_dict["target_col"] = None

        for c in df.columns:
            if c not in self.setting_dict["use_cols"]:
                if c not in self.setting_dict["non_use_cols"]:
                    self.setting_dict["non_use_cols"].append(c)

        # button click
        def add_button_clicked(b):
            self.setting_dict["use_cols"].extend(self._non_use_col_w.value)
            self._use_col_w.options = self.setting_dict["use_cols"]

            for v in self._non_use_col_w.value:
                self.setting_dict["non_use_cols"].remove(v)
            self._non_use_col_w.options = self.setting_dict["non_use_cols"]

        def remove_button_clicked(b):
            self.setting_dict["non_use_cols"].extend(self._use_col_w.value)
            self._non_use_col_w.options = self.setting_dict["non_use_cols"]

            for v in self._use_col_w.value:
                self.setting_dict["use_cols"].remove(v)

            self._use_col_w.options = self.setting_dict["use_cols"]

        # widgets
        add_button = widgets.Button(description="->")
        remove_button = widgets.Button(description="<-")

        self._non_use_col_w = widgets.SelectMultiple(
            description='Non-use',
            options=self.setting_dict["non_use_cols"],
            disabled=False
        )
        value = self.setting_dict["use_cols"]
        self._use_col_w = widgets.SelectMultiple(
            description='Use',
            options=self.setting_dict["use_cols"],
            value=value,
            disabled=False
        )

        add_button.on_click(add_button_clicked)
        remove_button.on_click(remove_button_clicked)

        # target
        self._target_col_w = widgets.Select(
            description='Target',
            options=list(df.columns),
            value=self.setting_dict["target_col"]
        )

        return display(
            self._target_col_w,
            widgets.HBox([self._non_use_col_w, self._use_col_w]),
            widgets.HBox([remove_button, add_button]),
        )

    def get_selected_column_df(self, df=None):
        if df is None:
            df = self.df

        self.setting_dict["use_cols"] = list(self._use_col_w.options)
        self.setting_dict["non_use_cols"] = list(self._non_use_col_w.options)
        self.setting_dict["target_col"] = self._target_col_w.value

        self._save()

        cols = [self.setting_dict["target_col"]]
        cols.extend(self.setting_dict["use_cols"])
        self.sel_df = df[cols]

        return self.sel_df

    def select_mol_descriptors(self):
        if "SMILES_col" not in self.setting_dict:
            self.setting_dict["SMILES_col"] = None
        if "descriptors" not in self.setting_dict:
            self.setting_dict["descriptors"] = ()

        self._smiles_col_w = widgets.Select(
            description='SMILES',
            options=list(self.df.columns),
            value=self.setting_dict["SMILES_col"],
        )

        self._mol_descriptor_w = widgets.SelectMultiple(
            description='Select descriptors',
            options=["RDKit", "Mordred(2D)", "Mordred(3D)",
                     "JR", "Avalon Fingerprint"],
            value=self.setting_dict["descriptors"]
        )

        return display(
            self._smiles_col_w,
            self._mol_descriptor_w)

    def calculate_mol_descriptors(self, smiles_list=None):
        only_desc_df_mode = True
        if smiles_list is None:
            smiles_list = list(self.df[self.setting_dict["SMILES_col"]])
            only_desc_df_mode = False

        # update form info
        self.setting_dict["SMILES_col"] = self._smiles_col_w.value
        self.setting_dict["descriptors"] = self._mol_descriptor_w.value
        self._save()

        # initiate calculator
        calculators = []
        for desc_name in self.setting_dict["descriptors"]:
            if desc_name == "RDKit":
                calculators.append(RDKitDescriptors())
            elif desc_name == "Mordred(2D)":
                calculators.append(MordredDescriptor())
            elif desc_name == "Mordred(3D)":
                calculators.append(MordredDescriptor(ignore_3D=False))
            if desc_name == "JR":
                calculators.append(GroupContMethod())
            if desc_name == "Avalon Fingerprint":
                calculators.append(Fingerprint())

        desc_calculator = AutoDescriptor(calculators=calculators)

        # calcualte

        desc_df = desc_calculator(smiles_list)

        # return only descriptors
        if only_desc_df_mode:
            return desc_df
        desc_df = desc_df.drop(self.setting_dict["SMILES_col"], axis=1)
        merge_df = pd.merge(self.df, desc_df, left_index=True,
                            right_index=True, how="outer")
        self.df = merge_df
        return merge_df

    def get_dataset(self, test_ratio=0.2, sel_df=None):
        if sel_df is None:
            sel_df = self.sel_df

        # drop nan
        sel_df = sel_df[sel_df[self.setting_dict["target_col"]]
                        == sel_df[self.setting_dict["target_col"]]]

        # split train test
        tot_records = sel_df.shape[0]
        n_test = int(tot_records*test_ratio)

        category_list = ["train"]*tot_records
        category_list[:n_test] = ["test"]*n_test
        random.shuffle(category_list)

        sel_df[self.category_col_name] = category_list

        tr_df = sel_df[sel_df[self.category_col_name] == "train"]
        te_df = sel_df[sel_df[self.category_col_name] == "test"]

        # set X and y
        self.tr_X = tr_df.drop([self.setting_dict["target_col"],
                                self.category_col_name], axis=1)
        self.tr_y = tr_df[[self.setting_dict["target_col"]]]
        self.te_X = te_df.drop([self.setting_dict["target_col"],
                                self.category_col_name], axis=1)
        self.te_y = te_df[[self.setting_dict["target_col"]]]

        self.tr_y = np.array(self.tr_y.values).reshape(-1)
        self.te_y = np.array(self.te_y.values).reshape(-1)

        self.dataset_df = sel_df

        return self.tr_X, self.te_X, self.tr_y, self.te_y
