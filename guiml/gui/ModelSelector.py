import ipywidgets as widgets


class ModelSelector:
    """
    select ML models
    """

    def __init__(self, model_list: list):
        self.model_list = model_list

        model_name_list = [
            f"{i}: {str(name)}" for i, name in enumerate(model_list)]
        selcted_model_name = model_name_list[0]

        self.select_model_w = widgets.Select(
            options=model_name_list,
            description='Select model',
            value=selcted_model_name,
        )
        self.select_model_w.layout.width = "80%"

    def __call__(self):
        return self.select_model_w

    def load(self):
        selected_model_name = self.select_model_w.value
        selected_id = int(selected_model_name.split(":")[0])
        print(f"use {selected_model_name}")
        # return selected_id

        return self.model_list[selected_id]
