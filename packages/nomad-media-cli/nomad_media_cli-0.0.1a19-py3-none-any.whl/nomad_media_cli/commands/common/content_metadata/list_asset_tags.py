from nomad_media_cli.helpers.utils import initialize_sdk
from nomad_media_cli.helpers.get_content_definition_id import get_content_definition_id

import click
import json
import sys

@click.command()
@click.option("--id", required=True, help="Asset id to list the tags for.")
@click.pass_context
def list_asset_tags(ctx, id):
    """List tags"""    
    
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]

    try:    
        asset_metadata = nomad_sdk.get_asset_details(id)
        
        tags = asset_metadata["tags"]
        tags = [collection["description"] for collection in tags]
        
        click.echo(json.dumps(tags, indent=4))

    except Exception as e:
        click.echo({ "error": f"Error listing tags: {e}" })
        sys.exit(1)