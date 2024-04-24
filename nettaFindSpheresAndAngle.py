# findSpheresAndAngleOpenMV - By: Netta Shen-Orr - Tue Apr 23 2024
import sensor, image, time, math

# Camera setup
sensor.reset()                              # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE)      # Set pixel format to grayscale.
sensor.set_framesize(sensor.QQVGA)          # Set frame size to QQVGA for faster processing.
sensor.skip_frames(time = 2000)             # Wait for settings to take effect.

# Define the camera's horizontal field of view
HFOV = 70.0                                 # Horizontal field of view in degrees.

# Color thresholds for grey and black in grayscale
black_threshold = (0, 50)   # Grayscale range for black.
grey_threshold = (51, 200)  # Grayscale range for grey.

while(True):
    img = sensor.snapshot()            # Take a snapshot.

    # Detect circles in the image.
    circles = img.find_circles(threshold=3500, x_margin=10, y_margin=10, r_margin=10, r_min=10, r_max=100, r_step=2)

    for circle in circles:
        # Calculate the mean intensity within the circle
        circle_mask = img.copy(roi=(circle.x()-circle.r(), circle.y()-circle.r(), 2*circle.r(), 2*circle.r()))
        circle_mask.mask_circle(circle.x(), circle.y(), circle.r())
        mean_intensity = circle_mask.get_statistics().mean()

        # Determine the color based on mean intensity
        if mean_intensity < ((black_threshold[0] + black_threshold[1]) / 2):
            color = "black"
        elif mean_intensity < ((grey_threshold[0] + grey_threshold[1]) / 2):
            color = "grey"
        else:
            color = "undefined"

        # Calculate angle from camera center to circle center
        center_x = img.width() // 2
        angle = (circle.x() - center_x) * (HFOV / img.width())

        # Draw the circle on the image
        img.draw_circle(circle.x(), circle.y(), circle.r(), color=127 if color == "grey" else 0)

        # Print out the color, position, radius, and angle of the circle
        print("Detected a {} circle at position ({}, {}), radius {}, angle {:.2f} degrees".format(color, circle.x(), circle.y(), circle.r(), angle))



