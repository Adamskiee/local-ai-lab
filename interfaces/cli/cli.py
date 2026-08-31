import click
import requests
import json
import sys

API_URL = "http://localhost:8000"

@click.group()
def cli():
    """Local Code Explainer CLI."""
    pass

@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
def index(path):
    """Index a directory."""
    click.echo(f"Indexing {path}...")
    try:
        response = requests.post(f"{API_URL}/index", json={"path": path})
        response.raise_for_status()
        click.echo("Success:")
        click.echo(json.dumps(response.json(), indent=2))
    except requests.exceptions.HTTPError as e:
        error_detail = e.response.text
        try:
            error_detail = e.response.json().get("detail", error_detail)
        except Exception:
            pass
        click.echo(f"API Error ({e.response.status_code}): {error_detail}", err=True)
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        click.echo(f"Error connecting to API. Is the FastAPI server running on {API_URL}?", err=True)
        click.echo(f"Details: {e}", err=True)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error connecting to API: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('project_root', type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True))
@click.argument('message')
def chat(project_root, message):
    """Chat with the indexed project."""
    try:
        response = requests.post(f"{API_URL}/chat", json={"project_root": project_root, "message": message})
        response.raise_for_status()
        data = response.json()
        click.echo("\nResponse:")
        click.echo(data.get("response", ""))
        
        sources = data.get("sources", [])
        if sources:
            click.echo("\nSources:")
            for source in sources:
                click.echo(f"  - {source.get('file_path')}:{source.get('start_line')}")
    except requests.exceptions.HTTPError as e:
        error_detail = e.response.text
        try:
            error_detail = e.response.json().get("detail", error_detail)
        except Exception:
            pass
        click.echo(f"API Error ({e.response.status_code}): {error_detail}", err=True)
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        click.echo(f"Error connecting to API. Is the FastAPI server running on {API_URL}?", err=True)
        click.echo(f"Details: {e}", err=True)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error connecting to API: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
