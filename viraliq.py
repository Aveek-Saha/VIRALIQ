import click
import os
import time

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

root = os.path.join(os.path.expanduser('~'), ".viraliq")
feats_path = os.path.join(root, "data", "feats", "resnet152")
metadata_path = os.path.join(root, "metadata")


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
    from database_clustering.video_to_image_feats import video_to_image_feats
    from database_clustering.create_video_embeddings import create_video_embeddings

    click.echo(f"Clustering type: {cluster_type}")
    click.echo(f"Video folder: {click.format_filename(dir)}")
    click.echo('Extracting video features:')
    video_to_image_feats(dir, feats_path, 2)
    click.echo('Creating embeddings:')
    create_video_embeddings(feats_path, metadata_path)


@click.command()
@click.argument("dir", type=click.Path(exists=True))
@click.argument("img", type=click.Path(exists=True))
@click.argument("num_results", default=10, type=int)
def search(img, dir, num_results):
    from database_clustering.retrieve_videos import get_video_ranks

    dir = click.format_filename(dir)
    query_image_path = click.format_filename(img)
    click.echo(f"Query image: {query_image_path}")

    x1 = time.time()
    video_ranks = get_video_ranks(query_image_path, feats_path, metadata_path)[:num_results]
    x2 = time.time()

    click.echo(f"Search time: {x2 - x1}\n")
    click.echo(f"Showing top {num_results} Video matches from {dir}")
    ranked_name = []
    for video in video_ranks:
        ranked_name.append(video.split(".npy")[0] + ".mp4")
        click.echo(video.split(".npy")[0] + ".mp4")


cli.add_command(cluster)
cli.add_command(search)
