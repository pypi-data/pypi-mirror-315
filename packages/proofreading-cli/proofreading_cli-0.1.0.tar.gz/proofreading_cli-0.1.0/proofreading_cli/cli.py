import sys
from typing import Dict, Tuple

import click
import pandas as pd
from proofreading_cli.api_client import ApiClient
from proofreading_cli.common import save
from proofreading_cli.config import Config
from proofreading_cli.constants import GC_API_KEY_ENV, RAW_HITS_DATASET_NAME
from proofreading_cli.paths import SETTINGS_PATH
from proofreading_cli.utils import (
    build_filters,
    format_filters,
    is_api_key_missing_from_env,
    is_start_date_after_end_date,
    validate_date,
)
from tabulate import tabulate

config = Config.load(SETTINGS_PATH)
gc_api_client = ApiClient(config)


@click.group()
def cli():
    pass


@click.command()
@click.option("--article-id", type=str, help="Specify the ID of the article.")
@click.option(
    "--subscription-id",
    type=str,
    help="Specify the subscription ID (default provided).",
)
@click.option(
    "--statuses",
    default=["Accepted", "Rejected", "Ignored"],
    type=click.Choice(["Skipped", "Open", "Accepted", "Rejected", "Ignored"]),
    multiple=True,
    help="Specify proofreading status (default: Open).",
)
@click.option(
    "--is-submitted", type=bool, default=True, help="Specify proofreading status."
)
@click.option(
    "--start-date",
    type=str,
    callback=validate_date,
    help="Specify start date for fetching hits. Format: (YYYY-MM-DD).",
    required=True,
)
@click.option(
    "--end-date",
    type=str,
    callback=validate_date,
    help="Specify end date for fetching hits. Format: (YYYY-MM-DD).",
)
@click.option(
    "--file-system",
    type=str,
    default=config.proofreading.data.path,
    help="Specify path to local directory where data should be saved.",
)
@click.option(
    "--inference",
    default=["model_0_0_1", "model_0_0_2"],
    type=click.Choice(["model_0_0_1", "model_0_0_2"]),
    multiple=True,
    help="Create an additional dataset with inference info cols(label, probability, and model_version).",
)
def hits(
    article_id: str,
    subscription_id: str,
    statuses: Tuple[str],
    is_submitted: bool,
    start_date: str,
    end_date: str,
    file_system: str,
    inference: Tuple[str],
):
    """Filter hits based on various criteria."""

    if is_api_key_missing_from_env():
        click.echo(
            click.style(
                f"\nExport {GC_API_KEY_ENV} environment variable.", fg="red", bold=True
            )
        )
        sys.exit(1)

    if is_start_date_after_end_date(start_date, end_date):
        click.echo(
            click.style(
                "\nStart date cannot be after the end date.", fg="red", bold=True
            )
        )
        sys.exit(1)

    filters: Dict[str, str] = build_filters(
        article_id, subscription_id, statuses, is_submitted, start_date, end_date
    )
    table_header, table_data = format_filters(filters)
    click.echo("\n 🚀 Preparing to launch your request... Buckle up! 🚀 ")
    click.echo("\n ``````````````````````` 🤖 ```````````````````````")
    click.echo(
        tabulate(
            table_data, headers=table_header, tablefmt="fancy_grid", numalign="center"
        )
    )

    try:
        hits: pd.DataFrame = gc_api_client.get_hits_by_date(params=filters)
        click.echo(click.style(f"\nFetched {len(hits)} hits from GC API.", fg="green"))

    except Exception as e:
        click.echo(
            click.style(
                f"\nError occurred while fetching hits: {e}", fg="red", bold=True
            )
        )
        sys.exit(1)

    save(path=file_system, data=hits, filename=RAW_HITS_DATASET_NAME)

    click.echo(
        click.style(
            f"\nData successfully saved at {file_system}", fg="green", bold=True
        )
    )


cli.add_command(hits)

if __name__ == "__main__":
    cli()
