# ML_2021 Object Detection

## How To Run
1. Download Dataset TrainDataset_0506.zip the unzip it
2. Run yologtfile.py [writing the yolov5 ground truth]
3. Run splitdata.py  [spliting train/valid in diff folder]
4. Add file named "setting.yaml" in datasets/annotations/ and revise it based on your folder
5. unzip PublicTestDataset.zip and put the images/ to yolov5/data/
## Train
cd yolov5
python train.py --img 1280 --batch 4 --epochs 2 --data ../datasets/annotations/setting.yaml --weights ../yolov5x6.pt
## Test
python write_ans.py --source data/images --weights runs/train/exp6/weights/best.pt --conf 0.25
## Final Result
yolov5/answer.csv
