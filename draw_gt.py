import numpy as np
import cv2,os,json

base = 'TrainDataset/img/'
save_folder = 'TrainDataset/img_gt/'
json_folder = 'TrainDataset/json/'

if not os.path.exists(save_folder):
    os.mkdir(save_folder)

for i in range(1,4001):
    filename = f'img_{i}.jpg'
    img = cv2.imread(base+filename) 

    with open(json_folder +filename.split('.')[0]+'.json','r') as fr:
                data = json.load(fr)
                for item in data["shapes"]:
                    first = tuple(int(i) for i in item["points"][0])  
                    second = tuple(int(i) for i in item["points"][2])
                    cv2.rectangle(img, first,second, (0, 0, 255), 2)
    cv2.imwrite(save_folder +filename, img)
