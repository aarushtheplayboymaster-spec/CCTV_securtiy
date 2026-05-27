import cv2
import numpy as np
class CAMERA_STERAM:
    def __init__(self,channel):
        self.channel = channel
        self.cam_url = f"rtsp://admin:aarush252011%21@192.168.1.98:554/Streaming/Channels/{self.channel}02"
        self.NVRcam_url = 'rtsp://admin:aarush252011%21@192.168.1.98:8000/Streaming/Tracks/102?starttime=20260521100000&endtime=20260521101000'
        self.cam_whole = [
            {"url": "rtsp://admin:aarush252011%21@192.168.1.98:554/Streaming/Channels/102", "label": "LIVE:"},
            {"url": "rtsp://admin:aarush252011%21@192.168.1.98:554/Streaming/Channels/202", "label": "LIVE:"},
            {"url": "rtsp://admin:aarush252011%21@192.168.1.98:554/Streaming/Channels/302", "label": "LIVE:"},
            {"url": "rtsp://admin:aarush252011%21@192.168.1.98:554/Streaming/Channels/402", "label": "ERROR 404"}
        ]
    # ALL ABOUT LIVE STERMS
    def main_steram(self):
        cam = cv2.VideoCapture(self.cam_url)
        while True:
            rat, fream = cam.read()
            resizing = cv2.resize(fream,(0,0),fx=2,fy=1.5)
            video_states = cv2.putText(resizing,'LIVE:',(20,80),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),3,cv2.LINE_AA)
            cv2.imshow('CCTV CAMERA',video_states)
            if cv2.waitKey(1) == ord('a'):
                break
        cam.release()
        cv2.destroyAllWindows()
    # IT SHOWS ALL THE MAIN STERMS TOGATHERE
    def main_steram_as_whole(self):
        # IT gets all the urls
        cam = [cv2.VideoCapture(whole['url']) for whole in self.cam_whole]
        while True:
            #place holder for fianlley product
            finall = []
            #A FOR LOOP WHICH MAKING AND TRANSFORMS EACH AND EVERY FOOAGE

            for i, cctv in enumerate(cam):
                rat, fream = cctv.read()
                resizing = cv2.resize(fream,(0,0),fx=1,fy=0.5)
                video_status = self.cam_whole[i]['label']
                cv2.putText(resizing,video_status,(20,80),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),3,cv2.LINE_AA)
                finall.append(resizing)
            #COMBINS THOSE VIDEOS INTO A BIG ONE
            top_videos = np.hstack((finall[0],finall[1]))
            bottom_videos = np.hstack((finall[2],finall[3]))
            whole_videos = np.vstack((top_videos,bottom_videos))
            cv2.imshow('all_camers',whole_videos)
            if cv2.waitKey(1) == ord('a'):
                break
        #A FOR LOOP TO RELEASE ALL FOOAGES
        for cam in cam:
            cam.release()
        cv2.destroyAllWindows()
    #ALL THE EFFACT YOU CAN CHOSSE FOR LIVE STREM
    def effact_control(self,frame,effacts):
         if effacts == 'normal':
            return frame
         elif effacts == 'night vision':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            bright_gray = cv2.convertScaleAbs(gray, alpha=1.5,beta=50)
            effect_frame = cv2.applyColorMap(bright_gray, cv2.COLORMAP_WINTER) 
            return cv2.GaussianBlur(effect_frame, (5, 5), 0)
            
         elif effacts == 'thermal vision':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return cv2.applyColorMap(gray, cv2.COLORMAP_INFERNO)
            
         elif effacts == 'ADVANS thermal vision':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            inverted = cv2.bitwise_not(gray)
            return cv2.applyColorMap(inverted, cv2.COLORMAP_INFERNO) 
            
         elif effacts == 'invert':
            return cv2.bitwise_not(frame)
            
         elif effacts == 'cartoon':
            color = cv2.bilateralFilter(frame, d=9, sigmaColor=200, sigmaSpace=200)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, blockSize=9, C=9)
            edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            cartoon = cv2.bitwise_and(color, edges_bgr)
            return cartoon
            
         elif effacts == 'cyber punk':
            b, g, r = cv2.split(frame)
            cyber_r = cv2.addWeighted(r, 0.7, g, 0.3, 0)
            cyber_g = cv2.addWeighted(g, 0.1, b, 0.4, 0)
            cyber_b = cv2.addWeighted(b, 0.8, r, 0.4, 0)
            cyber_frame = cv2.merge([cyber_b, cyber_g, cyber_r])
            hsv = cv2.cvtColor(cyber_frame, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            s = cv2.multiply(s, 1.5)
            v = cv2.multiply(v, 1.2)
            final_hsv = cv2.merge([h, s, v])
            return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
         elif effacts == 'light enhancer':
            ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
            channels = list(cv2.split(ycrcb))
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            channels[0] = clahe.apply(channels[0])
            processed_ycrcb = cv2.merge(channels)
            return cv2.cvtColor(processed_ycrcb, cv2.COLOR_YCrCb2BGR)
    #GIVES ABLETIY TO CONTROL ALL THE EFFACT
    def main_sterm_effacts_controling(self):
        cam = cv2.VideoCapture(self.cam_url)
        current_effact = 'normal'
        while True:
            ret, fream = cam.read()
            resizing = cv2.resize(fream,(0,0),fx=1.5,fy=1)
            video_states = cv2.putText(resizing,'LIVE-effact controling:',(20,80),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),3,cv2.LINE_AA)
            prosecced_video = self.effact_control(video_states,current_effact)
            cv2.imshow('CCTV CAMERA',prosecced_video)
            key = cv2.waitKey(1)
            if key == ord('a'):
                break
            elif key == ord('d'):
                current_effact = 'normal'
            elif key == ord('n'):
                current_effact = 'night vision'
            elif key == ord('t'):
                current_effact = 'thermal vision'
            elif key == ord('g'):
                current_effact = 'ADVANS thermal vision'
            elif key == ord('i'):
                current_effact = 'invert'
            elif key == ord('c'):
                current_effact = 'cartoon'
            elif key == ord('y'):
                current_effact = 'cyber punk'
            elif key == ord('l'):
                current_effact = 'light enhancer'
        cam.release()
        cv2.destroyAllWindows()
    #ALL ABOUT RECORDED STERM
