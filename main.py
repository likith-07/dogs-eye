from typing import Dict, Any

from pipeline.integrated_pipeline import IntegratedPipeline


def process_image(
    image_path: str
) -> Dict[str, Any]:

    pipeline = IntegratedPipeline(
        max_candidates=100,
        max_evaluations=10,
        verbose=True,
        provider_threshold=0.80
    )

    result = pipeline.execute(
        image_path
    )

    return result