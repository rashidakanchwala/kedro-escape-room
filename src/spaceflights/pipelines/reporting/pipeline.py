"""
This is a boilerplate pipeline 'reporting'
generated using Kedro 0.18.1
"""

from kedro.pipeline import Pipeline, node, pipeline

from spaceflights.pipelines.reporting.nodes import (
    create_feature_importance_plot,
    create_matplotlib_chart,
    get_top_shuttles_data,
    make_cancel_policy_bar_chart,
    make_price_analysis_image,
    make_price_histogram,
    decode_final_clue
)


def create_pipeline(**kwargs) -> Pipeline:
    """This is a simple pipeline which generates a series of plots"""
    return pipeline(
        [
            node(
                func=make_cancel_policy_bar_chart,
                inputs="prm_shuttle_company_reviews",
                outputs="cancellation_policy_breakdown",
                name="cancel_policy_bar_chart",
            ),
            node(
                func=make_price_histogram,
                inputs="prm_shuttle_company_reviews",
                outputs="price_histogram",
                name="price_histogram",
            ),
            node(
                func=make_price_analysis_image,
                inputs="prm_shuttle_company_reviews",
                outputs="cancellation_policy_grid",
                name="price_analysis_image",
            ),
            node(
                func=create_feature_importance_plot,
                inputs="feature_importance_output",
                outputs="feature_importance",
                name="feature_importance_plot",
            ),
            node(
                func=create_matplotlib_chart,
                inputs="prm_shuttle_company_reviews",
                outputs="confusion_matrix",
                name="confusion_matrix",
            ),
            node(
                func=get_top_shuttles_data,
                inputs="prm_shuttle_company_reviews",
                outputs="top_shuttle_data",
                name="top_shuttle_data",
            ),
            node(
            func=decode_final_clue,
            inputs=["price_histogram_revised","feature_importance_output"],
            outputs="final_clue",
            name="decode_final_clue_node",
        )
        ],
        inputs=["prm_shuttle_company_reviews", "feature_importance_output"],
        namespace="reporting",
    )
