########################################
# ArUco marker generator
# Adapted from Jes Fink-Jensen
# https://betterprogramming.pub/getting-started-with-aruco-markers-b4823a43973c
# Tested with opencv-python ver. 4.6.0.66
# Use-case 0: python aruco_gen_page.py -o "aruco_markers.png" -i 0 -d 72 --write-id -x 3 -y 4
# Use-case 1: python aruco_gen_page.py -o "aruco_markers.png" -i 0 -t "DICT_5X5_50" -d 72 --write-id -x 3 -y 4
# Use-case 2: python aruco_gen_page.py -o "aruco_markers.png" -i 10 -t "DICT_4X4_50" -d 72 -s 25 -m 10 --no-write-id -x 5 -y7
########################################

# Import necessary libraries
import argparse     # For parsing command line arguments
import cv2          # OpenCV library for computer vision tasks
import sys          # Provides access to some variables used or maintained by the interpreter and to functions that interact with the interpreter
import numpy as np  # Library for numerical operations

# Create an ArgumentParser object to handle command line arguments
ap = argparse.ArgumentParser()

# Add various command line arguments and their descriptions
ap.add_argument("-o", "--output", required=True, help="path to output image containing ArUCo tag")
ap.add_argument("-i", "--id", type=int, required=True, help="ID of first ArUCo tag to generate")
ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="type of ArUCo tag to generate")
ap.add_argument("-d", "--dpi", type=str, default="72", help="the DPI of the output print")
ap.add_argument("-s", "--size", type=int, default=50, help="the size in mm of the ArUco tag")
ap.add_argument("-m", "--margin", type=int, default=5, help="the size in mm of the margins between the ArUco tags")
ap.add_argument("-x", "--x", type=int, default=3, help="number of ArUco tags in the X direction")
ap.add_argument("-y", "--y", type=int, default=4, help="number of ArUco tags in the Y direction")
ap.add_argument("--write-id", default=True, action=argparse.BooleanOptionalAction, help="write the id of the tag or not")

# Parse the command line arguments and store them in a dictionary
args = vars(ap.parse_args())

# Dictionary mapping ArUCo types to their corresponding constant values in OpenCV
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

# Check if the specified ArUCo type is supported
if ARUCO_DICT.get(args["type"], None) is None:
	print("[INFO] ArUCo tag of '{}' is not supported".format(args["type"]))
	sys.exit(0)

# Get the ArUCo dictionary based on the specified type
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
tag_type = args["type"]

# Define dimensions of an A4 paper in millimeters
A4_width = 210
A4_height = 297

# Get user-defined parameters
x = args["x"]
y = args["y"]
size = args["size"]
margin = args["margin"]
text_size = 8

# Adjust text size if writing IDs is disabled
write_id = args["write_id"]
if not(write_id):
	text_size = 0

# Check if the grid contains at least one tag
if x < 1 or y < 1:
	print(f"[INFO] Please make sure that the grid contains at least one tag - i.e. (x > 0) and (y > 0). Currently, x = {x} and y = {y}.")
	sys.exit(0)

# Calculate remaining space on the A4 paper after placing the tags
rest_x = A4_width - (x * size + (x - 1) * margin)
rest_y = A4_height - (y * size + y * text_size + (y - 1) * margin)

# Check if the grid fits on the page
stop = False
if rest_x < 0:
	print(f"[INFO] Please ensure that the grid fits on the page. Consider reducing the number of tags in the x-direction. Currently, x = {x}.")
	stop = True
if rest_y < 0:
	print(f"[INFO] Please ensure that the grid fits on the page. Consider reducing the number of tags in the y-direction. Currently, y = {y}.")
	stop = True
if stop:
	sys.exit(0)

# Calculate half of the remaining space on the x and y axes
half_rest_x = int(np.floor(rest_x/2))
half_rest_y = int(np.floor(rest_y/2))

# Define dimensions of A4 paper at different DPIs
A4_DICT = {
	"72": (595, 842),
	"96": (794, 1123)
}

# Check if the specified DPI is supported
if A4_DICT.get(args["dpi"], None) is None:
	print("[INFO] A4 print of {} DPI is not supported. Please try one of the following: 72, 96.".format(args["dpi"]))
	sys.exit(0)

# Get the dimensions of the A4 paper based on the specified DPI
dpi = A4_DICT[args["dpi"]]

# Create a white canvas representing the A4 paper
page = np.ones((dpi[1],dpi[0],3), dtype="uint8")*255

# Calculate a multiplier for adjusting dimensions based on DPI
multiplier = np.min([dpi[0]/A4_width, dpi[1]/A4_height])

# Adjust dimensions and positions based on the multiplier
size_m = int(np.floor(size * multiplier))
text_size_m = int(np.floor(text_size * multiplier))
margin_m = int(np.floor(margin * multiplier))
half_rest_x_m = int(np.floor(half_rest_x * multiplier))
half_rest_y_m = int(np.floor(half_rest_y * multiplier))

# Initialize the starting ID for the ArUCo tags
tag_id = args["id"]

# Generate and place ArUCo tags on the page
print(f"[INFO] creating {x*y} tags from the {tag_type} dictionary. Starting with id:{tag_id}")
for i in range(0, y):
	for j in range(0, x):
		img = np.ones((size_m,size_m,3), dtype="uint8")*255
		i_val = half_rest_y_m + i*size_m + i*margin_m + 2*i*text_size_m
		j_val = half_rest_x_m + j*size_m + j*margin_m
		tag = np.zeros((size_m, size_m, 1), dtype="uint8")
		cv2.aruco.drawMarker(arucoDict, tag_id, size_m, tag, 1)
		if write_id:
			if "APRILTAG" in tag_type:
				text_string = f"April id: {tag_id}"
			else:
				text_string = f"ArUco id: {tag_id}"
			cv2.putText(page, text_string, (j_val, i_val-margin_m), 
						fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.6, color=(0, 0, 0))
		page[i_val:i_val+size_m, j_val:j_val+size_m] = tag
		tag_id += 1

# Save the generated page with ArUCo tags to the specified output path
cv2.imwrite(args["output"], page)

# Display the generated page with ArUCo tags
cv2.imshow("ArUCo Tags Page", page)

# Wait for a key press and then close the window
cv2.waitKey(0)