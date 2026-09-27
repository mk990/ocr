from paddleocr import PaddleOCR


def create_ocr() -> PaddleOCR:
    return PaddleOCR(
        lang="fa",
        device="cpu",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )


if __name__ == "__main__":
    # Run at image build time to download the models into the image
    create_ocr()
