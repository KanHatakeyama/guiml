import os
import joblib

TEMP_SAVE_FOLDER = "_guiml"
CATEGORY_COL_NAME = "dataset_category"


class GUIML:
    def __init__(self, save_name="guiml",
                 # category_col_name="dataset_category"
                 ):
        """

        """
        self.category_col_name = CATEGORY_COL_NAME
        self.save_name = save_name
        self.setting_path = TEMP_SAVE_FOLDER+"/"+save_name+".bin"

        self.csv = "unknown_csv"
        # load dict data
        if not os.path.exists(TEMP_SAVE_FOLDER):
            os.mkdir(TEMP_SAVE_FOLDER)

        if not os.path.exists(self.setting_path):
            self.setting = {}
            self.setting["csv"] = {}
            self.setting["csv"]["unknown_csv"] = {}

        else:
            self.setting = joblib.load(self.setting_path)
            self.csv = self.setting["current_csv"]

    def _save(self):
        joblib.dump(self.setting, self.setting_path)
