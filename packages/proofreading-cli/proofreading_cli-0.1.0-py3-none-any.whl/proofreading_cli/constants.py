from typing import Dict

from proofreading_cli.config import Config
from proofreading_cli.paths import SEARCH_DIMENSION_MAPING

RAW_HITS_DATASET_NAME = "hits.parquet"

GC_API_KEY_ENV = "GC_API_KEY"

search_dimension_mapping = Config.load(SEARCH_DIMENSION_MAPING)
SEARCH_DIMENSION_MAPPING_DICT: Dict = (
    search_dimension_mapping.search.dimension.mapping.to_dict()
)
