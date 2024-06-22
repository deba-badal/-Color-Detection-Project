import cv2
import pandas as pd

# Paths to the image and CSV file
img_path = 'pic2.jpg'
csv_path ='C:\\Users\\debas\\Downloads'

# Reading the CSV file into a pandas DataFrame
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

# Reading the image using OpenCV
img = cv2.imread(img_path)
img = cv2.resize(img, (800, 600))  # Resize the image to 800x600 pixels

# Declaring global variables
clicked = False  # Flag to check if the mouse was clicked
r = g = b = xpos = ypos = 0  # Variables to store RGB values and mouse click positions

# Function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 1000
    for i in range(len(df)):
        # Calculate the distance between the input color and colors in the DataFrame
        d = abs(R - int(df.loc[i, 'R'])) + abs(G - int(df.loc[i, 'G'])) + abs(B - int(df.loc[i, 'B']))
        if d <= minimum:
            minimum = d
            cname = df.loc[i, 'color_name']  # Get the color name with the minimum distance

    return cname

# Function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True  # Set the clicked flag to True
        xpos = x  # Get the x coordinate of the mouse click
        ypos = y  # Get the y coordinate of the mouse click
        b, g, r = img[y, x]  # Get the BGR values of the pixel where the mouse was clicked
        b = int(b)  # Convert B value to integer
        g = int(g)  # Convert G value to integer
        r = int(r)  # Convert R value to integer

# Creating a window to display the image
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)  # Set the callback function for mouse events

# Main loop to display the image and handle events
while True:
    cv2.imshow('image', img)  # Display the image in the window
    if clicked:
        # Draw a rectangle to display the color and its name
        cv2.rectangle(img, (20, 20), (600, 60), (b, g, r), -1)

        # Create text string to display the color name and RGB values
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        
        # Display the text string on the image
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colors, display text in black color
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    # Break the loop when the 'Esc' key is pressed
    if cv2.waitKey(20) & 0xFF == 27:
        break

# Destroy all OpenCV windows
cv2.destroyAllWindows()
