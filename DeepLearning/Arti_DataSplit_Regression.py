import glob
import os
import shutil
import random

data_path = "D:\\Datasets\\Regression_Artibot\\Non-bias"


train_dest = "D:\\Datasets\\Regression_Artibot\\train"  # Destination to train set(folder)
val_dest = "D:\\Datasets\\Regression_Artibot\\val"  # Destination to validation set(folder)
# test_dest = "D:\\Datasets\\arti_sim\\3_class\\test"       # Destination to test set(folder)




data = []  # List with every image
img_counter = 0
all_data = 0
nb_train = 0
nb_val = 0
nb_test = 0
train_total = 0
val_total = 0



for name in glob.glob1(data_path, '*.jpg'):
    img_path = os.path.join(data_path, name)
    data.append(img_path)
    img_counter += 1

nb_train = round(0.6 * img_counter)
# nb_val = round(0.3 * img_counter)
# print("nb_train: ", nb_train)
# print("nb_val: ", nb_val)

for i in range(nb_train):
    target_file = random.choice(data)
    # print("target_file: ", target_file)
    destination = train_dest
    # print("destination", destination)
    shutil.move(target_file, destination)
    data.remove(target_file)

for i in range(len(data)):
    target_file = random.choice(data)
    destination = val_dest
    val_total += 1
    shutil.move(target_file, destination)
    data.remove(target_file)

# print("nb_test: ", len(data))
# for i in range(len(data)):
#     target_file = random.choice(data)
#     destination = os.path.join(test_dest, label)
#     shutil.move(target_file, destination)
#     data.remove(target_file)

train_total += nb_train
val_total += nb_val
all_data += img_counter
img_counter = 0
data = []

print("Images in training-set: ", train_total)
print("Images in validation-set: ", val_total)
print("Total Images in data-set: ", all_data)