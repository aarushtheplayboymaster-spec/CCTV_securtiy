#imported custom modols from files
import keyboard
from src.CV2 import CAMERA_STERAM
#one faction to start the program
#it connects with live sterm
def main():
    challen_no = input('Enter your challen number:- ') 
    cam = CAMERA_STERAM(challen_no)
    cam.main_steram()
#it connects with  all live sterms
def whole_sterm():
    cam = CAMERA_STERAM(channel=None)
    cam.main_steram_as_whole()
#it ables you to control effact modes
def main_effacts():
    challen_no = input('Enter your challen number:- ') 
    cam = CAMERA_STERAM(challen_no)
    cam.main_sterm_effacts_controling()
#it connects with recorded sterm
def recorded():
    cam = CAMERA_STERAM()
    cam.recorded_sterm()
if __name__ == '__main__':
    keyboard.add_hotkey('shift+L',main)
    keyboard.add_hotkey('shift+W',whole_sterm)
    keyboard.add_hotkey('shift+C',main_effacts)

    keyboard.add_hotkey('shift+R',recorded)
    keyboard.wait('a')