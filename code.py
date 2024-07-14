import cv2
import numpy as np
import time

def capture_background(cap, num_frames=60):
    background_frames = []
    for _ in range(num_frames):
        ret, frame = cap.read()
        if ret:
            frame = np.flip(frame, axis=1)
            background_frames.append(frame)
        time.sleep(0.1)  # slight delay to capture stable frames
    return np.median(background_frames, axis=0).astype(dtype=np.uint8)

def refine_mask(mask):
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.dilate(mask, kernel, iterations=1)
    return mask

def main():
    cap = cv2.VideoCapture(0)
    
    print("Capturing background. Please ensure the blue cloth is not in the frame.")
    time.sleep(2)
    background = capture_background(cap)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = np.flip(frame, axis=1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define a broader range for blue color to detect variations
        lower_blue = np.array([90, 100, 100])
        upper_blue = np.array([140, 255, 255])
        
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        mask = refine_mask(mask)
        
        # Create an inverse mask
        inverse_mask = cv2.bitwise_not(mask)

        # Segment out the blue color part by creating the inverse mask
        res1 = cv2.bitwise_and(background, background, mask=mask)
        res2 = cv2.bitwise_and(frame, frame, mask=inverse_mask)

        # Combine the background and the current frame
        final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

        cv2.imshow('Harry Potter Invisibility Cloak', final_output)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
