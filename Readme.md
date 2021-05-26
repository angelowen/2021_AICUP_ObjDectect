# ML_2021 Object Detection
## 競賽說明
![](https://i.imgur.com/wEvuhYW.png)
現今生活的周遭處處可見各式各樣的招牌、路牌、看板、標語與廣告等，隨時隨地傳遞豐富的文字訊息給大街小巷中的人們。當在街上拍攝照片或錄影時，畫面中所包含的文字內容提供了該場景相當可靠的資訊。若能自動地將場景畫面中的文字辨識出來，對於包括場景理解、智慧城市/交通發展、機器人技術、自動駕駛、協助視障者或外來旅者等應用都能有所幫助。場景文字辨識實為人工智慧與電腦視覺的綜合議題，具有相當的挑戰。我們希望透過本次競賽，促進國內於場景文字辨識相關領域的技術發展，增進台灣人工智慧技術的實力。

場景文字檢測通常為場景文字辨識的前置步驟，即由畫面的像素中判斷文字出現的位置，以利後續針對該位置辨識可能的文字內容。場景文字檢測直接影響了文字辨識的準確度，本次賽事目標即為定位畫面中肉眼可識的文字位置。場景文字檢測受到許多因素所影響，包括場景中可能出現的多型態文字、多國文字、傾斜招牌文字、不同尺寸文字、外物遮蔽、類文字圖案紋理干擾、光線與陰影等。本賽事的目標場景為台灣市區街景，期望參賽者利用機器學習/深度學習技術，嘗試與開發適當的模型，以確偵測台灣街景畫面中的文字區域。
## 成果
![](https://i.imgur.com/mhMs7G1.png)
![](https://i.imgur.com/byMjpKg.png)
![](https://i.imgur.com/mDxUTOT.png)
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
python write_ans.py --source data/images --weights runs/train/exp16/weights/best.pt --conf 0.58 --save-txt --save-conf --img-size 1365

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
if area too small give up
## Hand
8 12 16 77 79 100 114 118 120 123 133 156 204 987 349 492
997
