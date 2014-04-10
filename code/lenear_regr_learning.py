from sklearn import linear_model
import numpy as np
import math


def read_features(features_filename):
    print('Read features')
    features_file = open(features_filename)
    features_dict = {}

    features_num = 0
    for l in features_file:
        if not (features_num % 10000):
            print(features_num)
        line = l.strip()
        if line:
            features = line.split()
            features_dict[int(features[0])] = [float(f) for f in features[1:]]
            features_num += 1
    features_file.close()

    return features_dict


def read_likes(likes_filename):
    likes_file = open(likes_filename)
    likes = {}
    print('Read likes')
    likes_file.readline()
    for l in likes_file:
        line = l.strip()
        if line:
            symbols = line.split(',')
            likes[int(symbols[0])] = int(symbols[1])
    likes_file.close()
    return likes


def read_data(features_filename, likes_filename):
    all_likes = read_likes(likes_filename)

    features = read_features(features_filename)
    likes = [all_likes[post_id] for post_id in features if post_id in all_likes]

    return features, likes


def join_text_freq_features(text_features, freq_words_features):
    print('Join text and frequent words features')
    join_features_dict = {post_id: text_features[post_id] + freq_words_features[post_id] for post_id in text_features if
                          post_id in freq_words_features}
    return join_features_dict


def add_artificial_param(data_list):
    new_data_list = []
    for data in data_list:
        new_data_list.append([1] + data)
    return new_data_list


def add_poly_param(data_list, poly_degree):
    new_data_list = []
    for data in data_list:
        new_data_list.append([x ** deg for x in data for deg in range(1, poly_degree + 1)])
    return new_data_list


def normalize_data(data_list):
    new_data_list = []
    num = 0
    for data in data_list:
        print(data)
        num += 1
        new_data = data_list[data]
        new_data[11] = math.log(new_data[11])
        new_data_list.append(new_data)
    return new_data_list


def write_prediction(predict_data, post_ids, prediction_filename):
    prediction_file = open(prediction_filename, 'w')
    prediction_file.write('%s,%s\n' % ('\"post_id\"', "\"likes\""))
    for j in range(len(predict_data)):
        prediction_val = predict_data[j]
        if prediction_val < 0:
            prediction_val = 0
        prediction_file.write('%s,%s\n' % (post_ids[j], prediction_val))
    prediction_file.close()


def error_and_score(true_likes_filename, predict_likes_filename):
    true_likes_file = open(true_likes_filename)
    predict_likes_file = open(predict_likes_filename)
    true_likes = {}
    predict_likes = {}
    true_likes_file.readline()
    predict_likes_file.readline()

    line_true = true_likes_file.readline()
    line_predict = predict_likes_file.readline()
    while line_true and line_predict:
        true_arr = line_true.strip().split(',')
        true_likes[int(true_arr[0])] = float(true_arr[1])

        predict_arr = line_predict.strip().split(',')
        predict_likes[int(predict_arr[0])] = float(predict_arr[1])

        line_true = true_likes_file.readline()
        line_predict = predict_likes_file.readline()
    true_likes_file.close()
    predict_likes_file.close()

    diff = [true_likes[post_id] - predict_likes[post_id] for post_id in true_likes if post_id in predict_likes]
    sq_diff = [(true_likes[post_id] - predict_likes[post_id]) ** 2 for post_id in true_likes if
               post_id in predict_likes]

    err = float(sum(sq_diff)) / len(sq_diff)
    r_sq = (1 - np.std(diff) / np.std(true_likes.values())) * 1000
    return err, r_sq


train_text_features_filename = '../data/features/train_features_val_text.txt'
train_freq_words_features_filename = '../data/features/train_features_val_freq_words.txt'

train_likes_filename = '../data/train_likes_count_val.txt'

test_text_features_filename = '../data/features/val_features_text.txt'
test_freq_words_features_filename = '../data/features/val_features_freq_words.txt'

val_likes_filename = '../data/val_likes_count.txt'

predict_in_filename = '../data/result/predict_likes_count_in.txt'
predict_out_filename = '../data/result/predict_likes_count_out.txt'

train_text_features_dict, train_likes = read_data(train_text_features_filename, train_likes_filename)
train_freq_words_features_dict = read_features(train_freq_words_features_filename)
test_text_features_dict = read_features(test_text_features_filename)
test_freq_words_features_dict = read_features(test_freq_words_features_filename)

train_features_dict = join_text_freq_features(train_text_features_dict, train_freq_words_features_dict)
test_features_dict = join_text_freq_features(test_text_features_dict, test_freq_words_features_dict)

# X_train = add_artificial_param(train_features_dict.values())
# X_test = add_artificial_param(test_features_dict.values())

X_train = add_artificial_param(normalize_data(train_text_features_dict))
X_test = add_artificial_param(normalize_data(test_text_features_dict.values()))
#
# X_train = add_artificial_param(add_poly_param(train_features_dict.values(), 3))
# X_test = add_artificial_param(add_poly_param(test_features_dict.values(), 3))

# y_train = train_likes
#
# print('Start learning')
# learn_alg = linear_model.LinearRegression()
# learn_alg.fit(X_train, y_train)
#
# print('Start predictions')
# prediction_in = learn_alg.predict(X_train)
# write_prediction(prediction_in, train_features_dict.keys(), predict_in_filename)
# prediction_out = learn_alg.predict(X_test)
# write_prediction(prediction_out, test_features_dict.keys(), predict_out_filename)
#
# print('Error in: %s, Score in: %s' % error_and_score(train_likes_filename, predict_in_filename))
# print('Error val: %s, Score val: %s' % error_and_score(val_likes_filename, predict_out_filename))
