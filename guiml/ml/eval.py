
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np


def evaluate_model(pipe, X, y):
    p_y = pipe.predict(X)

    res_dict = {}

    res_dict["r2"] = r2_score(p_y, y)
    res_dict["MAE"] = mean_absolute_error(p_y, y)
    res_dict["MSE"] = mean_squared_error(p_y, y)
    res_dict["RMSE"] = np.sqrt(res_dict["MSE"])

    return res_dict
