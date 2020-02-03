import numpy as np
from PIL import Image
import imutils, cv2, sys, traceback, argparse

filename = ""
MODE = "default"
is_show = False
color = (255, 255, 255)

threshold = 0
morphology_size = (1, 1)

parser = argparse.ArgumentParser()
parser.add_argument("--filename")
parser.add_argument("--mode")
parser.add_argument("--color")
parser.add_argument("--show")
parser.add_argument("--threshold")
parser.add_argument("--morphology")
args = parser.parse_args()

if (args.filename and args.color):
    filename = args.filename
    color = tuple(map(int, args.color.split("_")))[:: -1]
    try:
        MODE = args.mode
    except:
        pass
    try:
        if (args.show == "y"): is_show = True
    except:
        pass
    try:
        threshold = int(args.threshold)
    except:
        pass
    try:
        morphology_size = tuple(map(int, args.morphology.split("_")))
    except:
        pass
else:
    try:
        filename = input("Enter filename: ")

        color = tuple(map(int, input("Enter color(in RGB format - red green blue; example - 255 0 0(red)): ").split(" ")))[:: -1]

        MODE = input("Enter mode(default, s_background): ")

        if (input("Do you want to see debug output(image in grayscale, image after threshold processing; y/n)?") == "y"): is_show = True

        is_advanced = input("Do you want to initialize advanced settings(y/n)?")

        if (is_advanced == "y"):
            threshold = int(input("Enter threshold(default 0): "))
            morphology_size = tuple(map(int, input("Enter morphology shapes size(default 1 1): ").split(" ")))

    except:
        print("can't recognize")
        pass

try:
    field = np.array(Image.open(filename))
except FileNotFoundError:
    print("File not found")
    input("Press Enter to exit")
    sys.exit()
except:
    print("Exception catched")
    input("Press Enter to exit")
    sys.exit()

try:

    field = np.array(field, dtype=np.uint8)

    field_colory = field

    field = cv2.cvtColor(field, cv2.COLOR_BGR2GRAY)

    if (is_show):
        cv2.imshow("Grayscale image(press Enter to continue)", field)
        cv2.waitKey()

    field = cv2.adaptiveThreshold(field, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 95, threshold)

    field = cv2.morphologyEx(field, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, morphology_size))

    if (is_show):
        cv2.imshow("Threshold and morphology processing(press Enter to continue)", field)
        cv2.waitKey()

    cnts = cv2.findContours(field.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    result = 0

    if (MODE != "s_background"):
        stencil = np.zeros(field_colory.shape).astype(field_colory.dtype)

        cv2.fillPoly(stencil, cnts, color)
        result = cv2.bitwise_and(field_colory, stencil)
    else:
        result = cv2.cvtColor(field_colory, cv2.COLOR_BGR2RGB)
        cv2.fillPoly(result, cnts, color)
        result = cv2.bitwise_and(cv2.cvtColor(field_colory, cv2.COLOR_BGR2RGB), result)

    cv2.imwrite("result.jpg", result)

    cv2.imshow("Result (press Enter to continue)", result)
    cv2.waitKey()
except:
    print(traceback.format_exc())
    input("Press Enter to exit")
    sys.exit()