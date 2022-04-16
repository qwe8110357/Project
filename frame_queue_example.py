import pyrealsense2 as rs
import time
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
def slow_processing(frame):
    n = frame.get_frame_number() 
    if n % 20 == 0:
        time.sleep(1/4)
    print(n)
def slower_processing(frame):
    n = frame.get_frame_number() 
    if n % 20 == 0:
        time.sleep(1)
    print(n)    
print("Slow callback")
pipeline.start(config)

start = time.time()

while time.time() - start < 5:
    frames = pipeline.wait_for_frames()
    slow_processing(frames)
    pipeline.stop()                   