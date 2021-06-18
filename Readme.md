# ML_2021 Object Detection
## 競賽說明
現今生活的周遭處處可見各式各樣的招牌、路牌、看板、標語與廣告等，隨時隨地傳遞豐富的文字訊息給大街小巷中的人們。當在街上拍攝照片或錄影時，畫面中所包含的文字內容提供了該場景相當可靠的資訊。若能自動地將場景畫面中的文字辨識出來，對於包括場景理解、智慧城市/交通發展、機器人技術、自動駕駛、協助視障者或外來旅者等應用都能有所幫助。場景文字辨識實為人工智慧與電腦視覺的綜合議題，具有相當的挑戰。我們希望透過本次競賽，促進國內於場景文字辨識相關領域的技術發展，增進台灣人工智慧技術的實力。

場景文字檢測通常為場景文字辨識的前置步驟，即由畫面的像素中判斷文字出現的位置，以利後續針對該位置辨識可能的文字內容。場景文字檢測直接影響了文字辨識的準確度，本次賽事目標即為定位畫面中肉眼可識的文字位置。場景文字檢測受到許多因素所影響，包括場景中可能出現的多型態文字、多國文字、傾斜招牌文字、不同尺寸文字、外物遮蔽、類文字圖案紋理干擾、光線與陰影等。本賽事的目標場景為台灣市區街景，期望參賽者利用機器學習/深度學習技術，嘗試與開發適當的模型，以確偵測台灣街景畫面中的文字區域。

![](https://i.imgur.com/wEvuhYW.png)
## 成果
### 準確率:0.6544

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
## 資料放置
![](https://i.imgur.com/gz5TuEr.png)
## Training skills
[link](https://github.com/ultralytics/yolov5/wiki/Tips-for-Best-Training-Results)
1. [Hyperparameter Evolution](https://github.com/ultralytics/yolov5/issues/607)
2. Epochs. Start with 300 epochs.If overfitting does not occur after 300 epochs, train longer, i.e. 600, 1200 etc epochs.
3. `--multi-scale` when images are diff sizes
4. Batch size. Use the largest `--batch-size` that your hardware allows for.
5. [`--label-smoothing`](https://blog.csdn.net/qq_43211132/article/details/100510113)
6. `--quad` 會將一batch從 16x3x640x640 重塑為 4x3x1280x1280，重新排列batch中的馬賽克，it allows for 2x upscaling of some images within the batch (one of the 4 mosaics in each quad is upscaled by 2x, the other 3 mosaics are deleted)，當預測的img-sizes 大於 640，而正常模型在--img 640 上訓練時圖像尺寸大於 640 時性能較差。您可以將 --img 640 --quad 視為以 --img 640 的速度進行訓練的折衷方案，比起在 --img 1280 上訓練時看到的更高的 mAP

## Train
cd yolov5

python  train.py --img 1365 --rect  --batch 4 --epochs 300 --data ../datasets/annotations/setting.yaml --weights ../yolov5x6.pt --device 1 

## Test
python write_ans.py --source data/images  --weights runs/train/exp6/weights/best.pt runs/train/exp16/weights/best.pt  --conf 0.56 --save-txt --save-conf --img-size 1365

## Final Result
yolov5/answer.csv

上傳格式說明:

    參賽者僅需上傳一個 .csv 檔案，且須按照以下格式上傳，方可提交成功。
提交檔案格式範例如下:

![](https://i.imgur.com/Jtv3pjD.png)
![](https://i.imgur.com/OxjXmDe.png)

其中，每列皆代表一個預測框， (圖二)中的空白只是為了方便說明，參賽者不需另外添加空白(請參考提交template)。詳細說明如下:

FrameNumber: 為預測框所屬的圖片編號，資料型別為整數。
例如，第一列中的預測框 [ [632,1273], [702,1268], [703,1300], [632,1304] ] 為img_1.jpg的其中一個預測框，則frameNumber為1，以此類推。

Coordinates: 為該預測框的四個點座標，資料型別為整數。排列規則同json格式說明裡的方式。由左至右分別為，以標註框左上方為起點，順時針方向走訪至標註框左下方的點座標。即填入圖中 x0,y0,x1,y1,x2,y2,x3,y3 
![](https://i.imgur.com/Uyg3ggq.png)

Confidence: 為模型對該預測框的信心值，資料型別為浮點數。此信心值不會影響分數，但仍需要填寫。若參賽者所使用的方法沒有輸出信心值，可設為1.0。


## Testing skills
1. augmented inference 
2. [Model Ensembling](https://github.com/ultralytics/yolov5/issues/318)
3. [Model Puning](https://github.com/ultralytics/yolov5/issues/304) 


## 問題檢討及改進
1. batch size 只能設2，太大則CUDA OUT OF MEMORY，但預期  batch size 越大越好
2. 物件抓取到許多過度微小的細節，應統計分析哪些是容易抓錯的物件進行訓練資料的改進
3. 期望使用Hyperparameter Evolution找出最佳參數
4. `label-smoothing` and `--quad` 期望被使用
5. 訓練資料增加
