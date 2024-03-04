import cv2
import numpy as np

def detect_square(frame, min_area=1000, max_area=5000):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help with contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny edge detector to find edges in the image
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through the contours
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # If the polygon has 4 vertices, it is a rectangle
        if len(approx) == 4:
            # Calculate the aspect ratio of the rectangle
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h

            # Define a threshold for aspect ratio to consider it a square
            aspect_ratio_threshold = 0.9  # Adjust as needed

            if 1 - aspect_ratio_threshold < aspect_ratio < 1 + aspect_ratio_threshold:
                # Calculate the area of the rectangle
                area = cv2.contourArea(approx)

                # Check if the area is within the specified range
                if min_area < area < max_area:
                    # Draw the rectangle on the original frame
                    cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)

                    # Calculate the center of the square
                    center_x = x + w // 2
                    center_y = y + h // 2

                    return center_x, center_y

    # Return None if no square is detected
    return None

# Open a video capture object (you can replace '0' with the video file name)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video feed
    ret, frame = cap.read()

    # Break the loop if no frame is captured
    if not ret:
        break

    # Detect squares in the current frame
    result = detect_square(frame, min_area=500, max_area=10000)

    # Display the result
    if result is not None:
        center_x, center_y = result
        print(f"Square center coordinates: ({center_x}, {center_y})")

    cv2.imshow('Square Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
