from converter import convert

def main():
    input_image_path = './images/inputs/image(1).jpg'  # Input image path
    output_image_path = './images/results/image(1).jpg'  # Output image path

    # Call the image conversion function
    convert(input_image_path, output_image_path)

if __name__ == "__main__":
    main()