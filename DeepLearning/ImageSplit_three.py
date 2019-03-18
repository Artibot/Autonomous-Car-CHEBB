import glob
import os
import shutil
import random

data_path = "D:\\Datasets\\arti_sim\\log_three"


train_dest = "D:\\Datasets\\arti_sim\\3_class\\train"  # Destination to train set(folder)
val_dest = "D:\\Datasets\\arti_sim\\3_class\\val"  # Destination to validation set(folder)
test_dest = "D:\\Datasets\\arti_sim\\3_class\\test"       # Destination to test set(folder)

classes = ("Hard_Left", "Hard_Right", "Straight")  # Classes


data = []  # List with every image
img_counter = 0
all_data = 0
nb_train = 0
nb_val = 0
nb_test = 0
train_total = 0
val_total = 0

for label in classes:
    data_path2 = os.path.join(data_path, label)

    for name in glob.glob1(data_path2, '*.jpg'):
        img_path = os.path.join(data_path2, name)
        data.append(img_path)
        img_counter += 1

    nb_train = round(0.6 * img_counter)
    nb_val = round(0.3 * img_counter)
    print("nb_train: ", nb_train)
    print("nb_val: ", nb_val)

    for i in range(nb_train):
        target_file = random.choice(data)
        destination = os.path.join(train_dest, label)
        shutil.move(target_file, destination)
        data.remove(target_file)

    for i in range(nb_val):
        target_file = random.choice(data)
        destination = os.path.join(val_dest, label)
        shutil.move(target_file, destination)
        data.remove(target_file)

    print("nb_test: ", len(data))
    for i in range(len(data)):
        target_file = random.choice(data)
        destination = os.path.join(test_dest, label)
        shutil.move(target_file, destination)
        data.remove(target_file)

    train_total += nb_train
    val_total += nb_val
    all_data += img_counter
    img_counter = 0
    data = []

print("Images in training-set: ", train_total)
print("Images in validation-set: ", val_total)









