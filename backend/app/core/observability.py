from langfuse import get_client
from typing import Optional, Literal

langfuse = get_client()

ScoreType = Literal["NUMERIC", "BOOLEAN", "CATEGORICAL"]

def score_trace(
    name: str,
    value: float | bool | str,
    data_type: ScoreType,
    comment: Optional[str] = None,
):
    langfuse.score_current_trace(
        name=name,
        value=value,
        data_type=data_type,
        comment=comment,
    )


def score_span(
    name: str,
    value: float | bool | str,
    data_type: ScoreType,
    comment: Optional[str] = None,
):
    langfuse.score_current_span(
        name=name,
        value=value,
        data_type=data_type,
        comment=comment,
    )
