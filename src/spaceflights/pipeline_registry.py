"""Project pipelines."""

from typing import Dict

from kedro.pipeline import Pipeline, pipeline, node

from spaceflights.pipelines import data_ingestion as di
from spaceflights.pipelines import feature_engineering as fe
from spaceflights.pipelines import modelling as mod
from spaceflights.pipelines import reporting as rep


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.

    """
    
    mistrust_pipeline = pipeline([
        node(
        func= lambda x,y: x,
        inputs=["sensitive_data","prm_shuttle_company_reviews"],
        outputs=None,
        name="sensitive_node",
    )])
    
    
    ingestion_pipeline = di.create_pipeline()

    feature_pipeline = fe.create_pipeline()

    modelling_pipeline = mod.create_pipeline(
        model_types=["linear_regression", "random_forest"]
    )

    reporting_pipeline = rep.create_pipeline()
    

    return {
        "__default__": (
            ingestion_pipeline
            + feature_pipeline
            + mistrust_pipeline
            + modelling_pipeline
            + reporting_pipeline
        ),
        "data_ingestion": ingestion_pipeline,
        "modelling_stage": modelling_pipeline,
        "feature_engineering": feature_pipeline,
        "reporting_stage": reporting_pipeline,
        "pre_modelling": ingestion_pipeline + feature_pipeline,
    }