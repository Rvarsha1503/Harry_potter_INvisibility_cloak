from flask import Flask, Response, render_template, jsonify
import cv2
import numpy as np
import time

app = Flask(__name__)

cap = cv2.VideoCapture(0)  # open the cam
background = None  # where the bg gets saved

def capture_background(num_frames=60):
    """grab the bg for the invis effect"""
    global background

    # reinit the cam if needed
    global cap
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ yo, can't access the cam! check perms.")
        return False

    print("📸 gonna grab the bg now... pls no blue stuff in the frame!")
    time.sleep(2)

    frames = []
    for _ in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            print("❌ frame capture failed! check the cam connection.")
            return False
        
        frame = np.flip(frame, axis=1)
        frames.append(frame)
        time.sleep(0.05)

    background = np.median(frames, axis=0).astype(dtype=np.uint8)
    print("✅ bet! bg captured.")
    return True

def refine_mask(mask):
    """smooth out the mask so the invis effect pops better"""
    kernel = np.ones((7, 7), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=1)
    return mask

def invisibility_effect():
    """apply the invisibility effect and stream it to the bros."""
    global background
    if background is None:
        if not capture_background():
            return  # if bg capture fails, just dip

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = np.flip(frame, axis=1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # set the blue color range (blue objects get the invis vibe)
        lower_blue = np.array([80, 80, 80])
        upper_blue = np.array([150, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        mask = refine_mask(mask)

        inverse_mask = cv2.bitwise_not(mask)
        res1 = cv2.bitwise_and(background, background, mask=mask)
        res2 = cv2.bitwise_and(frame, frame, mask=inverse_mask)
        final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

        _, buffer = cv2.imencode('.jpg', final_output)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video_feed():
    return Response(invisibility_effect(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/restart', methods=['POST'])
def restart():
    """reset the bg and restart the magic"""
    global background
    background = None  # reset that bg
    if capture_background():
        return jsonify({'status': '✅ bg recaptured! we good.'})
    return jsonify({'status': '❌ nah, bg capture failed'}), 500

if __name__ == "__main__":
    capture_background()
    app.run(debug=True, use_reloader = False)
