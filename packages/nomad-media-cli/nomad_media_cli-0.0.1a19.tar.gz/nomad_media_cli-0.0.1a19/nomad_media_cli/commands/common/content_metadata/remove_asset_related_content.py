import click
from nomad_media_cli.helpers.utils import initialize_sdk

@click.command()
@click.option("--id", required=True, help="The id of the asset.")
@click.option("--related-content-id", required=True, help="The id of the related content.")
@click.pass_context
def remove_asset_related_content(ctx, id, related_content_id):
    """Remove related content to asset"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]
    
    try:
        nomad_sdk.delete_related_content(id, related_content_id, "asset")
        click.echo({ "message": "Related content removed to asset." })
    except Exception as e:
        click.echo({ "error": f"Error removing related content to asset: {e}" })