from parser import Parser
import sys

if len(sys.argv) < 4:
    print('Usage: python3 script.py keyword output_folder source1 [source2] [...]')
    print('For example: python3 download.py alphago alphago_videos iqiyi.com qq.com')
    sys.exit(1)

keyword = sys.argv[1]
download_folder = sys.argv[2]
sources = sys.argv[3:]
data_filename = keyword + '_data'

parser = Parser()
parser.load_data(data_filename)
parser.download(download_folder, filters=tuple(sources))
