import re

REMOVE_CHARS = ''.join(['.', ',', '!', '?', ';', ':', '-', '*', '(', ')', '[', ']', '{', '}', '\\', '/', '@', '#',
                        '$', '%', '^', '+', '=', '`', '~', '"', '\'', '|'])
NUMBER_FREQ_WORDS = 100
RARE_WORDS_NUMBER = 10

RE_IM = re.compile('Images\\[[0-9]+')
RE_POOL = re.compile('Pool\\[.*')
RE_WEB_ADDRESS = [re.compile('.*http://.+'), re.compile('.*https://.+'), re.compile('.*www\\..+'),
                  re.compile('.+\\.com.*'), re.compile('.+\\.ru.*'), re.compile('.+\\.ua.*'),
                  re.compile('.+\\.org.*'), re.compile('.+\\.net.*')]
RE_SMILE = re.compile('\)')
RE_SAD = re.compile('\(')
RE_MARKS = re.compile('[!?]')


def is_named_entity(text_word, was_end_sentence):
    text_word = text_word.translate(None, REMOVE_CHARS)
    is_all_letters_upper = all([letter.isupper() for letter in unicode(text_word, 'utf8')])
    if not is_all_letters_upper and unicode(text_word, 'utf8')[0].isupper() and not was_end_sentence:
        return True
    return False


def make_words_number_dict(data_filename):
    data_file = open(data_filename)
    words_number_dict = {}
    post_num = 1
    print('Preparing words number dictionary')
    for post in data_file:
        if not (post_num % 10000):
            print(post_num)
        post_num += 1
        if post:
            post_data = post.strip().split('\t')
            if len(post_data) == 4:
                words = post_data[3].split()

                is_end_sentence = True
                was_images = False
                was_pool = False

                for word in words:
                    if word:
                        was_end_sentence = is_end_sentence
                        if word.endswith('.') or word.endswith('!') or word.endswith('?'):
                            is_end_sentence = True
                        else:
                            is_end_sentence = False

                        num_match_images = len(RE_IM.findall(word))
                        if num_match_images != 0:
                            if not word.endswith(']'):
                                was_images = True
                            continue

                        if was_images:
                            end_im = len(re.compile('[0-9]+\]').findall(word))
                            if end_im != 0:
                                was_images = False
                            continue

                        num_pool = len(RE_POOL.findall(word))
                        if num_pool != 0:
                            if not word.endswith(']'):
                                was_pool = True
                            continue

                        if was_pool:
                            if word == ']':
                                was_pool = False
                            continue

                        is_web_adr = False
                        for p_web_adr in RE_WEB_ADDRESS:
                            num_web_adr = len(p_web_adr.findall(word))
                            if num_web_adr != 0:
                                is_web_adr = True
                                break
                        if is_web_adr:
                            continue

                        if is_named_entity(word, was_end_sentence):
                            continue

                        if word.isdigit():
                            continue

                        word = unicode(word.translate(None, REMOVE_CHARS), 'utf8').lower()
                        if word:
                            if word in words_number_dict:
                                words_number_dict[word] += 1
                            else:
                                words_number_dict[word] = 1

    data_file.close()
    write_dict(words_number_dict, '../data/words_number_dict.txt')


def get_text_features(text, words_number_dict):
    features_vector = [0 for i in range(13)]
    words = text.split()

    is_end_sentence = True
    was_images = False
    was_pool = False

    number_smile = 0
    number_sad = 0

    for word in words:
        if word:
            was_end_sentence = is_end_sentence
            if word.endswith('.') or word.endswith('!') or word.endswith('?'):
                is_end_sentence = True
            else:
                is_end_sentence = False

            features_vector[9] += len(word)

            features_vector[10] += 1

            number_smile += len(RE_SMILE.findall(word))
            number_sad += len(RE_SAD.findall(word))

            features_vector[8] += len(RE_MARKS.findall(word))

            num_match_images = len(RE_IM.findall(word))
            if num_match_images != 0:
                features_vector[0] += num_match_images
                features_vector[1] += num_match_images
                if not word.endswith(']'):
                    was_images = True
                continue

            if was_images:
                num_im = len(re.compile('[0-9]+').findall(word))
                end_im = len(re.compile('[0-9]+\]').findall(word))
                features_vector[1] += num_im
                if end_im != 0:
                    was_images = False
                continue

            num_pool = len(RE_POOL.findall(word))
            if num_pool != 0:
                features_vector[2] += num_pool
                if not word.endswith(']'):
                    was_pool = True
                continue

            if was_pool:
                num_pool_answer = len(re.compile('PoolAnswer\\[*.').findall(word))
                features_vector[3] += num_pool_answer
                if word == ']':
                    was_pool = False
                continue

            is_web_adr = False
            num_web_adr = 0
            for p_web_adr in RE_WEB_ADDRESS:
                num_web_adr = len(p_web_adr.findall(word))
                if num_web_adr != 0:
                    is_web_adr = True
                    break
            if is_web_adr:
                features_vector[4] += num_web_adr
                continue

            if is_named_entity(word, was_end_sentence):
                features_vector[5] += 1
                continue

            if word.isdigit():
                features_vector[6] += 1
                continue

            word = unicode(word.translate(None, REMOVE_CHARS), 'utf8').lower()
            if word not in words_number_dict or words_number_dict[word] <= RARE_WORDS_NUMBER:
                features_vector[12] += 1

    features_vector[7] += abs(number_smile - number_sad)

    if features_vector[10] != 0:
        features_vector[11] = float(features_vector[9]) / features_vector[10]

    return features_vector


