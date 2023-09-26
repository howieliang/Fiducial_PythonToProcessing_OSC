// Define a class called TagManager to manage an array of Tag objects.
class TagManager {
  Tag[] tags; // Declare an array of Tag objects.
  
  // Constructor for the TagManager class, takes an integer 'n' as a parameter.
  TagManager(int n) {
    tags = new Tag[n]; // Initialize the 'tags' array with 'n' elements.
    
    // Loop through the array and create a new Tag object for each element.
    for (int i = 0; i < n; i++) {
      tags[i] = new Tag(i);
    }
  }
  
  // Set method to update the properties of a specific Tag object by its 'id'.
  void set(int id, float x, float y, float z, float r, float p, float yaw) {
    tags[id].set(x, y, z, r, p, yaw); // Call the set method on the specified Tag object.
  }
  
  // Update method to check the activity status of all Tag objects.
  void update() {
    for (Tag t : tags) {
      t.checkActive(); // Call the checkActive method on each Tag object.
    }
  }
  
  // Display method to display all Tag objects.
  void display2D() {
    for (Tag t : tags) {
      t.display2D(); // Call the display method on each Tag object.
    }
  }
  
  // Display3D method to display all Tag objects in a 3D context.
  void display3D() {
    for (Tag t : tags) {
      t.display3D(); // Call the display3D method on each Tag object.
    }
  }
}
