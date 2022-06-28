from ..GUIML import GUIML
import pandas as pd
import ipywidgets as widgets
from .mol_plot import bokeh_plot, select_plot_columns
import seaborn as sns


class PlotSelector(GUIML):
    def __init__(self, save_name="guiml"):
        super().__init__(save_name)

    def __call__(self, df):
        """
        plot dataframe
        """

        first_column = list(df.columns)[0]
        # initiate dict
        if "plot_cols" not in self.setting["csv"][self.csv]:
            plot_cols = {}
            for k in ["x", "y", "hue"]:
                if k not in plot_cols:
                    plot_cols[k] = first_column

            self.setting["csv"][self.csv]["plot_cols"] = plot_cols

        for k in ["x", "y", "hue"]:
            if self.setting["csv"][self.csv]["plot_cols"][k] not in list(df.columns):
                self.setting["csv"][self.csv]["plot_cols"][k] = first_column

        # apply selected values
        try:
            self.setting["csv"][self.csv]["plot_cols"]["x"] = self.w_x.value
            self.setting["csv"][self.csv]["plot_cols"]["y"] = self.w_y.value
            self.setting["csv"][self.csv]["plot_cols"]["hue"] = self.w_hue.value
            self.setting["csv"][self.csv]["plot_cols"]["program"] = self.w_plot_program.value
        except:
            self.setting["csv"][self.csv]["plot_cols"]["program"] = "Seaborn"

        for k in ["x", "y", "hue"]:
            if self.setting["csv"][self.csv]["plot_cols"][k] not in list(df.columns):
                self.setting["csv"][self.csv]["plot_cols"][k] = first_column
        # select box
        box, self.w_x, self.w_y, self.w_hue = select_plot_columns(df,
                                                                  self.setting["csv"][self.csv]["plot_cols"]["x"],
                                                                  self.setting["csv"][self.csv]["plot_cols"]["y"],
                                                                  self.setting["csv"][self.csv]["plot_cols"]["hue"],
                                                                  )
        # plot program
        self.w_plot_program = widgets.Dropdown(
            description='Plot program',
            options=["Seaborn", "Bokeh"],
            value=self.setting["csv"][self.csv]["plot_cols"]["program"],
        )
        display(box, self.w_plot_program)

        # plot graph

        if self.w_plot_program.value == "Seaborn":
            return sns.scatterplot(data=df,
                                   x=self.setting["csv"][self.csv]["plot_cols"]["x"],
                                   y=self.setting["csv"][self.csv]["plot_cols"]["y"],
                                   hue=self.setting["csv"][self.csv]["plot_cols"]["hue"],
                                   )
        else:
            return bokeh_plot(df,
                              self.setting["csv"][self.csv]["plot_cols"]["x"],
                              self.setting["csv"][self.csv]["plot_cols"]["y"],
                              self.setting["csv"][self.csv]["plot_cols"]["hue"],)
