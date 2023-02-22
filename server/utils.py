import cv2
import numpy as np


def box_label(
    image: np.ndarray,
    box: tuple,
    label: str = "",
    color: tuple = (128, 128, 128),
    txt_color: tuple = (255, 255, 255),
) -> None:
    """Draw a bounding box with label
    Args:
        - image (np.ndarray): image to draw on
        - box (list): bounding box in xyxy format
        - label (str): label to draw
        - color (tuple): color to draw bounding box
        - txt_color (tuple): color to draw label

    """
    print(type(image))
    print(image.shape)
    image = np.ascontiguousarray(image, dtype=np.uint8)
    lw = max(round(sum(image.shape) / 2 * 0.003), 2)
    print(lw)
    p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
    cv2.rectangle(image, p1, p2, color, thickness=lw, lineType=cv2.LINE_AA)
    if label:
        tf = max(lw - 1, 1)  # font thickness
        w, h = cv2.getTextSize(label, 0, fontScale=lw / 3, thickness=tf)[
            0
        ]  # text width, height
        outside = p1[1] - h >= 3
        p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
        cv2.rectangle(image, p1, p2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(
            image,
            label,
            (p1[0], p1[1] - 2 if outside else p1[1] + h + 2),
            0,
            lw / 3,
            txt_color,
            thickness=tf,
            lineType=cv2.LINE_AA,
        )


def plot_bboxes(
    image: np.ndarray,
    boxes: tuple,
    labels: list = [],
    colors: list = [],
    masks: tuple = None,
    score=True,
    conf: float = None,
) -> np.ndarray:
    """Draw bounding boxes and masks on image
    Args:
        image (np.ndarray): image to draw on
        boxes (list): list of bounding boxes in xyxy format
        labels (list): list of labels
        colors (list): list of colors
        score (bool): whether to draw score
        masks (list): list of masks
        conf (float): confidence threshold
        Returns:
            np.ndarray: image with bounding boxes
    """
    # Define COCO Labels
    if labels == []:
        labels = {
            0: "__background__",
            1: "person",
            2: "bicycle",
            3: "car",
            4: "motorcycle",
            5: "airplane",
            6: "bus",
            7: "train",
            8: "truck",
            9: "boat",
            10: "traffic light",
            11: "fire hydrant",
            12: "stop sign",
            13: "parking meter",
            14: "bench",
            15: "bird",
            16: "cat",
            17: "dog",
            18: "horse",
            19: "sheep",
            20: "cow",
            21: "elephant",
            22: "bear",
            23: "zebra",
            24: "giraffe",
            25: "backpack",
            26: "umbrella",
            27: "handbag",
            28: "tie",
            29: "suitcase",
            30: "frisbee",
            31: "skis",
            32: "snowboard",
            33: "sports ball",
            34: "kite",
            35: "baseball bat",
            36: "baseball glove",
            37: "skateboard",
            38: "surfboard",
            39: "tennis racket",
            40: "bottle",
            41: "wine glass",
            42: "cup",
            43: "fork",
            44: "knife",
            45: "spoon",
            46: "bowl",
            47: "banana",
            48: "apple",
            49: "sandwich",
            50: "orange",
            51: "broccoli",
            52: "carrot",
            53: "hot dog",
            54: "pizza",
            55: "donut",
            56: "cake",
            57: "chair",
            58: "couch",
            59: "potted plant",
            60: "bed",
            61: "dining table",
            62: "toilet",
            63: "tv",
            64: "laptop",
            65: "mouse",
            66: "remote",
            67: "keyboard",
            68: "cell phone",
            69: "microwave",
            70: "oven",
            71: "toaster",
            72: "sink",
            73: "refrigerator",
            74: "book",
            75: "clock",
            76: "vase",
            77: "scissors",
            78: "teddy bear",
            79: "hair drier",
            80: "toothbrush",
        }
    # Define colors
    if colors == []:
        colors = [
            (89, 161, 197),
            (67, 161, 255),
            (19, 222, 24),
            (186, 55, 2),
            (167, 146, 11),
            (190, 76, 98),
            (130, 172, 179),
            (115, 209, 128),
            (204, 79, 135),
            (136, 126, 185),
            (209, 213, 45),
            (44, 52, 10),
            (101, 158, 121),
            (179, 124, 12),
            (25, 33, 189),
            (45, 115, 11),
            (73, 197, 184),
            (62, 225, 221),
            (32, 46, 52),
            (20, 165, 16),
            (54, 15, 57),
            (12, 150, 9),
            (10, 46, 99),
            (94, 89, 46),
            (48, 37, 106),
            (42, 10, 96),
            (7, 164, 128),
            (98, 213, 120),
            (40, 5, 219),
            (54, 25, 150),
            (251, 74, 172),
            (0, 236, 196),
            (21, 104, 190),
            (226, 74, 232),
            (120, 67, 25),
            (191, 106, 197),
            (8, 15, 134),
            (21, 2, 1),
            (142, 63, 109),
            (133, 148, 146),
            (187, 77, 253),
            (155, 22, 122),
            (218, 130, 77),
            (164, 102, 79),
            (43, 152, 125),
            (185, 124, 151),
            (95, 159, 238),
            (128, 89, 85),
            (228, 6, 60),
            (6, 41, 210),
            (11, 1, 133),
            (30, 96, 58),
            (230, 136, 109),
            (126, 45, 174),
            (164, 63, 165),
            (32, 111, 29),
            (232, 40, 70),
            (55, 31, 198),
            (148, 211, 129),
            (10, 186, 211),
            (181, 201, 94),
            (55, 35, 92),
            (129, 140, 233),
            (70, 250, 116),
            (61, 209, 152),
            (216, 21, 138),
            (100, 0, 176),
            (3, 42, 70),
            (151, 13, 44),
            (216, 102, 88),
            (125, 216, 93),
            (171, 236, 47),
            (253, 127, 103),
            (205, 137, 244),
            (193, 137, 224),
            (36, 152, 214),
            (17, 50, 238),
            (154, 165, 67),
            (114, 129, 60),
            (119, 24, 48),
            (73, 8, 110),
        ]

    mask_image = np.zeros_like(image)

    # plot each boxes
    for i, box in enumerate(boxes):
        # add score in label if score=True
        if score:
            label = (
                labels[int(box[-1]) + 1]
                + " "
                + str(round(100 * float(box[-2]), 1))
                + "%"
            )
        else:
            label = labels[int(box[-1]) + 1]
        # filter every box under conf threshold if conf threshold setted
        if conf:
            if box[-2] > conf:
                color = colors[int(box[-1])]
                box_label(image, box, label, color)

                if masks is not None:
                    mask = masks[i]
                    if len(mask.shape) == 3:
                        mask = mask[..., 0]  # take first channel if multi-channel mask
                    mask = (mask * 255).cpu().numpy().astype(np.uint8)
                    alpha = 0.5  # adjust transparency here
                    color_mask = np.zeros_like(image)
                    color_mask[:, :, :] = color
                    masked_image = cv2.bitwise_and(color_mask, color_mask, mask=mask)
                    mask_image = cv2.addWeighted(
                        masked_image, alpha, mask_image, 1 - alpha, 0
                    )
        else:
            color = colors[int(box[-1])]
            box_label(image, box, label, color)

        # combine original image with mask image
    image = cv2.addWeighted(image, 1, mask_image, 1, 0)

    return image
