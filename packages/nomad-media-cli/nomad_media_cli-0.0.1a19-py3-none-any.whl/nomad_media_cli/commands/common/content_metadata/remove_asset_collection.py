import click
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The id of the asset.")
@click.option("--collection-id", required=True, help="The id of the collection.")
@click.pass_context
def remove_asset_collection(ctx, id, collection_id):
    """Remove collection from asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]
    
    try:
        nomad_sdk.remove_tag_or_collection("collection", id, "asset", collection_id)
        click.echo({ "message": "Collection removed from asset." })
    except Exception as e:
        click.echo({ "error": f"Error removing collection from asset: {e}" })