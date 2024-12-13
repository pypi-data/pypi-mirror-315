#!/usr/bin/env python

from email.policy import default
import logging

import click

from typing import Optional

from bxbdbt.utils import (
    get_all_tags,
    get_manifest_sha,
    get_youngest_tag,
    print_version,
    DEFAULT_EXCLUDED_TAGS,
    filter_tags,
)


# load .env file
from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger(__name__)


@click.command()
@click.argument("registry_url", required=True)
@click.help_option("--help", "-h")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="Show version and license information",
)
@click.option(
    "--youngest-tag-only",
    is_flag=True,
    help="Return only the youngest tag",
)
@click.option(
    "--show-sha",
    is_flag=True,
    help="Show SHA256 digest for each tag",
)
@click.option(
    "--no-filter",
    is_flag=True,
    help="Disable filtering of tags",
)
def main(
    registry_url: Optional[str],
    debug: bool,
    youngest_tag_only: bool,
    show_sha: bool,
    no_filter: bool = False,
):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s",
    )

    if not registry_url:
        raise click.ClickException(
            "Registry URL must be provided if no Containerfile is specified"
        )

    if youngest_tag_only:
        tags = get_youngest_tag(registry_url)
        if tags:
            tags = [tags]  # Convert single tag to list for consistent handling
    else:
        tags = get_all_tags(registry_url)

    if not tags:
        logger.warning("No tags found after filtering")
        return

    if not no_filter:
        tags = filter_tags(tags, DEFAULT_EXCLUDED_TAGS)

    logger.debug(f"Found {len(tags)} tags after filtering")

    for tag in tags:
        if show_sha:
            sha = get_manifest_sha(registry_url, tag)
            if sha:
                click.echo(f"{tag}\t{sha}")
            else:
                click.echo(f"{tag}\t<sha not available>")
        else:
            click.echo(tag)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
