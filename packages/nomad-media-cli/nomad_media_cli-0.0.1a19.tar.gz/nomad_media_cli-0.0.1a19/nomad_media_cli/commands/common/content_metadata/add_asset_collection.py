import click
import json
import sys
from nomad_media_cli.helpers.utils import initialize_sdk
from nomad_media_cli.helpers.get_content_definition_id import get_content_definition_id

@click.command()
@click.option("--id", required=True, help="The ID of the content.")
@click.option("--url", help="The Nomad URL of the Asset (file or folder) to add the collection to (bucket::object-key).")
@click.option("--object-key", help="Object-key only of the Asset (file or folder) to add the collection to. This option assumes the default bucket that was previously set with the `set-bucket` command.")
@click.option("--collection-name", help="The name of the collection.")
@click.option("--collection-id", help="The ID of the collection.")
@click.pass_context
def add_asset_collection(ctx, id, url, object_key, collection_name, collection_id):
    """Add collection to content"""
    initialize_sdk(ctx)
    nomad_sdk = ctx.obj["nomad_sdk"]
    
    if url or object_key:
        if url and "::" not in url:
            click.echo({ "error": "Please provide a valid path or set the default bucket." })               
            sys.exit(1)
        if object_key:
            if "bucket" in ctx.obj:
                url = f"{ctx.obj['bucket']}::{object_key}"
            else:
                click.echo({ "error": "Please set bucket using `set-bucket` or use url." })
                sys.exit(1)
                
        url_search_results = nomad_sdk.search(None, None, None, [{
            "fieldName": "url",
            "operator": "equals",
            "values": url
        }], None, None, None, None, None, None, None, None, None, None, None)
        
        if not url_search_results or len(url_search_results["items"] == 0):
            click.echo({ "error": f"URL {url} not found." })
            sys.exit(1)
            
        id = url_search_results["items"][0]["id"]

    try:
        offset = 0
        collection_content_definition_id = get_content_definition_id(ctx, "Collection")
        while not collection_id:
            collections = nomad_sdk.search(None, offset, None, [{
                "fieldName": "contentDefinitionId",
                "operator": "equals",
                "values": collection_content_definition_id
            }], None, None, None, None, None, None, None, None, None, None, None)
            
            if len(collections["items"]) == 0:
                break
            
            for collection in collections["items"]:
                if collection.get("title") == collection_name:
                    collection_id = collection["id"]
                    break
                
            offset += 1

        if collection_id: collection_name = None

        result = nomad_sdk.add_tag_or_collection(
            "collection",
            id,
            "asset",
            collection_name,
            collection_id,
            not collection_id
        )
        
        click.echo(json.dumps(result, indent=4))

    except Exception as e:
        click.echo({"error": f"Error adding collection: {e}"})
        sys.exit(1)