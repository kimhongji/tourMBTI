import json
import re
from konlpy.tag import Okt
from tqdm import tqdm

# ref: https://wikdocs.net/22650
# ref: https://mr-doosun.tistory.com/24
# ref: https://dacon.io/codeshare/1808
# ref: https://haystar.tistory.com/11 (*)


class NLP:
    def __init__(self):
        self.okt = Okt()

    def run(self, texts):
        txt = self.extract_word(texts)
        words = self.extract_morphs(txt)
        clean_words = self.clean_stopwords(words)
        filtered_words = self.remove_least_freq_word(clean_words)
        word_dic = self.make_word_count_dic(filtered_words)

        return word_dic

    # 한글 표현만 남기기
    def extract_word(self, texts):
        doc = ""
        for text in texts:
            doc = doc + "" + text

        hangul = re.compile('[^가-힣]')
        result = hangul.sub(' ', doc)
        return result

    # 형태소 분석
    def extract_morphs(self, text):
        document = text.replace('.', '')
        tokenized_document = self.okt.morphs(document, stem=True)
        return tokenized_document

    # 한 글자, 불용어 제거
    def clean_stopwords(self, words):
        remove_one_word = [x for x in words if len(x) > 1]

        with open('./stopwords.txt', 'r') as f:
            list_file = f.readlines()
            list_file = list(map(lambda s: s.strip(), list_file))

        remove_stopwords = [x for x in remove_one_word if x not in list_file]

        return remove_stopwords

    # 최소 횟수 이하 단어 제거
    def remove_least_freq_word(self, clean_words):
        min_cnt = 1
        filtered_words = []
        for i in tqdm(range(len(clean_words))):
            tmp = clean_words[i]
            if clean_words.count(tmp) >= min_cnt:
                filtered_words.append(tmp)

        return filtered_words

    # {key: count} 형식으로 변경
    def make_word_count_dic(self, words):
        word_count = {}

        for word in words:
            if word not in word_count.keys():
                word_count[word] = 1
            else:
                word_count[word] = word_count[word] + 1

        return word_count


if __name__ == "__main__":
    exampleTexts = ["몇해전 신축하여 외관도 전통한옥 가미하여 지어짐.", "잘 가꾸어진 공원이에요 걷기좋아요", "공기도 좋고 이뻐요"]

    # key: 관광지, value: 키워드 list (빈도수 포함) {키워드, num}
    # { "경복궁" : [{"좋다", 1} , "한적하다", "넓다"... ] }
    nlp = NLP()
    keywords = nlp.run(exampleTexts)

    print(keywords)

    keyword_json = json.dumps(keywords, ensure_ascii=False)

    print(keyword_json)
