import csv
import cv2

# img_path = r'F:\Python_Project_Color_Detection\images\colorPalettes.jpg''
# img = cv2.imread(img_path)
cam = cv2.VideoCapture(0)

# declaring global variables (are used later on)
# clicked = False
r = g = b = x_pos = y_pos = 0

# Reading csv file with pandas and giving names to each column
# index = ["color", "color_name", "hex", "R", "G", "B"]
# csv = pd.read_csv('colors.csv', names=index, header=None)
colors = []
with open('colors.csv', 'r') as csv_file:
    csvreader = csv.reader(csv_file)
    for row in csvreader:
        color_info = {
            "color_name": row[1],
            "hex": row[2],
            "R": int(row[3]),
            "G": int(row[4]),
            "B": int(row[5])
        }
        colors.append(color_info)

# function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 10000
    for i in colors:
        d = abs(R - i["R"]) + abs(G - i["G"]) + abs(B - i["B"])

        if d <= minimum:
            minimum = d
            cname = i["color_name"] + '   Hex=' + i["hex"]
    return cname


# Function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos
        x_pos = x
        y_pos = y
        b, g, r = frame[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:

    (grabbed, frame) = cam.read()
    frame = cv2.resize(frame, (900, frame.shape[0]))

    # cv2.rectangle(image, start point, endpoint, color, thickness)-1 fills entire rectangle
    cv2.rectangle(frame, (20, 20), (750, 60), (b, g, r), -1)

    # Creating text string to display( Color name and RGB values )
    text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

    # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
    cv2.putText(frame, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    # For very light colours we will display text in black colour
    if r + g + b >= 600:
        cv2.putText(frame, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow('image', frame)

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()