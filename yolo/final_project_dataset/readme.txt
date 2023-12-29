每個資料夾盡可能附上原資料相關說明，但所使用資料並非原資料全部內容(有進行刪減)
yaml檔類別設定請參照car_person_bike_motor中的data.yaml
還沒寫train_list.txt和test_list.txt，但不確定是否需要

- motor(只有機車的框)
train:valid:test = 464:33:33
https://universe.roboflow.com/ilyass/motor-detection/dataset/1

- bike(只有腳踏車的框，有概率框到機車)
train:valid:test = 1337:359:180
https://universe.roboflow.com/fiap-dsvre/detectionbike/dataset/1

- car_person_bike_motor(多為人和車的框但圖比較複雜，少量腳踏車和摩托車為另外手動標註)
train:valid:test = 1571:448:224
https://www.kaggle.com/datasets/owaiskhan9654/car-person-v2-roboflow

- car (只有車的框，為原本小組提供的資料，只有分train/test，test無label)
train:test = 1001:175
https://www.kaggle.com/datasets/sshikamaru/car-object-detection
