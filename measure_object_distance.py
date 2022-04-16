
import cv2
from realsense_camera import *
from mask_rcnn import *

# Load Realsense camera
rs = RealsenseCamera()
mrcnn = MaskRCNN()
prereal_coordinate=np.zeros((3,90))
while True:

	# Get frame in real time from Realsense camera
	ret, bgr_frame, depth_frame, color_frame,Odepth_frame = rs.get_frame_stream()

	# Get object mask
	boxes, classes, contours, centers = mrcnn.detect_objects_mask(bgr_frame)

	# Draw object mask
	bgr_frame = mrcnn.draw_object_mask(bgr_frame)

	# Show depth info of the objects
	non,prereal_coordinate=mrcnn.draw_object_info(bgr_frame, depth_frame, color_frame,Odepth_frame,prereal_coordinate)


	#cv2.imshow("depth frame", depth_frame)
	cv2.imshow("Bgr frame", bgr_frame)

	key = cv2.waitKey(1)
	if key & 0xFF == ord('q') or key == 27:
		break

rs.release()
cv2.destroyAllWindows()
