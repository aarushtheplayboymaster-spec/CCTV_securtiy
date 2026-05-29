#imported custom modols from files
import keyboard
from datetime import datetime
from src.CV2 import LIVE_CAMERA_STERAM
from src.CV2 import RECORDED_STERM
#one faction to start the program
#it connects with live sterm
def main():
    challen_no = input('Enter your challen number:- ') 
    cam = LIVE_CAMERA_STERAM(challen_no)
    cam.main_steram()
#it connects with  all live sterms
def whole_sterm():
    cam = LIVE_CAMERA_STERAM(channel=None)
    cam.main_steram_as_whole()
#it ables you to control effact modes
def main_effacts():
    challen_no = input('Enter your challen number:- ') 
    cam = LIVE_CAMERA_STERAM(challen_no)
    cam.main_sterm_effacts_controling()
#it connects with recorded sterm
def recorded_sterm():
    DATE_STR = input('ENTER YOUR DATE:- ')
    START_HOUR_STR = input('ENTER YOUR STARTING HOUR:- ')
    END_HOUR_STR = input('ENTER YOUR ENDING HOUR:- ')
    START_MIN_STR = input('ENTER YOUR STARTING MIN:- ')
    END_MIN_STR = input('ENTER YOUR ENDING MIN:- ')
    channals = input('ENTER YOUR ENDING MIN:- ')

    RAW_START = f"{DATE_STR}T{START_HOUR_STR}{START_MIN_STR}00"
    RAW_END   = f"{DATE_STR}T{END_HOUR_STR}{ END_MIN_STR }00"
    
    time_format = "%Y%m%dT%H%M%S"
    start_time = datetime.strptime(RAW_START, time_format)
    end_time = datetime.strptime(RAW_END, time_format)
    total_minutes = int((end_time - start_time).total_seconds() / 60)
    

    print(f"--- Software Engine Initialized ---")
    print(f"Detected Stream Duration: {total_minutes} Minutes")

    # 4. Construct a perfect, clean URL template with the placeholder built right in
    # This guarantees Python can inject the scrubbed minutes directly without string collisions
    REPLACEABLE_URL= (
        f"rtsp://admin:aarush252011%21@192.168.1.98:554/Streaming/Tracks/{channals}01?"
        f"starttime={DATE_STR}T{START_HOUR_STR}{{:02d}}00Z&"
        f"endtime={DATE_STR}T{END_HOUR_STR}{END_MIN_STR}00Z"
    )
    cam = RECORDED_STERM(REPLACEABLE_URL,total_minutes,START_HOUR_STR)
    cam.recorded_sterm()
if __name__ == '__main__':
    keyboard.add_hotkey('shift+L',main)
    keyboard.add_hotkey('shift+W',whole_sterm)
    keyboard.add_hotkey('shift+C',main_effacts)
    keyboard.add_hotkey('shift+R',recorded_sterm)
    keyboard.wait('a')