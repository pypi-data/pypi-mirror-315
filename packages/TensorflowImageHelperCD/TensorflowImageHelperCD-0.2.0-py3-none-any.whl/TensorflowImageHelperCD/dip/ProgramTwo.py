


def programTwo():
    """
    Read an image and extract and display low-level features such as edges, textures using filtering techniques
    """
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    # Gaussian blur function
    def apply_gaussian_blur(image, kernel_size):
        kernel = cv2.getGaussianKernel(kernel_size, -1)
        return cv2.filter2D(image, -1, np.outer(kernel, kernel))

    # Sobel edge detection function
    def detect_edges_sobel(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        return np.clip(cv2.magnitude(grad_x, grad_y), 0, 255).astype(np.uint8)
    # Load, blur, and detect edges
    image = cv2.imread('car.jpg')
    blurred_image = apply_gaussian_blur(image, 11)
    edges = detect_edges_sobel(blurred_image)
    # Display images
    titles = ['Original Image', 'Blurred Image', 'Sobel Edges']
    images = [image, blurred_image, edges]
    plt.figure(figsize=(15, 5))
    for i, img in enumerate(images):
        plt.subplot(1, 3, i + 1)
    plt.imshow(img if i < 2 else img, cmap='gray' if i == 2 else None)
    plt.title(titles[i])
    plt.axis('off')
    plt.tight_layout()
    plt.show()
