import cv2

class Preview:

    def __init__(self): 
        self.video_input_object = cv2.VideoCapture(0) 
        
    def open_preview(self):
        while True:
            ret, frame = self.video_input_object.read()
            if not ret:
                break
            cv2.imshow('Preview', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def open_preview_configured(self):
        while True:
            ret, frame = self.video_input_object.read()
            if not ret:
                break
            region_of_interest = (0, 60, 640, 360)
            x, y, w, h = region_of_interest
            roi_frame = frame[y:y+h, x:x+w]
            gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
            cv2.putText(gray_frame, 'Press the "q" key to capture', (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.imshow('Preview', gray_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break