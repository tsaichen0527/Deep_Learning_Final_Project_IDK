from math import inf
import numpy as np
from byte_tracker import BYTETracker, STrack
import os
import re

class Process:
    def __init__(self, folder, track_threshs, match_threshs, track_buffers):
        self.folder = folder
        self.track_threshs = track_threshs
        self.match_threshs = match_threshs
        self.track_buffers = track_buffers
        self.detections_arr = [[] for _ in range(5)]
        np.float=float
        self.fixed_confidences = 1
        self.track_start_frame_index = 2400    # 統一讀取 frame 長度
        self.track_end_frame_index = 11400    # 統一讀取 frame 長度

    def start(self):
        files = os.listdir(self.folder)
        files = sorted(files, key=lambda x: int(re.search(r'\d+', x).group()))
        index = 0
        for file in files:
            # 僅讀取部分片段的 frame
            if (index < self.track_start_frame_index):
                index += 1
                continue
            
            if (index > self.track_end_frame_index):
                break
            
            lines = self.read_file(os.path.join(self.folder, file))
            self.get_detections(lines)
            index += 1

        total_id_arr = []
        for i in range(5):
            tracks = self.get_tracks(self.detections_arr[i], track_thresh=self.track_threshs[i], match_thresh=self.match_threshs[i], track_buffer=self.track_buffers[i])
            total_id_arr += [self.get_total_id(tracks)]
        return total_id_arr

    # 取得物體的數量
    def get_total_id(self, tracks):
        min = inf
        max = 0
        for track in tracks:
            if (track.track_id < min):
                min = track.track_id
                
            if (track.track_id > max):
                max = track.track_id
                
        return  0 if (max - min + 1) < 0 else (max - min + 1)
        
    # 對每個 frame 抓出各物體的座標、confidence 資訊，整理到 detections
    def get_detections(self, lines):
        detection0 = []
        detection1 = []
        detection2 = []
        detection3 = []
        detection4 = []

        for line in lines:
            parts = line.strip().split()
            label = int(parts[0])
            
            # 若資料無 confidence，則給預設值
            if (len(parts) >= 6):
                confidences = parts[-1]
            else:
                confidences = self.fixed_confidences
            
            coord = [float(x) for x in parts[1:5]]
            l, t = float(coord[0]), float(coord[1])
            w, h = float(coord[2]), float(coord[3])
            
            tlbr = STrack.tlwh_to_tlbr([l, t, w, h])
            
            if label == 0:
                detection0.append(np.append(tlbr, confidences))
            elif label == 1:
                detection1.append(np.append(tlbr, confidences))
            elif label == 2:
                detection2.append(np.append(tlbr, confidences))
            elif label == 3:
                detection3.append(np.append(tlbr, confidences))
            elif label == 4:
                detection4.append(np.append(tlbr, confidences))

        self.detections_arr[0] += [detection0]
        self.detections_arr[1] += [detection1]
        self.detections_arr[2] += [detection2]
        self.detections_arr[3] += [detection3]
        self.detections_arr[4] += [detection4]

    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return lines

    # 讓 tracker 訓練
    def get_tracks(self, detections, track_thresh, match_thresh, track_buffer):
        class BYTETrackerArgs:
            def __init__(self, track_thresh, match_thresh, track_buffer):
                self.track_thresh = track_thresh
                self.match_thresh = match_thresh
                self.track_buffer = track_buffer
                self.aspect_ratio_thresh = 3.0
                self.min_box_area = 1.0
                self.mot20 = False

        byte_tracker_args = BYTETrackerArgs(track_thresh.get(), match_thresh.get(), track_buffer.get())
        byte_tracker = BYTETracker(byte_tracker_args, frame_rate=3)

        tracks = []
        index = 0
        for detection in detections:
            index += 1
            if (index % 10 != 0):
                continue
            
            np_arr_det = np.array(detection, dtype=float)

            # 若此 frame 沒有物體，放入 0 array
            if (np_arr_det.ndim == 1):
                np_arr_det = np.array([[1, 1, 1, 1, 0]])
                
            # To-do: 設定正確的 img_info, img_size
            track = byte_tracker.update(output_results=np.array(np_arr_det, dtype=float), img_info=(1920, 1080), img_size=(1920, 1080))
            tracks = tracks + track
            # for trac in track:
                # print('track: frame: ', trac.frame_id)
                # print('loc ', trac.location)
                # print('time ', trac.time_since_update)
                # print('tlbr: ', trac.tlbr)
                # print('tlwh: ', trac.tlwh)
                # print('id: ', trac.track_id)
                # print('score: ', trac.score)

        return tracks