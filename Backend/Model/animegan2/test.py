from converter import convert

def main():
    input_image = './samples/inputs/image(1).jpg'  # 입력 이미지 경로
    output_image = './samples/results/image(1).jpg'  # 출력 이미지 경로

    # 이미지 변환 함수 호출
    convert(input_image, output_image)

if __name__ == "__main__":
    main()