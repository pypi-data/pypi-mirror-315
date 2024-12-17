from femtum_sdk.core.component_pb2 import TagDto
import pandas as pd


def ApplyTagsToDataframe(
    dataframe: pd.DataFrame,
    tags: list[TagDto],
) -> pd.DataFrame:

    for tag in tags:
        dataframe[tag.Key] = tag.Value if tag.Value else True

    return dataframe
