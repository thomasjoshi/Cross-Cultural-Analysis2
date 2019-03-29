from parser import Parser
import sys

# query = '章莹颖'
# keyword = 'yingying_zhang'
# quantity = 200
# init = True

if len(sys.argv) < 5:
    print('Usage: python3 script.py query keyword quantity fresh_run?')
    print('For example: python3 run_parser.py alphago alphago 150 y')
    sys.exit(1)

query = sys.argv[1]
keyword = sys.argv[2]
quantity = int(sys.argv[3])
init = sys.argv[4][0].lower() == 'y'
url_filename = keyword + '_urls.txt'
data_filename = keyword + '_data'
title_filename = keyword + '_titles.txt'
desc_filename = keyword + '_descriptions.txt'
download_folder = keyword + '_videos'

parser = Parser()
if init:
    parser.get_urls_bilibili(query, quantity, order=0, duration=1, tids_1=0, tids_2=0)
    parser.save_urls(url_filename)
    parser.get_urls_tencent(query, quantity, duration=1)
    parser.save_urls(url_filename)
    parser.get_urls_iqiyi(query, quantity, source=1, duration=1)
    parser.save_urls(url_filename)
    parser.get_urls_youku(query, quantity, duration=1)
    parser.save_urls(url_filename)
    parser.get_data()
    parser.save_urls(url_filename)
    parser.save_data(data_filename)
else:
    parser.load_data(data_filename)
parser.export_titles(title_filename)
parser.export_descriptions(desc_filename)
