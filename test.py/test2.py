import os
import sys

VLC_PATH = r"C:\Program Files\VideoLAN\VLC"

if sys.platform == "win32":
    if os.path.exists(VLC_PATH):
        os.environ['PATH'] = VLC_PATH + os.pathsep + os.environ['PATH']
        os.add_dll_directory(VLC_PATH)
    else:
        print(f"[CRITICAL ERROR]: VLC was not found at {VLC_PATH}.")
        print("Please verify your VLC installation or update the VLC_PATH variable.")
import datetime
import vlc
from PyQt6.QtCore import Qt, pyqtSignal, QRectF, QPointF
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QColor, QPen

# ==============================================================================
# MASTER CONFIGURATION BLOCK
# ==============================================================================
DVR_IP = "192.168.1.98"          # Your DVR's local IP address
DVR_USER = "admin"                # Your DVR Username
DVR_PASSWORD = "aarush252011%21"  # Your DVR Password
CAMERA_CHANNEL = "101"            # 101 = Cam 1 Main Stream

# ==============================================================================
# 1. CUSTOM TIMELINE USER INTERFACE COMPONENT
# ==============================================================================
class CustomTimeline(QWidget):
    time_changed = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.setMinimumHeight(80)
        
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.start_epoch = today.timestamp()
        self.end_epoch = self.start_epoch + 86400  
        self.total_duration = self.end_epoch - self.start_epoch
        self.current_epoch = self.start_epoch
        
        self.recorded_segments = [
            (self.start_epoch + 0, self.start_epoch + 86400),
        ]
        self.is_dragging = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width, height = self.width(), self.height()
        
        painter.fillRect(0, 0, width, height, QColor("#1e1e1e"))
        
        painter.setBrush(QColor("#2980b9"))
        painter.setPen(Qt.PenStyle.NoPen)
        for seg_start, seg_end in self.recorded_segments:
            x_start = ((seg_start - self.start_epoch) / self.total_duration) * width
            x_end = ((seg_end - self.start_epoch) / self.total_duration) * width
            painter.drawRect(QRectF(x_start, 25, x_end - x_start, height - 45))
            
        painter.setPen(QPen(QColor("#95a5a6"), 1))
        for hour in range(25):
            x = (hour / 24) * width
            painter.drawLine(QPointF(x, 0), QPointF(x, 8))
            if hour % 4 == 0:
                painter.drawText(int(x) + 4, 20, f"{hour:02d}:00")

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
# 2. MAIN WINDOW SYSTEM FRAME (POWERED BY VLC)
# ==============================================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DVR System Core Control Console (VLC Engine Edition)")
        self.setGeometry(100, 100, 950, 650)
        self.setStyleSheet("background-color: #2c3e50; color: white;")

        main_layout = QVBoxLayout()
        
        # This widget becomes the literal video window frame for VLC
        self.video_frame = QWidget()
        self.video_frame.setStyleSheet("background-color: #000000; border: 2px solid #34495e;")
        self.video_frame.setMinimumHeight(450)
        main_layout.addWidget(self.video_frame)

        self.time_label = QLabel("Current Target Selection: --:--:--")
        self.time_label.setStyleSheet("font-size: 13px; font-weight: bold; background: #34495e; padding: 6px; border-radius: 3px;")
        main_layout.addWidget(self.time_label)

        self.timeline = CustomTimeline()
        self.timeline.time_changed.connect(self.on_timeline_scrubbed)
        main_layout.addWidget(self.timeline)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Initialize the VLC Instance Engine and create a media player
        self.vlc_instance = vlc.Instance("--rtsp-transport=tcp", "--no-audio", "--quiet")
        self.media_player = self.vlc_instance.media_player_new()

    def on_timeline_scrubbed(self, target_epoch):
        dt_object = datetime.datetime.fromtimestamp(target_epoch)
        
        # ==============================================================================
        # CRITICAL TEST DATE CONFIGURATION
        # Ensure this matches a day/time your DVR has active saved recordings for!
        # ==============================================================================
        dt_object = dt_object.replace(year=2026, month=5, day=26, hour=14, minute=0, second=0)
        
        end_dt_object = dt_object + datetime.timedelta(minutes=30)
        self.time_label.setText(f"Target Timestamp Sent: {dt_object.strftime('%Y-%m-%d %H:%M:%S')}")
        
        start_str = dt_object.strftime("%Y%m%dt%H%M%S") + "z"
        end_str = end_dt_object.strftime("%Y%m%dt%H%M%S") + "z"
        
        rtsp_url = f"rtsp://{DVR_USER}:{DVR_PASSWORD}@{DVR_IP}:554/Streaming/channels/{CAMERA_CHANNEL}?starttime={start_str}&endtime={end_str}"
        print(f"\n[VLC CORE]: Directing stream to -> {rtsp_url}")

        # Stop any active rendering streams
        self.media_player.stop()

        # Load the destination link directly into the player
        media = self.vlc_instance.media_new(rtsp_url)
        self.media_player.set_media(media)

        # --- THE FIX ---
        # Instead of drawing frame by frame via Python, we inject the operating system
        # Window ID directly into VLC. VLC takes total control of the black box safely.
        if sys.platform == "win32":
            self.media_player.set_hwnd(int(self.video_frame.winId()))
        elif sys.platform == "darwin": # macOS
            self.media_player.set_nsobject(int(self.video_frame.winId()))
        else: # Linux
            self.media_player.set_xwindow(int(self.video_frame.winId()))

        # Wake up the player stream
        self.media_player.play()

    def closeEvent(self, event):
        self.media_player.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())