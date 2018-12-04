from common import download
import sys

# filename = 'urls_qq.txt'
# output_dir = 'videos_tencent'
filename = sys.argv[1]
output_dir = sys.argv[2]
download(filename, output_dir)
