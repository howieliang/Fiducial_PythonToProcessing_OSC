//*********************************************
// Example Code: ArUCo Fiducial Marker Detection in OpenCV Python and then send to Processing via OSC
// Rong-Hao Liang: r.liang@tue.nl
//*********************************************

// Import the necessary libraries for OSC communication
import oscP5.*;
import netP5.*;

TagManager tm;
OscP5 oscP5;
final float SCALE = 100*10;

void setup() {
  // Set the canvas size to 800x800 pixels with a 3D rendering context
  size(800, 800, P3D);
  
  // Initialize the OSC communication on port 9000 (should match the port used in Python)
  oscP5 = new OscP5(this, 9000);
  
  // Create a TagManager to manage ArUco fiducial markers
  tm = new TagManager(600);

  // Set up the camera for the 3D scene
  PVector cameraPosition = new PVector(0, 0, -10);
  PVector lookAt = new PVector(0, 0, 0);
  PVector cameraUp = new PVector(0, 1, 0);
  camera(cameraPosition.x, cameraPosition.y, cameraPosition.z,
    lookAt.x, lookAt.y, lookAt.z,
    cameraUp.x, cameraUp.y, cameraUp.z);
}

void draw() {
  // Clear the background with white
  background(255);
  
  // Update and display the ArUco fiducial markers in 3D space
  tm.update();
  tm.display3D();
}

void oscEvent(OscMessage msg) {
  // Check if the received OSC message matches the address pattern "/message"
  if (msg.checkAddrPattern("/message")) {
    // Extract data from the OSC message
    int id = msg.get(0).intValue();
    float x = msg.get(1).floatValue();
    float y = msg.get(2).floatValue();
    float z = msg.get(3).floatValue();
    float r = msg.get(4).floatValue();
    float p = msg.get(5).floatValue();
    float yaw = msg.get(6).floatValue();
    
    // Update the TagManager with the received fiducial marker data
    // (scaling the position by a factor of *scale*)
    tm.set(id, x * SCALE, y * SCALE, z * SCALE, r, p, yaw);
  }
}
