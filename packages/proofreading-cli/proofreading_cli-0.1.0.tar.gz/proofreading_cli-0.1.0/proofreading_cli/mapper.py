from proofreading_cli.constants import SEARCH_DIMENSION_MAPPING_DICT


def map_hit_item(item: dict) -> dict:
    return {
        "hit_id": item["id"],
        "search_query_id": item["searchQuery"]["id"],
        "subscription_id": item["searchQuery"]["subscriptionId"],
        "article_id": item["articleId"],
        "proofreading_type": item["searchQuery"]["productionMetadata"][
            "proofreadingType"
        ],
        "proofreading_timestamp": item["proofreading"]["timestamp"],
        "query": item["searchQuery"]["query"],
        "search_dimension_id": item["searchQuery"]["searchDimensionId"],
        "search_dimension_name": SEARCH_DIMENSION_MAPPING_DICT[
            item["searchQuery"]["searchDimensionId"]
        ],
        "lectorate_search_term": item["searchQuery"]["lectorateSearchTerm"],
        "text": item["markedText"],
        "proofreading_status": item["proofreading"]["status"],
    }
