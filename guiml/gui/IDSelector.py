
import random
import ipywidgets as widgets
import pandas as pd


class IDSelector:
    """
    select ids
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.train_ids = list(self.df.index)
        self.test_ids = []

    def selector(self):
        select_train_id_w = widgets.SelectMultiple(
            options=self.train_ids,
            description='Train ID',
        )
        select_test_id_w = widgets.SelectMultiple(
            options=self.test_ids,
            description='Test ID',
        )

        # button click
        def add_button_clicked(b):
            ids = select_train_id_w.value

            self.test_ids.extend(ids)
            select_test_id_w.options = sorted(self.test_ids)

            for i in ids:
                self.train_ids.remove(i)
            select_train_id_w.options = sorted(self.train_ids)

        add_button = widgets.Button(description="->")
        add_button.on_click(add_button_clicked)

        def remove_button_clicked(b):
            ids = select_test_id_w.value

            self.train_ids.extend(ids)
            select_train_id_w.options = sorted(self.train_ids)

            for i in ids:
                self.test_ids.remove(i)
            select_test_id_w.options = sorted(self.test_ids)

        remove_button = widgets.Button(description="<-")
        remove_button.on_click(remove_button_clicked)

        # for random data select
        random_split_slider_w = widgets.IntSlider(
            value=80, min=0, max=100, description='Train (%)')

        def random_button_clicked(b):
            tot_records = self.df.shape[0]
            n_test = int(tot_records*random_split_slider_w.value/100)

            all_ids = list(self.df.index)
            random.shuffle(all_ids)
            self.train_ids = all_ids[:n_test]
            self.test_ids = all_ids[n_test:]

            select_train_id_w.options = sorted(self.train_ids)
            select_test_id_w.options = sorted(self.test_ids)

        random_button = widgets.Button(description="Random Split")
        random_button.on_click(random_button_clicked)

        display(
            widgets.HBox([select_train_id_w, select_test_id_w]),
            widgets.HBox([remove_button, add_button]),
            widgets.HBox([random_split_slider_w, random_button]),
        )
