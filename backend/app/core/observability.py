from langfuse import get_client

langfuse = get_client()

def score_trace(
    name: str,
    value: float,
    comment: str | None = None,
):
    langfuse.score_current_trace(
        name=name,
        value=value,
        data_type="NUMERIC",
        comment=comment,
    )

def score_span(
    name: str,
    value: float,
    comment: str | None = None,
):
    langfuse.score_current_span(
        name=name,
        value=value,
        data_type="NUMERIC",
        comment=comment,
    )
