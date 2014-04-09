import random
import os


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
    for i in train_rows_ind:
        train_data_file.write('%s' % data[i])
        train_likes_count_file.write('%s' % likes_count[i])
    train_data_file.close()
    train_likes_count_file.close()

    val_data_file = open(path + '/val_content.txt', 'w')
    val_likes_count_file = open(path + '/val_likes_count.txt', 'w')
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


def replace_minus_to_zero(data_filename, new_data_filename):
    data_file = open(data_filename)
    new_data_file = open(new_data_filename, 'w')
    data_file.readline()
    for l in data_file:
        if l:
            line = l.strip().split(',')
            new_val = float(line[1])
            if new_val < 0:
                new_val = 0
            new_data_file.write('%s %s\n' % (line[0], new_val))
    data_file.close()
    new_data_file.close()


train_content_filename = '../data/train_content_val.txt'
new_train_content_filename = '../data/train_content_val_10.txt'
train_likes_count_filename = '../data/train_likes_count.csv'

# break_data_train_val(train_content_filename, train_likes_count_filename, 100000)

make_small_data_set(train_content_filename, '../data/train_content_val_400.txt', 1, 400)

# print(get_data_number('../data/train_content_val.txt'), get_data_number('../data/train_likes_count_val.txt'))
# print(get_data_number('../data/val_content.txt'), get_data_number('../data/val_likes_count.txt'))

# replace_minus_to_zero('../data/result/test_likes_count.txt', '../data/result/new_test_likes_count.txt')

# make_small_rand_data('../data/train_content.csv', '../data/train_content_rand_20.txt', 30)