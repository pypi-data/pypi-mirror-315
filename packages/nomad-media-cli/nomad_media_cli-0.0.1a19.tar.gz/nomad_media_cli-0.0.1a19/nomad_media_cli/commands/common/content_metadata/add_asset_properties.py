import click
import json
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The id of the asset.")
@click.option("--name", help="The display name of the asset.")
@click.option("--date", help="The display date of the asset.")
@click.option("--custom-properties", help="The custom properties of the asset. Must be in JSON format. Example: '{\"key\": \"value\"}'")
@click.pass_context
def add_asset_properties(ctx, id, name, date, custom_properties):
    """Add custom properties to asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]
    
    try:
        try:
            custom_properties = json.loads(custom_properties)
        except:
            click.echo({ "error": "Custom properties must be in JSON format." })
            return      

        nomad_sdk.add_custom_properties(id, name, date, custom_properties)
        click.echo({ "message": "Custom properties added to asset." })
    except Exception as e:
        click.echo({ "error": f"Error adding custom properties to asset." })