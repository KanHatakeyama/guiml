# model definition
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline


numeric_preprocessor = Pipeline(
    steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('scaler', StandardScaler()),
    ]
)

categorical_preprocessor = Pipeline(
    steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore')),
    ]
)


def prepare_pipeline(parsed_df, model):
    number_cols, category_cols = get_number_and_category_cols(
        parsed_df)
    pipeline = make_pipeline(
        ColumnTransformer(
            [
                ('numerical', numeric_preprocessor, number_cols),
                ('categorical', categorical_preprocessor, category_cols)
            ]
        ),

        model
    )

    return pipeline


def get_number_and_category_cols(parsed_df):

    category_columns = list(parsed_df.select_dtypes(include='object').columns)
    data_df = parsed_df

    for col in category_columns:
        data_df[col] = data_df[col].astype(str)

    number_columns = list(parsed_df.select_dtypes(include='float').columns)

    return number_columns, category_columns
