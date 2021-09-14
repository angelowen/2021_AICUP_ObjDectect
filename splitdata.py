import os
import numpy as np
import shutil

# Create folder
if not os.path.exists('./datasets'):
    os.makedirs("./datasets")
    os.makedirs("./datasets/annotations")
    os.makedirs("./datasets/images")
    os.makedirs("./datasets/labels")

# Creating Train / Val / Test folders 
root_dir = './datasets/images'
labels_dir = './datasets/labels'
if not os.path.exists(root_dir +'/train'):
    os.makedirs(root_dir +'/train')
    os.makedirs(root_dir +'/val' )
    os.makedirs(labels_dir +'/train')
    os.makedirs(labels_dir +'/val' )

img_src = "./TrainDataset/img" # Folder to copy images from
yologt = "./yologt"

allFileNames = os.listdir(img_src)
np.random.shuffle(allFileNames)
data = np.array(allFileNames)
train_num = int(len(allFileNames)*0.8)
train_FileNames, val_FileNames = data[:train_num], data[train_num:]
# print(train_FileNames, val_FileNames )

## write annotation
with open('./datasets/annotations/train.txt', 'w') as fw:
    for name in train_FileNames:
        fw.write('../datasets/images/train/'+name+'\n')
with open('./datasets/annotations/val.txt', 'w') as fw:
    for name in val_FileNames:
        fw.write('../datasets/images/val/'+name+'\n')

train_labels = [yologt+'/'+ name.split('.')[0]+".txt" for name in train_FileNames.tolist()]
val_labels = [yologt+'/' + name.split('.')[0]+".txt" for name in val_FileNames.tolist()]
train_FileNames = [img_src+'/'+ name for name in train_FileNames.tolist()]
val_FileNames = [img_src+'/' + name for name in val_FileNames.tolist()]


print('Total images: ', len(allFileNames))
print('Training: ', len(train_FileNames))
print('Validation: ', len(val_FileNames))

# Copy-pasting labels , images
for name in train_labels:
    shutil.copy(name, labels_dir +'/train')
for name in val_labels:
    shutil.copy(name, labels_dir +'/val')

for name in train_FileNames:
    shutil.copy(name, root_dir +'/train')
for name in val_FileNames:
    shutil.copy(name, root_dir +'/val')
