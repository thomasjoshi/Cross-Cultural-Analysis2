import argparse
from src.spidering.get_metadata import get_metadata
from src.spidering.spider import Spider
from src.spidering.download import download
from src.tool.profiler import profile

def main():
    """
    The main function of the project
    """
    parser = argparse.ArgumentParser(description='Cross Cultural Analysis')
    parser.add_argument(
        '-k', '--key', help='key for Youtube API, string or path to text file')
    args = parser.parse_args()
    sources = [Spider.TENCENT]

    # Get video metadata
    profile(get_metadata, ("AlphaGo", 10,
                           "results/AlphaGo/Tencent/video_metadata", False, args.key, sources))

    # Download videos
    profile(download, ("results/AlphaGo/Tencent/video_metadata/metadata",
                       "results/AlphaGo/Tencent/audios", "results/AlphaGo/Tencent/videos", sources))

if __name__ == '__main__':
    main()