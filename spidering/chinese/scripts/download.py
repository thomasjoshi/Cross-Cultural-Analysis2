from parser import Parser
import sys

if len(sys.argv) < 3:
    print('Usage: python3 script.py keyword source1 [source2] [...]')
    print('For example: python3 download.py alphago iqiyi.com qq.com')
    sys.exit(1)

keyword = sys.argv[1]
sources = sys.argv[2:]
data_filename = keyword + '_data'
download_folder = keyword + '_videos'

parser = Parser()
parser.load_data(data_filename)
parser.download(download_folder, filters=tuple(sources))
