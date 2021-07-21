from opencv.device import Camera
from opencv.processors_cam import findFaceGetPulse
import cv2
import sys




class getPulseApp(object):


    def __init__(self):
        self.cameras = []
        self.selected_cam = 0
        camera = Camera(camera=0)
        self.cameras.append(camera)

        self.w, self.h = 0, 0
        self.pressed = 0

        self.processor = findFaceGetPulse(bpm_limits=[50, 160],
                                          data_spike_limit=2500.,
                                          face_detector_smoothness=10.)

        self.plot_title = "Data display - raw signal (top) and PSD (bottom)"

        self.key_controls = {"s": self.toggle_search,
                             }


    def toggle_search(self):
        state = self.processor.find_faces_toggle()
        print("face detection lock =", not state)



    def key_handler(self):

        self.pressed = waitKey(10) & 255  # wait for keypress for 10 ms
        if self.pressed == 27:  # exit program on 'esc'
            print("Exiting")
            for cam in self.cameras:
                cam.cam.release()
            sys.exit()

        for key in self.key_controls.keys():
            if chr(self.pressed) == key:
                self.key_controls[key]()

    def main_loop(self):

        frame = self.cameras[self.selected_cam].get_frame()
        self.h, self.w, _c = frame.shape
        self.processor.frame_in = frame

        self.processor.run(self.selected_cam)
        output_frame = self.processor.frame_out
        cv2.imshow("Processed", output_frame)

        self.key_handler()

def waitKey(*args,**kwargs):
    return cv2.waitKey(*args,**kwargs)

if __name__ == "__main__":

    App = getPulseApp()
    while True:
        App.main_loop()
