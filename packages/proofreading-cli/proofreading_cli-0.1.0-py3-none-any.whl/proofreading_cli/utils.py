import os
import re
from datetime import datetime
from typing import Any, Dict, List, Tuple

import click
from proofreading_cli.constants import GC_API_KEY_ENV


def validate_date(ctx: Any, param: Any, value: str) -> str:
    """Validates the date input format (YYYY-MM-DD)."""
    if value is not None:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise click.BadParameter(
                f"Invalid date format: '{value}'. Expected format: YYYY-MM-DD."
            )
    return value


def is_api_key_missing_from_env() -> bool:
    return GC_API_KEY_ENV not in os.environ


def is_start_date_after_end_date(start_date: str, end_date: str) -> bool:
    return bool(start_date and end_date and start_date > end_date)


def build_filters(
    article_id: str,
    subscription_id: str,
    statuses: Tuple[str],
    is_submitted: bool,
    start_date: str,
    end_date: str,
) -> Dict[str, str]:
    """Build a dictionary of filters based on provided options."""
    filters = {}

    if article_id:
        filters["article_id"] = article_id
    if subscription_id:
        filters["subscription_id"] = subscription_id
    if statuses:
        filters["statuses"] = statuses
    if is_submitted is not None:
        filters["is_submitted"] = is_submitted
    if start_date:
        filters["start_date"] = start_date
    if end_date:
        filters["end_date"] = end_date

    return filters


def format_filters(filters: Dict[str, str]) -> Tuple[List[str], List[str]]:
    table_header = [
        click.style("Filter", fg="yellow", bold=True),
        click.style("Value", fg="yellow", bold=True),
    ]

    table_data = [
        [click.style(key, fg="yellow"), click.style(value, fg="yellow")]
        for key, value in filters.items()
    ]

    return table_header, table_data
