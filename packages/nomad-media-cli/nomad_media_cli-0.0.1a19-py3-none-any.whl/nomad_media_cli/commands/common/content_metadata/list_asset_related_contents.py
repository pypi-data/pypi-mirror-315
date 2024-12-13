from nomad_media_cli.helpers.utils import initialize_sdk
from nomad_media_cli.helpers.get_content_definition_id import get_content_definition_id

import click
import json
import sys

@click.command()
@click.option("--id", required=True, help="Asset id to list the related contents for.")
@click.pass_context
def list_asset_related_contents(ctx, id):
    """List related contents"""    
    
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:    
        asset_metadata = nomad_sdk.get_asset_details(id)
        
        related_contents = asset_metadata["relatedContent"]
        
        click.echo(json.dumps(related_contents, indent=4))

    except Exception as e:
        click.echo({ "error": f"Error listing related contents: {e}" })
        sys.exit(1)