def get_freq_words_features(text, most_freq_words):
    features_vector = [0 for i in range(len(most_freq_words))]
    words = text.split()
    for word in words:
        word = unicode(word.translate(None, REMOVE_CHARS), 'utf8').lower()
        if word in most_freq_words:
            features_vector[most_freq_words.index(word)] += 1
    return features_vector


def text_features_detector(data_filename, words_dict_filename):
    words_dict = read_dict(words_dict_filename)
    words_number_dict = {unicode(key, 'utf8'): words_dict[key] for key in words_dict}

    data_file = open(data_filename)
    features_dic = {}
    print('Extracting text features')
    post_num = 1
    for post in data_file:
        if not (post_num % 10000):
            print(post_num)
        if post:
            post_data = post.strip().split('\t')
            if len(post_data) == 4:
                post_text = post_data[3]
                features_dic[int(post_data[1])] = get_text_features(post_text, words_number_dict)
        post_num += 1
    data_file.close()
    return features_dic


def freq_words_features_detector(data_filename, words_dict_filename):
    words_dict = read_dict(words_dict_filename)
    words_number_dict = {unicode(key, 'utf8'): words_dict[key] for key in words_dict}

    freq_words = sorted(words_number_dict, key=words_number_dict.get, reverse=True)[:NUMBER_FREQ_WORDS]

    data_file = open(data_filename)
    features_dic = {}
    print('Extracting frequent words features')
    post_num = 1
    for post in data_file:
        if not (post_num % 10000):
            print(post_num)
        if post:
            post_data = post.strip().split('\t')
            if len(post_data) == 4:
                post_text = post_data[3]
                features_dic[int(post_data[1])] = get_freq_words_features(post_text, freq_words)
        post_num += 1
    data_file.close()
    return features_dic


def write_dict(dict_write, filename):
    dict_file = open(filename, 'w')
    for key in dict_write.keys():
        dict_file.write('%s %s\n' % (key.encode('utf8'), str(dict_write[key])))
    dict_file.close()


def read_dict(dict_filename):
    print('Read dict')
    dict_file = open(dict_filename)
    new_dict = {}
    for l in dict_file:
        line = l.strip()
        if line:
            words = line.split()
            new_dict[words[0]] = int(words[1])
    return new_dict


def write_features(dic_features, features_filename):
    features_file = open(features_filename, 'w')
    print('Write features')
    for post_id in dic_features:
        features_file.write('%s\n' % ' '.join([str(post_id)] + [str(f) for f in dic_features[post_id]]))
    features_file.close()


words_number_dict_filename = '../data/words_number_dict.txt'

train_data_filename = '../data/train_content.csv'
train_text_features_filename = '../data/features/train_features_text.txt'
train_freq_words_features_filename = '../data/features/train_features_freq_words.txt'

test_data_filename = '../data/test_content.csv'
test_text_features_filename = '../data/features/test_features_text.txt'
test_freq_words_features_filename = '../data/features/val_features_freq_words.txt'

make_words_number_dict(train_data_filename)

text_features_train = text_features_detector(train_data_filename, words_number_dict_filename)
write_features(text_features_train, train_text_features_filename)
# freq_words_features_train = freq_words_features_detector(train_data_filename, words_number_dict_filename)
# write_features(freq_words_features_train, train_freq_words_features_filename)

text_features_test = text_features_detector(test_data_filename, words_number_dict_filename)
write_features(text_features_test, test_text_features_filename)
# freq_words_features_test = freq_words_features_detector(test_data_filename, words_number_dict_filename)
# write_features(freq_words_features_test, test_freq_words_features_filename)
