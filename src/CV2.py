import cv2
import numpy as np
import time
class LIVE_CAMERA_STERAM:
    def __init__(self,channel):
        self.channel = channel
        self.cam_url = f"rtsp://admin:aarush252011%21@192.168.1.98:554/Streaming/Channels/{self.channel}02"
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


class RECORDED_STERM:
    def __init__(self, rtsp_template, total_minutes,input_time):
        self.base_url = rtsp_template
        self.total_minutes = total_minutes
        self.input_time = input_time
        
        # Application States (Now instance attributes instead of globals!)
        self.current_minute = 0
        self.is_dragging = False
        self.stream_changed = True
        self.is_paused = False
        
        # Dynamic window dimension tracking
        self.window_w = 1280
        self.window_h = 720
        self.timeline_h = 80
    
        self.window_name = "RECORDED_FOOTAGE"
        self.cam = None
    def recorded_effact_control(self,frame,current_effect_idx):
         if current_effect_idx == 'normal':
            return frame
         elif current_effect_idx == 'night vision':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            bright_gray = cv2.convertScaleAbs(gray, alpha=1.5,beta=50)
            effect_frame = cv2.applyColorMap(bright_gray, cv2.COLORMAP_WINTER) 
            return cv2.GaussianBlur(effect_frame, (5, 5), 0)
            
         elif current_effect_idx == 'thermal vision':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return cv2.applyColorMap(gray, cv2.COLORMAP_INFERNO)
            
         elif current_effect_idx == 'ADVANS thermal vision':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            inverted = cv2.bitwise_not(gray)
            return cv2.applyColorMap(inverted, cv2.COLORMAP_INFERNO) 
            
         elif current_effect_idx == 'invert':
            return cv2.bitwise_not(frame)
            
         elif current_effect_idx == 'cartoon':
            color = cv2.bilateralFilter(frame, d=9, sigmaColor=200, sigmaSpace=200)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, blockSize=9, C=9)
            edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            cartoon = cv2.bitwise_and(color, edges_bgr)
            return cartoon
            
         elif current_effect_idx == 'cyber punk':
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
         elif current_effect_idx == 'light enhancer':
            ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
            channels = list(cv2.split(ycrcb))
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            channels[0] = clahe.apply(channels[0])
            processed_ycrcb = cv2.merge(channels)
            return cv2.cvtColor(processed_ycrcb, cv2.COLOR_YCrCb2BGR)

    def mouse_callback(self, event, x, y, flags, param):
    
        if y >= self.window_h:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.is_dragging = True
                self.current_minute = int((x / self.window_w) * self.total_minutes)
                self.current_minute = max(0, min(self.current_minute, self.total_minutes - 1))
                self.stream_changed = True

            elif event == cv2.EVENT_MOUSEMOVE and self.is_dragging:
                new_min = int((x / self.window_w) * self.total_minutes)
                new_min = max(0, min(new_min, self.total_minutes - 1))
                if new_min != self.current_minute:
                    self.current_minute = new_min
                    self.stream_changed = True

        if event == cv2.EVENT_LBUTTONUP:
            self.is_dragging = False

    def draw_interface(self, video_frame,current_effect):
        # Create dark charcoal timeline background
        frame_resized = cv2.resize(video_frame, (self.window_w, self.window_h))
        prosessed_video = self.recorded_effact_control(frame_resized,current_effect)
        timeline_panel = np.zeros((self.timeline_h, self.window_w, 3), dtype=np.uint8)
        timeline_panel[:] = (40, 40, 40)

        # Draw ruler ticks
        for i in range(self.total_minutes + 1):
            tick_x = int((i / self.total_minutes) * self.window_w)
            cv2.line(timeline_panel, (tick_x, 0), (tick_x, int(self.timeline_h * 0.25)), (100, 100, 100), 2)
            
            font_scale = self.window_w / 2500
            cv2.putText(timeline_panel, f"{self.input_time}:{i:02d}:00", (tick_x + 5, int(self.timeline_h * 0.55)), 
                        cv2.FONT_HERSHEY_SIMPLEX, max(0.3, font_scale), (150, 150, 150), 1, cv2.LINE_AA)

        # Draw slider track
        track_y = int(self.timeline_h * 0.75)
        cv2.line(timeline_panel, (0, track_y), (self.window_w, track_y), (60, 60, 60), 2)

        # Draw vertical blue playhead needle
        playhead_x = int(((self.current_minute + 0.5) / self.total_minutes) * self.window_w)
        cv2.line(timeline_panel, (playhead_x, 0), (playhead_x, self.timeline_h), (255, 144, 30), 2)
        cv2.rectangle(timeline_panel, (playhead_x - 8, 0), (playhead_x + 8, int(self.timeline_h * 0.2)), (255, 144, 30), -1)

        # Glue panels together
        combined_ui = np.vstack((prosessed_video, timeline_panel))

        return combined_ui

    def recorded_sterm(self):
        cv2.namedWindow(self.window_name)
        
        # Crucial: Connect OpenCV mouse tracker directly to this class instance method
        cv2.setMouseCallback(self.window_name, self.mouse_callback)
        current_effect_idx = 'normal'
        while True:
            if self.stream_changed:
                if self.cam is not None:
                    self.cam.release()
                new_url = self.base_url.format(self.current_minute)
                self.cam = cv2.VideoCapture(new_url)
                self.stream_changed = False
            elif cv2.waitKey(1) == ord('p'):
                self.is_paused = True
            elif cv2.waitKey(1) == ord('s'):
                self.is_paused = False
            elif self.is_paused == True:
                time.sleep(0.03)
                continue

            ret, frame = self.cam.read()
            
            if not ret:
                w_width = self.window_w if self.window_w > 0 else 1280
                w_height = self.window_h if self.window_h > 0 else 720
                placeholder = np.zeros((w_height, w_width, 3), dtype=np.uint8)
                cv2.putText(placeholder, "CONNECTING / BUFFERING...", (w_width//2 - 150, w_height//2), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
                ui_output = self.draw_interface(placeholder)
            else:
                ui_output = self.draw_interface(frame,current_effect_idx)


            cv2.imshow(self.window_name, ui_output)


            # Press 'a' to quit
            key = cv2.waitKey(1)
            if key == ord('a'):
                break
            elif key == ord('d'):
                current_effect_idx = 'normal'
            elif key == ord('n'):
                current_effect_idx = 'night vision'
            elif key == ord('t'):
                current_effect_idx = 'thermal vision'
            elif key == ord('g'):
                current_effect_idx = 'ADVANS thermal vision'
            elif key == ord('i'):
                current_effect_idx = 'invert'
            elif key == ord('c'):
                current_effect_idx = 'cartoon'
            elif key == ord('y'):
                current_effect_idx = 'cyber punk'
            elif key == ord('l'):
                current_effect_idx = 'light enhancer'
               
        if self.cam is not None:
            self.cam.release()
        cv2.destroyAllWindows()

