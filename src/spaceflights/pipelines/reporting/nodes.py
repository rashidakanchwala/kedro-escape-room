"""
This is a boilerplate pipeline 'reporting'
generated using Kedro 0.18.1
"""

from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import PIL
import plotly.express as px
import seaborn as sn
from plotly import graph_objects as go

from .image_utils import DrawTable


def make_cancel_policy_bar_chart(
    model_input_data: pd.DataFrame, top_counties: int = 20
) -> pd.DataFrame:
    """This function performs a group by on the input table, limits the
    results to the top n countries based on price and returns the
    data needed to visualise a stacked bar chart. The DataFrame is
    rendered as a Plot using the YAML API exposed in the Kedro Catalog.

    Args:
        model_input_data (pd.DataFrame): The data to plot
        top_counties (int, optional): [description]. Defaults to 20.

    Returns:
        pd.DataFrame: The aggregated data ready for visualisation
    """
    country_policy_df = (
        model_input_data.groupby(["company_location", "cancellation_policy"])["price"]
        .sum()
        .reset_index()
    )

    high_value_countries = (
        model_input_data.groupby("company_location")
        .price.sum()
        .sort_values()
        .head(top_counties)
        .index
    )

    high_value_filter = country_policy_df.company_location.isin(high_value_countries)
    return country_policy_df[high_value_filter]


def make_price_histogram(model_input_data: pd.DataFrame) -> go.Figure:
    """This function retrieves the two key columns needed to visualise the
    price-engine histogram. We then prepare the Plotly figure using the
    Plotly Python API

    Args:
        model_input_data (pd.DataFrame): The data to plot

    Returns:
        BaseFigure: Plotly object which is serialised as JSON for rendering
    """
    price_data_df = model_input_data.loc[:, ["price", "engine_type"]]
    p = np.random.dirichlet([1, 1, 1])
    price_data_df["engine_type"] = np.random.choice(
        ["Quantum", "Plasma", "Nuclear"], len(price_data_df), p=p
    )
    plotly_object = px.histogram(
        data_frame=price_data_df, x="price", log_x=True, color="engine_type"
    )
    return plotly_object


def make_price_analysis_image(model_input_table: pd.DataFrame) -> pd.DataFrame:
    """Analyze average price and review scores by cancellation policy.

    Args:
        model_input_table (pd.DataFrame): Input data with 'price' and 'review_scores_rating'.

    Returns:
        pd.DataFrame: Aggregated data showing mean price and review scores.
    """
    analysis_df = (
        model_input_table.groupby("cancellation_policy")[["price", "review_scores_rating"]]
        .mean()
        .reset_index()
    )
    return analysis_df


def create_feature_importance_plot(features: pd.DataFrame) -> go.Figure:
    sorted_features = features.sort_values(by="Score", ascending=True)
    plotly_object = px.bar(
        sorted_features,
        x="Score",
        y="Feature",
        color="Score",
        color_continuous_scale="RdBu",
    )
    return plotly_object


def create_matplotlib_chart(companies: pd.DataFrame) -> plt:
    random_actuals = np.random.randint(2, size=11)
    random_predicted = np.random.randint(2, size=11)

    data = {"y_Actual": random_actuals, "y_Predicted": random_predicted}
    plt.style.use("dark_background")
    df = pd.DataFrame(data, columns=["y_Actual", "y_Predicted"])
    confusion_matrix = pd.crosstab(
        df["y_Actual"], df["y_Predicted"], rownames=["Actual"], colnames=["Predicted"]
    )
    sn.heatmap(confusion_matrix, annot=True)
    return plt


def get_top_shuttles_data(model_input_table: pd.DataFrame) -> Dict:
    """This function retrieves the head from the input table
    and converts them into a JSON dataset.

    Args:
        model_input_table (pd.DataFrame): The data to retrieve the top N rows from
        top_n (int, optional): The number of top rows to retrieve. Defaults to 5.

    Returns:
        str: A JSON string representing the top N rows of the dataset.
    """

    # Get the top N rows of the model input table
    top_shuttle_df = model_input_table.head(5)
    top_shuttle_json = top_shuttle_df.to_dict(orient="records")
    return top_shuttle_json


import codecs

def decode_final_clue(encoded_text: str, feature_importance_output) -> str:
    """Decode the final ROT13 clue."""
    decoded = codecs.decode(encoded_text, "rot_13")
    print("\n🗝 The final clue has been revealed.")
    return decoded
