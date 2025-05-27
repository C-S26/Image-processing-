import cv2

def apply_multi_region_blur(image):
    regions = []
    clone = image.copy()

    def draw_rectangle(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            regions.append((x, y))
        elif event == cv2.EVENT_LBUTTONUP:
            x1, y1 = regions[-1]
            x2, y2 = x, y
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])
            if x2 - x1 > 0 and y2 - y1 > 0:
                regions[-1] = (x1, y1, x2, y2)
                cv2.rectangle(clone, (x1, y1), (x2, y2), (0, 255, 0), 2)
            else:
                regions.pop()

    cv2.namedWindow("Select Blur Regions (Press Enter to confirm)")
    cv2.setMouseCallback("Select Blur Regions (Press Enter to confirm)", draw_rectangle)

    while True:
        cv2.imshow("Select Blur Regions (Press Enter to confirm)", clone)
        if cv2.waitKey(1) & 0xFF == 13:
            break

    for (x1, y1, x2, y2) in regions:
        roi = image[y1:y2, x1:x2]
        if roi.size != 0:
            blurred = cv2.GaussianBlur(roi, (51, 51), 30)
            image[y1:y2, x1:x2] = blurred

    cv2.destroyWindow("Select Blur Regions (Press Enter to confirm)")
    return image

def apply_freehand_blur(image):
    drawing = False
    mask = image.copy() * 0  # same shape, black mask

    def draw(event, x, y, flags, param):
        nonlocal drawing
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            cv2.circle(mask, (x, y), 20, (255, 255, 255), -1)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False

    cv2.namedWindow("Draw Freehand to Blur (ESC to finish)")
    cv2.setMouseCallback("Draw Freehand to Blur (ESC to finish)", draw)

    while True:
        preview = cv2.addWeighted(image, 1, mask, 0.3, 0)
        cv2.imshow("Draw Freehand to Blur (ESC to finish)", preview)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    blurred = cv2.GaussianBlur(image, (51, 51), 30)
    mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    mask_inv = cv2.bitwise_not(mask_gray)

    fg = cv2.bitwise_and(blurred, blurred, mask=mask_gray)
    bg = cv2.bitwise_and(image, image, mask=mask_inv)
    result = cv2.add(fg, bg)

    cv2.destroyWindow("Draw Freehand to Blur (ESC to finish)")
    return result


def apply_redaction(image):
    redactions = []
    clone = image.copy()

    def draw_box(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            redactions.append((x, y))
        elif event == cv2.EVENT_LBUTTONUP:
            x1, y1 = redactions[-1]
            x2, y2 = x, y
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])
            if x2 - x1 > 0 and y2 - y1 > 0:
                redactions[-1] = (x1, y1, x2, y2)
                cv2.rectangle(clone, (x1, y1), (x2, y2), (0, 0, 0), -1)
            else:
                redactions.pop()

    cv2.namedWindow("Select Redaction Areas (Enter to apply)")
    cv2.setMouseCallback("Select Redaction Areas (Enter to apply)", draw_box)

    while True:
        cv2.imshow("Select Redaction Areas (Enter to apply)", clone)
        if cv2.waitKey(1) & 0xFF == 13:
            break

    for (x1, y1, x2, y2) in redactions:
        image[y1:y2, x1:x2] = (0, 0, 0)

    cv2.destroyWindow("Select Redaction Areas (Enter to apply)")
    return image

def apply_crop(image):
    r = cv2.selectROI("Crop Image", image, showCrosshair=True)
    if r != (0, 0, 0, 0):
        x, y, w, h = r
        cropped = image[int(y):int(y + h), int(x):int(x + w)]
        cv2.destroyWindow("Crop Image")
        return cropped
    cv2.destroyWindow("Crop Image")
    return image
