from parser import Parser

init = False
parser = Parser()

query = 'alphago'
quantity = 150
url_filename = 'alphago_urls.txt'
data_filename = 'alphago_data'
title_filename = 'alphago_titles.txt'
desc_filename = 'alphago_descriptions.txt'

if init:
    parser.get_urls_bilibili(query, quantity, order=0, duration=1, tids_1=0, tids_2=0)
    parser.get_urls_tencent(query, quantity, duration=1)
    parser.get_urls_youku(query, quantity, duration=1)
    # parser.get_urls_iqiyi(query, quantity, source=1, duration=2)
    parser.save_urls(url_filename)
    parser.get_data()
    parser.save_urls(url_filename)
    parser.save_data(data_filename)
else:
    parser.load_data(data_filename)
# parser.download('Alphago')
# parser.export_titles(title_filename)
# parser.export_descriptions(desc_filename)
