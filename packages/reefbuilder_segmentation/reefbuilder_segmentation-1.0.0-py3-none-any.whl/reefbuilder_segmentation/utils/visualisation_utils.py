import cv2


# TODO: Make tabs consistent across code
def draw_bboxes_xyxyn(bboxes, image):
    colors = [(150, 150, 150)]
    drawn_img = image.copy()
    for i, box in enumerate(bboxes):
        x, y, x1, y1 = box
        x, x1 = x * image.shape[1], x1 * image.shape[1]
        y, y1 = y * image.shape[0], y1 * image.shape[0]
        tuple_xy = (int(x), int(y))
        tuple_x1y1 = (int(x1), int(y1))
        cv2.rectangle(drawn_img, tuple_xy, tuple_x1y1, colors[0], 10)
    return drawn_img
