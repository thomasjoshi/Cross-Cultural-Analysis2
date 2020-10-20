import argparse
from src.spidering.get_metadata import get_metadata
from src.spidering.download import download
from src.tool.profiler import profile


def main():
    """
    The main function of the project
    """
    # Parse arguments
    parser = argparse.ArgumentParser(description='Cross Cultural Analysis')
    parser.add_argument(
        '-k', '--key', help='key for Youtube API, string or path to text file')
    args = parser.parse_args()

    # Get video metadata
    profile(get_metadata, ("Modi NDTV", 10,
                           "results/Modi/NDTV/video_metadata", False, args.key, ["youtube"]))
    profile(get_metadata, ("Modi Republic World", 10,
                           "results/Modi/republic_world/video_metadata", False, args.key, ["youtube"]))

    # Download videos
    profile(download, ("results/Modi/NDTV/video_metadata/metadata",
                       "results/Modi/NDTV/audios", "results/Modi/NDTV/videos", ["youtube"]))
    profile(download, ("results/Modi/republic_world/video_metadata/metadata",
                       "results/Modi/republic_world/audios", "results/Modi/republic_world/videos", ["youtube"]))


if __name__ == '__main__':
    main()
