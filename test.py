import base64
import io

def encode_image_to_base64(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string

# 사용 예시
image_path = 'generated_image.png'  # 이 부분에 이미지 파일 경로를 넣으세요
encoded_image = encode_image_to_base64(image_path)
print(encoded_image)
