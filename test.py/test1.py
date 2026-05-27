import sys
import datetime
import cv2
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QRectF, QPointF
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QColor, QPen, QImage, QPixmap

# ==============================================================================
# CONFIGURATION BLOCK - CHANGE THESE VALUES TO MATCH YOUR NVR SETTINGS BEFORE RUNNING
# ==============================================================================
NVR_IP = "192.168.1.98"      # Your NVR's local IP address
NVR_USER = "admin"            # Your NVR Username
NVR_PASSWORD = "aarush252011%21"  # Your NVR Password
CAMERA_CHANNEL = "101"        # 101 = Cam 1 Main Stream | 102 = Cam 1 Sub Stream (Highly Recommended for Speed)

# ==============================================================================
# 1. VIDEO DECODING ENGINE
# ==============================================================================
# ==============================================================================
# 1. FIXED DVR VIDEO DECODING ENGINE
# ==============================================================================
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.rtsp_url = None
        self.cap = None

    def set_rtsp_url(self, url):
        """Safely updates the destination stream and reinitializes OpenCV capture."""
        self.rtsp_url = url
        if self.cap and self.cap.isOpened():
            self.cap.release()
            
        print(f"\n[NETWORK]: Connecting to DVR Channel: {self.rtsp_url}")
        
        # Open the capture object with strict ffmpeg protocol allocations
        self.cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
        
        if self.cap.isOpened():
            print("[SUCCESS]: Handshake complete. DVR is actively fetching footage...")
            # CRITICAL FOR DVRs: Wait a moment for the DVR hard drive to seek and fill buffer
            self.msleep(1500) 
        else:
            print("[ERROR]: Connection failed. Check your DVR time configurations.")
        
    def run(self):
        while self._run_flag:
            if self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    # Frame found! Convert from OpenCV BGR to PyQt RGB
                    height, width, channel = frame.shape
                    bytes_per_line = channel * width
                    qt_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
                    self.change_pixmap_signal.emit(qt_img)
                else:
                    # DVRs take time to stream playback frames. If a frame drops, 
                    # do NOT pause indefinitely; wait 50ms and check again.
                    self.msleep(50)
            else:
                self.msleep(30)

    def stop(self):
        self._run_flag = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.wait()
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width, height = self.width(), self.height()
        
        # Draw background canvas frame
        painter.fillRect(0, 0, width, height, QColor("#1e1e1e"))
        
        # Draw storage timeline data tracks (Blue bars)
        painter.setBrush(QColor("#2980b9"))
        painter.setPen(Qt.PenStyle.NoPen)
        for seg_start, seg_end in self.recorded_segments:
            x_start = ((seg_start - self.start_epoch) / self.total_duration) * width
            x_end = ((seg_end - self.start_epoch) / self.total_duration) * width
            painter.drawRect(QRectF(x_start, 25, x_end - x_start, height - 45))
            
        # Draw time rulers
        painter.setPen(QPen(QColor("#95a5a6"), 1))
        for hour in range(25):
            x = (hour / 24) * width
            painter.drawLine(QPointF(x, 0), QPointF(x, 8))
            if hour % 4 == 0:
                painter.drawText(int(x) + 4, 20, f"{hour:02d}:00")

        # Draw seeker playhead indicator line
        playhead_x = ((self.current_epoch - self.start_epoch) / self.total_duration) * width
        painter.setPen(QPen(QColor("#e74c3c"), 2))
        painter.drawLine(QPointF(playhead_x, 0), QPointF(playhead_x, height))
        painter.setBrush(QColor("#e74c3c"))
        painter.drawEllipse(QPointF(playhead_x, 4), 5, 5)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.update_seeker(event.position().x())

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            self.update_seeker(event.position().x())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            self.time_changed.emit(self.current_epoch)

    def update_seeker(self, mouse_x):
        width = self.width()
        if width <= 0: return
        mouse_x = max(0, min(mouse_x, width))
        self.current_epoch = self.start_epoch + ((mouse_x / width) * self.total_duration)
        self.update()


