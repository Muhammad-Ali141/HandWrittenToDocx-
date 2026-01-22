from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_angle_cls=True,
    lang='en',
    rec=True
)

def extract_text(image_path):
    result = ocr.ocr(image_path, cls=True)

    extracted_text = []
    for line in result:
        for word in line:
            extracted_text.append(word[1][0])

    return "\n".join(extracted_text)
