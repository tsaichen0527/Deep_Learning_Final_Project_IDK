# Deep_Learning_Final_Project_IDK
訓練或進行照片影片偵測要先載好yolov7以及執行環境
```
git clone https://github.com/WongKinYiu/yolov7.git
cd yolov7
pip install --upgrade pip
pip install -r requirements.txt
```
## 訓練
訓練前
1. 將dataset導入進data/images以及data/labels裡面
2. 將train_yaml裡的coco_self.yaml放進yolov7\data，yolov7_self.yaml放進yolov7\cfg\training
然後在cmd裡下指令
weight可以換成要接續訓練的weight位置，yolov7_training.pt是官方遇訓練好的
訓練完成後的結果會被除在yolov7/runs/train裡面
```
cd yolov7
python train.py --weights ../weights/yolov7_training.pt --cfg cfg/training/yolov7_self.yaml --data data/coco_self.yaml  --device 0 --batch-size 10 --epoch 2 --name yolov7-trafic
```

## 偵測
weight可以換成前面訓練出來最好的結果，目前Deep_Learning_Final_Project_IDK\weights\yolov7-trafic\best.pt是可以測試用的
偵測完成後的結果會被除在yolov7/runs/detect裡面
```
cd yolov7
python detect.py --weights ../weights/yolov7-trafic200/weights/best.pt --source ../test_video/videoplayback.mp4 --save-txt --save-conf
```