# ==============================================================================
# 3. INTERFACE FRAME CONTAINER
# ==============================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NVR Core Control Console")
        self.setGeometry(100, 100, 950, 650)
        self.setStyleSheet("background-color: #2c3e50; color: white;")

        main_layout = QVBoxLayout()
        
        self.video_display = QLabel("Interactive Timeline Console\n[Click on the timeline track below to test stream connection]")
        self.video_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_display.setStyleSheet("background-color: #000000; font-size: 14px; font-family: monospace;")
        self.video_display.setMinimumHeight(450)
        main_layout.addWidget(self.video_display)

        self.time_label = QLabel("Current Selection: --:--:--")
        self.time_label.setStyleSheet("font-size: 13px; font-weight: bold; background: #34495e; padding: 5px;")
        main_layout.addWidget(self.time_label)


        self.timeline.time_changed.connect(self.on_timeline_scrubbed)
        main_layout.addWidget(self.timeline)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Deploy thread engine loops
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_video_frame)
        self.thread.start()

    def update_video_frame(self, qt_img):
        """Receives decoded frames from the video thread and renders them to the screen."""
        if qt_img.isNull():
            return
            
        # Scale image dynamically to fit screen layout while keeping aspect ratio
        scaled_pixmap = QPixmap.fromImage(qt_img).scaled(
            self.video_display.width(), 
            self.video_display.height(), 
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation # Makes the playback look crisp
        )
        
        self.video_display.setPixmap(scaled_pixmap)
        self.video_display.repaint() # <--- ADD THIS LINE: Forces the UI to immediately redraw the new frame
    def on_timeline_scrubbed(self, target_epoch):
        # 1. Convert the timeline click into a Python datetime object
        dt_object = datetime.datetime.fromtimestamp(target_epoch)
        
        # ==============================================================================
        # FORCE A WORKING DVR TIME SLOT FOR TESTING
        # Change these numbers to a specific date/time you KNOW your DVR has video!
        # ==============================================================================
        dt_object = dt_object.replace(
            year=2026, 
            month=5, 
            day=26,    # Change to a day with known recordings
            hour=14,   # Pick an hour with known recordings (14 = 2:00 PM)
            minute=0, 
            second=0
        )
        # ==============================================================================
        
        # 2. DVRs require an explicit End Time. We will set it to 30 minutes after the start time.
        end_dt_object = dt_object + datetime.timedelta(minutes=30)
        
        self.time_label.setText(f"Target Timestamp Sent: {dt_object.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 3. Format both timestamps for the Hikvision DVR firmware
        start_str = dt_object.strftime("%Y%m%dt%H%M%S") + "z"
        end_str = end_dt_object.strftime("%Y%m%dt%H%M%S") + "z"
        
        # 4. THE DVR FIX: Note the use of 'channels' instead of 'tracks'
        # CAMERA_CHANNEL should be "101" for Camera 1 Main Stream
        rtsp_url = f"rtsp://{NVR_USER}:{NVR_PASSWORD}@{NVR_IP}:554/Streaming/channels/{CAMERA_CHANNEL}?starttime={start_str}&endtime={end_str}"
        
        print(f"[DVR PLAYBACK]: Requesting URL -> {rtsp_url}")
        
        # Pass the corrected string into your active player thread
        self.thread.set_rtsp_url(rtsp_url)
        # Build Hikvision standardized text string (Universal Format Matcher)
       
        # Replace the URL construction block with this:
        start_str = dt_object.strftime("%Y%m%dt%H%M%S") + 'Z'
        end_dt = dt_object + datetime.timedelta(minutes=1)
        end_str = end_dt.strftime("%Y%m%dt%H%M%S") + 'Z'

        rtsp_url = f"rtsp://{NVR_USER}:{NVR_PASSWORD}@{NVR_IP}:554/Streaming/tracks/{CAMERA_CHANNEL}?starttime={start_str}&endtime={end_str}"
        # Build absolute authenticated endpoint target string

        # Pass payload string directly into active player loop thread
        self.thread.set_rtsp_url(rtsp_url)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())