# ML_2021 Object Detection

## How To Run
1. Download Dataset TrainDataset_0506.zip the unzip it
2. Run yologtfile.py [writing the yolov5 ground truth]
3. Run splitdata.py  [spliting train/valid in diff folder]
4. Add file named "setting.yaml" in datasets/annotations/ and revise it based on your folder
5. unzip PublicTestDataset.zip and put the images/ to yolov5/data/
6. download yolov5x6.pt from yolov5 official website
## Training skills
[link](https://github.com/ultralytics/yolov5/wiki/Tips-for-Best-Training-Results)
1. [Hyperparameter Evolution](https://github.com/ultralytics/yolov5/issues/607)
2. Epochs. Start with 300 epochs.If overfitting does not occur after 300 epochs, train longer, i.e. 600, 1200 etc epochs.
3. Image size `--img` 1280 is better
4. Batch size. Use the largest `--batch-size` that your hardware allows for.

## Train
cd yolov5
python  train.py --img 1280  --batch 4 --epochs 200 --data ../datasets/annotations/setting.yaml --weights ../yolov5x6.pt 


nohup  python  train.py --img 1365 --rect  --batch 4 --epochs 200 --data ../datasets/annotations/setting.yaml --weights ../yolov5x6.pt --device 1 &> output1.txt &

## Test
python write_ans.py --source data/images --weights runs/train/exp16/weights/best.pt --conf 0.6 --save-txt --save-conf --img-size 1365

## Final Result
yolov5/answer.csv

## Testing skills
1. augmented inference 
2. [Model Ensembling](https://github.com/ultralytics/yolov5/issues/318)
3. [Model Puning](https://github.com/ultralytics/yolov5/issues/304) 
---
4. --update 
5. new model -> 0.65 && other < 0.9  && ensembling
## others
iou_thres -> did not get better
model: exp 6,8,16
exp6 : conf > 0.6 && img_size1280 && w/o not care<0.9 other<0.7
exp16 : conf > 0.6 && img_size1365 && w/o not care<0.9 other<0.8
## Hand
8 12 16 77 79 100 114 118 120 123 133 156 204 987
997
