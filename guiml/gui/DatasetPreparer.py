from ..GUIML import GUIML
import numpy as np


class DatasetPreparer(GUIML):
    def __init__(self, save_name="guiml"):
        super().__init__(save_name)

    def __call__(self, sel_df, id_selector):
        """
        automatically prepare dataset by random splitting
        """

        sel_df.loc[id_selector.train_ids, self.category_col_name] = "train"
        sel_df.loc[id_selector.test_ids, self.category_col_name] = "test"

        # drop nan
        sel_df = sel_df[sel_df[self.setting["csv"][self.csv]["target_col"]]
                        == sel_df[self.setting["csv"][self.csv]["target_col"]]]

        tr_df = sel_df[sel_df[self.category_col_name] == "train"]
        te_df = sel_df[sel_df[self.category_col_name] == "test"]

        # set X and y
        self.tr_X = self.prepare_X(tr_df)
        self.tr_y = tr_df[[self.setting["csv"][self.csv]["target_col"]]]

        self.te_X = self.prepare_X(te_df)
        self.te_y = te_df[[self.setting["csv"][self.csv]["target_col"]]]

        self.tr_y = np.array(self.tr_y.values).reshape(-1)
        self.te_y = np.array(self.te_y.values).reshape(-1)

        return self.tr_X, self.te_X, self.tr_y, self.te_y, sel_df

    def prepare_X(self, df):
        """
        get explanatory variables
        """

        for col in [self.setting["csv"][self.csv]["target_col"],
                    self.category_col_name,
                    "predicted"]:

            if col in df.columns:
                df = df.drop(col, axis=1)
        return df
