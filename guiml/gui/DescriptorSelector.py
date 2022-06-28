from ..GUIML import GUIML
import pandas as pd
import ipywidgets as widgets
from ..Chem.Autodescriptor import AutoDescriptor, RDKitDescriptors, GroupContMethod, MordredDescriptor, Fingerprint


class DescriptorSelector(GUIML):
    def __init__(self, save_name="guiml"):
        super().__init__(save_name)

    def __call__(self, df):
        """
        select SMILES column and descriptor types
        """
        try:
            self.csv = self.csv
        except:
            self.csv = "unknown_csv"

        if "SMILES_col" not in self.setting["csv"][self.csv]:
            self.setting["csv"][self.csv]["SMILES_col"] = None
        if "descriptors" not in self.setting["csv"][self.csv]:
            self.setting["csv"][self.csv]["descriptors"] = ()

        self._smiles_col_w = widgets.Select(
            description='SMILES',
            options=list(df.columns),
            value=self.setting["csv"][self.csv]["SMILES_col"],
        )

        self._mol_descriptor_w = widgets.SelectMultiple(
            description='Select descriptors',
            options=["RDKit", "Mordred(2D)", "Mordred(3D)",
                     "JR", "Avalon Fingerprint"],
            value=self.setting["csv"][self.csv]["descriptors"]
        )

        self.df = df
        return display(
            self._smiles_col_w,
            self._mol_descriptor_w)

    def load(self, smiles_list=None):
        """
        calculate molecular descriptors
        """

        if self._smiles_col_w.value is None:
            raise ValueError("Please select a SMILES column")

        only_desc_df_mode = True
        if smiles_list is None:
            smiles_list = list(self.df[self._smiles_col_w.value])
            only_desc_df_mode = False

        # update form info
        self.setting["csv"][self.csv]["SMILES_col"] = self._smiles_col_w.value
        self.setting["csv"][self.csv]["descriptors"] = self._mol_descriptor_w.value
        self._save()

        # initiate calculator
        calculators = []
        for desc_name in self.setting["csv"][self.csv]["descriptors"]:
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

        # merge to original DF
        desc_df = desc_df.drop(
            self.setting["csv"][self.csv]["SMILES_col"], axis=1)

        merge_cols = list(desc_df.columns)
        merge_cols = [i for i in merge_cols if i not in list(self.df.columns)]
        merge_df = pd.merge(self.df, desc_df[merge_cols], left_index=True,
                            right_index=True, how="outer")
        return merge_df
