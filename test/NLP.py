import re
from konlpy.tag import Okt
from collections import Counter
from konlpy.tag import Okt
from konlpy.tag import Twitter
from tqdm import tqdm

# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize

# ref: https://wikdocs.net/22650
# ref: https://mr-doosun.tistory.com/24
# ref: https://dacon.io/codeshare/1808
# ref: https://haystar.tistory.com/11 (*)


okt = Okt()


# text -> BOW -> preprocessing -> <keyword, cnt> 변환

def build_bag_of_words(document):
    # 온점 제거 및 형태소 분석
    document = document.replace('.', '')
    tokenized_document = okt.morphs(document, stem=True)
    # stopwords = ['을', '를', '이', '가', '은', '는']
    # tokenized_document = [t for t in pre_tokenized_document if t not in stopwords]

    word_to_index = {}
    bow = []

    for word in tokenized_document:
        if word not in word_to_index.keys():
            word_to_index[word] = len(word_to_index)
            # BoW에 전부 기본값 1을 넣는다.
            bow.insert(len(word_to_index) - 1, 1)
        else:
            # 재등장하는 단어의 인덱스
            index = word_to_index.get(word)
            # 재등장한 단어는 해당하는 인덱스의 위치에 1을 더한다.
            bow[index] = bow[index] + 1

    return word_to_index, bow


# 한글 표현만 남기기
def extract_word(text):
    hangul = re.compile('[^가-힣]')
    result = hangul.sub(' ', text)
    return result


# 형태소 분석
def extract_morphs(text):
    document = text.replace('.', '')
    tokenized_document = okt.morphs(document, stem=True)
    return tokenized_document


# 한 글자, 불용어 제거
def clean_stopwords(words):
    remove_one_word = [x for x in words if len(x) > 1]

    with open('./stopwords.txt', 'r') as f:
        list_file = f.readlines()
    stopwords = list_file[0].split(",")
    remove_stopwords = [x for x in remove_one_word if x not in stopwords]

    return remove_stopwords


# 최소 횟수 이하 단어 제거
def remove_least_freq_word(words):
    min_cnt = 1
    filtered_words = []
    for i in tqdm(range(len(words))):
        tmp = words[i]
        if words.count(tmp) >= min_cnt:
            filtered_words.append(tmp)

    return filtered_words

# {key: count} 형식으로 변경
def make_word_count_dic(words):
    word_count = {}

    for word in words:
        if word not in word_count.keys():
            word_count[word] = 1
        else:
            word_count[word] = word_count[word] + 1

    return word_count


if __name__ == "__main__":
    exampleTextList = ["몇해전 신축하여 외관도 전통한옥 가미하여 지어짐.", "잘 가꾸어진 공원이에요 걷기좋아요"]

    txt = extract_word(exampleTextList[0])
    words = extract_morphs(txt)
    clean_words = clean_stopwords(words)
    filtered_words = remove_least_freq_word(clean_words)
    word_dic = make_word_count_dic(filtered_words)

    print(word_dic)
