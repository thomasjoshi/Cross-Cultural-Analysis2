from parser import Parser

init = True
parser = Parser()

query = 'alphago'
quantity = 150
keyword = 'alphago'
url_filename = keyword + '_urls.txt'
data_filename = keyword + '_data'
title_filename = keyword + '_titles.txt'
desc_filename = keyword + '_descriptions.txt'
download_folder = keyword + '_videos'

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

# parser.download(download_folder, sources=(1, 2, 3, 4))
