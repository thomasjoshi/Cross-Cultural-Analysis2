from parser import Parser

init = True
parser = Parser()

if init:
    parser.get_urls_bilibili('alphago', 5)
    parser.get_urls_tencent('alphago', 5)
    parser.get_urls_youku('alphago', 5)
    parser.get_urls_iqiyi('alphago', 5)
    parser.save_urls('urls.txt')
    parser.get_data()
    parser.save_urls('urls.txt')
    parser.save_data('data')
else:
    parser.load_data('data')
# parser.download('Alphago')
parser.export_titles('titles.txt')
parser.export_descriptions('descriptions.txt')
