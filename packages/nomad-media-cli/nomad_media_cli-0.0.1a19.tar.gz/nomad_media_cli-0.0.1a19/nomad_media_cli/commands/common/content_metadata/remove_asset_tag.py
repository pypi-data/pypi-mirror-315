import click
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The id of the asset.")
@click.option("--tag-id", required=True, help="The id of the tag.")
@click.pass_context
def remove_asset_tag(ctx, id, tag_id):
    """Remove tag from asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]
    
    try:
        nomad_sdk.remove_tag_or_collection("tag", id, "asset", tag_id)
        click.echo({ "message": "tag removed from asset." })
    except Exception as e:
        click.echo({ "error": f"Error removing tag from asset: {e}" })