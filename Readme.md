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
python train.py --img 1280 --batch 4 --epochs 200 --data ../datasets/annotations/setting.yaml --weights ../yolov5x6.pt
python train.py --epochs 10 --data ../datasets/annotations/setting.yaml  --weights ../yolov5x6.pt --cache --evolve
## Test
python write_ans.py --source data/images --weights runs/train/exp6/weights/best.pt --conf 0.49 --save-txt --save-conf

## Final Result
yolov5/answer.csv

## Testing skills
1. augmented inference -> did not get better result in this case
2. [Model Ensembling](https://github.com/ultralytics/yolov5/issues/318)
3. [Model Puning](https://github.com/ultralytics/yolov5/issues/304) 

## others
iou-thres

