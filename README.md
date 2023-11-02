# Fiducial_PythonToProcessing_OSC

ArUco Fiducial Marker Detection in OpenCV using Python, then send the results to Processing via OSC protocol.

by Rong-Hao Liang: r.liang@tue.nl

Update (Sep 27, 2023): Tested with opencv-python ver. 4.6.0.66 and Processing 4.2

ArUco tags are a type of fiducial marker often used in computer vision applications for camera-based localization and tracking. 
More Info on ArUCo Markers: [https://docs.opencv.org/3.2.0/d5/dae/tutorial_aruco_detection.html](https://docs.opencv.org/3.2.0/d5/dae/tutorial_aruco_detection.html)

## Install Python Environment

1. Install MiniConda
    - [https://docs.conda.io/projects/miniconda/en/latest/miniconda-other-installer-links.html](https://docs.conda.io/projects/miniconda/en/latest/miniconda-other-installer-links.html)
2. Open MiniConda Prompt / PowerShell (Windows) or Terminal (Mac)

```bash
conda create --name p39 python=3.9
conda activate p39
pip install opencv-contrib-python==4.6.0.66
pip install python-osc
```

## **Camera Calibration**

1. Capture and Save Sample Images for Calibration

```bash
python camCapture.py
```

- Prepare the checkerboard pattern
![checkerboard](/Python/ArUco/calibPattern.png)

- Press the SPACE key to save 3-4 snapshots from the camera.
![fig1](/Python/ArUco/0.jpg)
![fig2](/Python/ArUco/1.jpg)
![fig3](/Python/ArUco/2.jpg)
![fig4](/Python/ArUco/3.jpg)

2. Load the camera-captured images and save the calibration data as a JSON file.

```bash
python camCalib.py
```

- Press the SPACE key to browse the saved images
- The _camera.json_ file is saved after the execution

3. Capture the ArUCo markers using the calibrated camera.

```bash
python main.py
```

- Initialize a video capture object with the default camera (0) in the code. If you have another camera, change the index to 1.

```python
cap = cv2.VideoCapture(0)  
```

## **Marker Generation**

You can use [this website](https://chev.me/arucogen/) to generate and print Aruco markers (select the "Original Aruco" option on the dropdown). Or, use the aruco_gen_page.py file to create an array of printed markers for printing on an A4 paper. The aruco_gen_page.py file is adapted from Jes Fink-Jensen (https://betterprogramming.pub/getting-started-with-aruco-markers-b4823a43973c)

```python
python aruco_gen_page.py -o "aruco_markers.png" -i 0 -d 72 --write-id -x 3 -y 4
```
![fig1](/Python/ArUco/aruco_markers50.png)


## Install Processing Environment

1. Install Processing ([https://processing.org/download](https://processing.org/download))
2. Install the oscp5 library ([https://sojamo.de/libraries/oscP5/](https://sojamo.de/libraries/oscP5/)) from the contribution manager
3. Run the Processing sketch Processing/MarkerReceiverOSC_v1/MarkerReceiverOSC_v1.pde
