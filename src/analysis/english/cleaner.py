from nltk import pos_tag
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import RegexpTokenizer

class TextCleaner:
    def tokenize(self, sentence):
        tokenizer = RegexpTokenizer(r'\w+')
        return tokenizer.tokenize(sentence)

    def remove_stopwords(self, words):
        stop_words = set(stopwords.words('english'))
        return [w for w in words if not w.lower() in stop_words]

    def stem(self, words):
        stemmer = PorterStemmer()
        return [stemmer.stem(word.lower()) for word in words]

    def lemmatize(self, tags):
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word, self.get_wordnet_pos(pos)) for word, pos in tags]

    def clean(self, sentence):
        words = self.tokenize(sentence)
        tags = pos_tag(words)
        lemmatized_words = self.lemmatize(tags)
        filtered_words = self.remove_stopwords(lemmatized_words)
        stemmed_words = self.stem(filtered_words)
        return stemmed_words

    def get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN
