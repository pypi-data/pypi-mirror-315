def programEight():
    """
    WRITE A PROGRAM TO ENHANCE CONTRAST OF AN IMAGE USING HISTOGRAM EQULISATION. DISPLAY THE RESULTS WITH AND WITHOUT
EQUALISATION FOR COMPARISION.
    """
    import cv2
    import matplotlib.pyplot as plt
    from skimage import io
    # Load image and perform histogram equalization
    image = io.imread('car.jpg')
    equalized_image = cv2.merge([cv2.equalizeHist(channel) for channel in cv2.split(image)])
    # Display original and equalized images
    titles = ['Original Image', 'Equalized Image']
    images = [image, equalized_image]
    plt.figure(figsize=(12, 6))
    for i, img in enumerate(images):
        plt.subplot(1, 2, i + 1)
        plt.title(titles[i])
        plt.imshow(img)
        plt.axis('off')
    plt.tight_layout()
    plt.show()