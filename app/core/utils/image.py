from PIL import ImageFile
import base64
import io

def from_image_to_bytes(image: ImageFile.ImageFile) -> bytes:
    """
    pillow image 객체를 bytes로 변환
    """
    # Pillow 이미지 객체를 Bytes로 변환
    imageByteArr = io.BytesIO()
    image.save(imageByteArr, format=image.format)
    imageByteArr = imageByteArr.getvalue()
    # Base64로 Bytes를 인코딩
    encoded = base64.b64encode(imageByteArr)
    # Base64로 ascii로 디코딩
    decoded = encoded.decode('ascii')
    return decoded