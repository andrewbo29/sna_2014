import random
import os
import feature_detector


def make_small_data_set(data_filename, new_data_filename, data_number_start, data_number_end):
    data_file = open(data_filename)
    new_data_file = open(new_data_filename, 'w')
    row_num = 1
    while row_num < data_number_start:
        data_file.readline()
        row_num += 1
    line = data_file.readline()
    while data_number_start <= row_num <= data_number_end and line:
        new_data_file.write(line)
        row_num += 1
        line = data_file.readline()
    data_file.close()
    new_data_file.close()


def make_small_rand_data(data_filename, new_data_filename, new_data_size):
    data_size = get_data_number(data_filename)
    rows_ind = random.sample(range(data_size), data_size)
    new_rows_ind = rows_ind[:new_data_size]

    data_file = open(data_filename)
    row_num = 0
    data = ['' for i in range(data_size)]
    for line in data_file:
        data[row_num] = line
        row_num += 1
    data_file.close()

    new_data_file = open(new_data_filename, 'w')
    for i in new_rows_ind:
        new_data_file.write('%s' % data[i])
    new_data_file.close()


def break_data_train_val(data_filename, likes_count_filename, val_size):
    data_size = get_data_number(data_filename)
    rows_ind = random.sample(range(data_size), data_size)
    train_rows_ind = rows_ind[:(data_size - val_size)]
    val_rows_ind = rows_ind[(data_size - val_size):]

    data_file = open(data_filename)
    row_num = 0
    data = ['' for i in range(data_size)]
    for line in data_file:
        data[row_num] = line
        row_num += 1
    data_file.close()

    likes_count_file = open(likes_count_filename)
    row_num = 0
    likes_count = ['' for i in range(data_size)]
    likes_count_file.readline()
    for line in likes_count_file:
        likes_count[row_num] = line
        row_num += 1
    likes_count_file.close()

    path = os.path.dirname(data_filename)
    train_data_file = open(path + '/train_content_val.txt', 'w')
    train_likes_count_file = open(path + '/train_likes_count_val.txt', 'w')
    train_likes_count_file.write('%s,%s\n' % ('\"post_id\"', "\"likes\""))
    for i in train_rows_ind:
        train_data_file.write('%s' % data[i])
        train_likes_count_file.write('%s' % likes_count[i])
    train_data_file.close()
    train_likes_count_file.close()

    val_data_file = open(path + '/val_content.txt', 'w')
    val_likes_count_file = open(path + '/val_likes_count.txt', 'w')
    val_likes_count_file.write('%s,%s\n' % ('\"post_id\"', "\"likes\""))
    for j in val_rows_ind:
        val_data_file.write('%s' % data[j])
        val_likes_count_file.write('%s' % likes_count[j])
    val_data_file.close()
    val_likes_count_file.close()


def get_data_number(data_filename):
    data_file = open(data_filename)
    number_data = 0
    for line in data_file:
        number_data += 1
    return number_data


def find_strange_posts(data_filename, strange_posts_filename):
    data_file = open(data_filename)
    strange_posts_file = open(strange_posts_filename, 'w')
    post_num = 1
    for post in data_file:
        print(post_num)
        post_num += 1
        if post:
            post_data = post.strip().split('\t')
            if len(post_data) != 4:
                strange_posts_file.write(post)
                strange_posts_file.write('\n')
    data_file.close()
    strange_posts_file.close()


def get_posts(data_filename):
    data_file = open(data_filename)
    for post in data_file:
        if post:
            post_data = post.strip().split('\t')
            if len(post_data) == 4:
                print(post_data[1])
    data_file.close()


def get_post_data(data_filename, post_number):
    data_file = open(data_filename)
    path = os.path.dirname(data_filename)
    filename = '/post_%s.txt' % post_number
    post_file = open(path + filename, 'w')
    for post in data_file:
        words = post.strip().split('\t')
        if int(words[1]) == post_number:
            post_file.write(post)
            return


def write_post_id(data_filename, post_ids_filename):
    data_file = open(data_filename)
    post_ids = []
    for post in data_file:
        post_data = post.strip().split('\t')
        if len(post_data) == 4:
            post_ids.append(int(post_data[1]))
    data_file.close()

    post_ids_file = open(post_ids_filename, 'w')
    for post_id in post_ids:
        post_ids_file.write('%s\n' % post_id)
    post_ids_file.close()


def split_group_features_by_post_id(post_ids_filename, group_features_filename, new_group_features_filename):
    print('Split group features by post ids')
    print('Prepare post ids')
    post_ids_file = open(post_ids_filename)
    post_ids = []
    for l in post_ids_file:
        post_ids.append(l.strip())
    post_ids_file.close()

    print('Split group features')
    num_features = 1
    group_features_file = open(group_features_filename)
    group_features_dict = {}
    group_features_file.readline()
    for l in group_features_file:
        print(num_features)
        num_features += 1
        line = l.strip()
        if line:
            group_features = line.split(',')
            group_post_id = int(float(group_features[1]))
            if group_post_id in post_ids:
                group_features_dict[int(float(group_features[1]))] = [float(f) for f in group_features[2:]]
    group_features_file.close()

    feature_detector.write_features(group_features_dict, new_group_features_filename)


train_content_filename = '../data/train_content_val.txt'
train_post_ids_filename = '../data/train_post_ids.txt'
train_group_features_filename = '../data/features/group_features.csv'

test_content_filename = '../data/val_content.txt'
test_post_ids_filename = '../data/val_post_ids.txt'

# break_data_train_val(train_content_filename, train_likes_count_filename, 100000)

write_post_id(train_content_filename, train_post_ids_filename)
write_post_id(test_content_filename, test_post_ids_filename)

split_group_features_by_post_id(train_post_ids_filename, train_group_features_filename,
                                '../data/features/train_features_val_group.txt')
split_group_features_by_post_id(test_post_ids_filename, train_group_features_filename,
                                '../data/features/val_features_group.txt')
