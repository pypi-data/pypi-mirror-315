import click

from phnx.downloader.fragment_downloader import FragmentDownloader
from phnx.downloader.volume_downloader import VolumeDownloader


@click.group()
def cli():
    """phalanx: A versatile downloader for scrolls and fragments."""
    pass


@cli.command(name='download-volume')
@click.argument('scroll-name', required=True)
@click.option('--volpkg-name', default=None, help='Name of the volpkg (if multiple are available).')
@click.option('--output-path', required=True, help='The output path (the path of the full_scrolls directory).')
@click.option('--volume-id', default=None, help='Volume identifier.')
@click.option('--slices', default='all', help='Slice ranges to download (e.g., "1-5,10,15-20").')
def download_volume(scroll_name, volpkg_name, output_path, volume_id, slices):
    """Download slices from a volume."""
    downloader = VolumeDownloader()
    downloader.download(output_path=output_path, scroll_name=scroll_name, volpkg_name=volpkg_name, volume_id=volume_id,
                        slices=slices)


@cli.command(name='download-fragment')
@click.option('--output-dir', default='data', help='Output data root directory.')
@click.argument('scroll-name', required=True)
@click.option('--volpkg-name', default=None, help='Name of the volpkg (if multiple are available).')
@click.argument('fragment-id', required=True)
@click.option('--slices', default='all', help='Slice ranges to download (e.g., "0-10,15,20-25").')
@click.option('--mask', default=True, help='Download the mask for the fragment.')
def download_fragment(output_dir, scroll_name, volpkg_name, fragment_id, slices, mask):
    """Download slices from a fragment."""
    downloader = FragmentDownloader()
    downloader.download(
        output_dir=output_dir,
        scroll_name=scroll_name,
        volpkg_name=volpkg_name,
        fragment_id=fragment_id,
        slices=slices,
        mask=mask
    )


if __name__ == '__main__':
    cli()
