from ultralytics import YOLO
import numpy as np
import cv2
import os
from datetime import datetime 
import time
from plyer import notification
class DITECTERS:
    def __init__(self,coondenats_of_the_zone):
       self.DVRurl =  "rtsp://admin:aarush252011%21@192.168.1.98:554/Streaming/Channels/302"
       self.model = YOLO('yolo26n.pt')
       self.save_dir = "snapshots"
       os.makedirs(self.save_dir, exist_ok=True)
       self.last_capture_time = 0
       self.cooldown_time = 2
       self.is_intruder = False
       self.captured_ids = set()
       self.is_intruder_data = {}
       self.points = [[223, 41], [272, 17], [357, 199], [315, 241], [227, 47], [311, 108], [316, 234]]
       self.coondenats_of_the_zone = coondenats_of_the_zone
    def ditec(self):
        cam = cv2.VideoCapture(self.DVRurl)
        zone_points = np.array(self.points,np.int32)
        zone_points = zone_points.reshape((-1, 1, 2))
        while True:
            ret, frame = cam.read()
            if not ret:
                print('OOP!')
                pass
            frame = cv2.resize(frame, (640, 480))
            results = self.model.track(
                source=frame, 
                conf=0.5, 
                classes=[0, 1], 
                persist=True,     
                stream=False, 
                verbose=False,
            )
            r = results[0]
            if r.boxes is not None:
                boxes = r.boxes.xyxy.cpu().numpy()
                object_clss = r.boxes.cls.cpu().numpy().astype(int) if r.boxes.cls is not None else ["?"] * len(boxes)
                track_ids = r.boxes.id.cpu().numpy().astype(int) if r.boxes.id is not None else ["?"] * len(boxes)

                for box,object_id, track_id in zip(boxes,object_clss,track_ids):
                    x1,y1,x2,y2 = map(int,box)
                    feet_point = (int(x1 + x2) / 2),int(y2)
                    is_inside = cv2.pointPolygonTest(zone_points,feet_point,False)
                    if is_inside >= 0:
                        self.is_intruder = True
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                        cv2.putText(frame, f"INTRUDER {track_id}", (int(x1), int(y1) - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    else:
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                        object_name = r.names[object_id]
                        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                        cv2.putText(frame, f"ID: {object_name}", (x1, y1 - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        currten_time = time.time()
            if self.is_intruder:
                cv2.putText(frame, "WARNING: ZONE BREACHED!", (20, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                if track_id not in self.captured_ids:
                    if (currten_time - self.last_capture_time) > self.cooldown_time:
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                        print('A INTRUDER DETECHEDED IN CAMERA 1')
                        print(f'AT COORDEDNETS {x2,y2}')
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            
                        crop_img = frame
                        crop_path = os.path.join(self.save_dir, f"person_{track_id}_{timestamp}_crop.jpg")
                        cv2.imwrite(crop_path, crop_img)
                        self.is_intruder_data['intruder1'] = {'object id':object_name,'AT COORDENETS':{x2,y2},'AT':{timestamp}}
                        notification.notify(
                            title="INTRUEDER",
                            message=f"THERE IS SOMEONE AT YOUR DOOR {crop_path} at {timestamp}",
                           app_name="My Cross-Platform App",
                            timeout=10 
                        )
                        self.captured_ids.add(track_id)
                        self.last_capture_time = currten_time
                    else:
                        self.captured_ids.add(track_id)
            zone_color = (0, 0, 255)
            cv2.polylines(frame, [zone_points], True, zone_color, 3)
            cv2.imshow("YOLO Zone Intrusion", frame)
            cv2.imshow('ditec',frame)
            if cv2.waitKey(1) == ord('a'):
                break
        cam.release()
        cv2.destroyAllWindows()


    def click_event(self, event, x, y, flags, param):
        img = param
        if event == cv2.EVENT_LBUTTONDOWN:  
            print(f"Clicked coordinate: [{x}, {y}]")
            self.points.append([x, y])
            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
            if len(self.points) > 1:
                cv2.line(img, tuple(self.points[-2]), (x, y), (0, 255, 0), 2)
            cv2.imshow('Coordinate Finder', img)
    def get_coon(self):
        while True:
            user_image = input('ENTER YOU IMAGE TO MAPE:- ')
            img = cv2.imread(user_image)
            img = cv2.resize(img, (640, 480))
            if img is None:
                print('the img is not found')
            elif img is not None:
                break
        cv2.namedWindow('Coordinate Finder')
        cv2.setMouseCallback('Coordinate Finder', self.click_event, param=img)
        cv2.imshow('Coordinate Finder', img)
        while True:
            key = cv2.waitKey(1)
            if key == ord('a'):
                break
        cv2.destroyAllWindows()
        print("\nFinal Coordinates for your code:")
        print(self.points)

    
