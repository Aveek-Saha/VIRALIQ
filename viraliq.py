import click
from database_clustering import *

@click.group()
@click.version_option()
def cli():
    """VIRALIQ.
    This is a command line program to search for videos using an image query. 
    First create embeddings for your videos and then search them quickly
    using an image.
    """

@click.command()
@click.option("cluster_type",
              '--database',
              default=True,
              flag_value="database",
              help="Cluster entire video database")
@click.option("cluster_type",
              '--video',
              flag_value="video",
              help="Cluster individual videos")
@click.argument("dir", type=click.Path(exists=True))
def cluster(cluster_type, dir):
    click.echo(cluster_type)
    click.echo(click.format_filename(dir))

    

@click.command()
@click.argument("img", type=click.Path(exists=True))
def search(img):
    click.echo(click.format_filename(img))

cli.add_command(cluster)
cli.add_command(search)