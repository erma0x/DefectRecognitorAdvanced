import cv2 as cv

image = cv.imread(cv.samples.findFile(args.input))
if image is None:
    print('Could not open or find the image: ', args.input)
    exit(0)

alpha = 1.0 # Simple contrast control
beta = 0    # Simple brightness control
# Initialize values
print(' Basic Linear Transforms ')
print('-------------------------')
try:
    alpha = float(input('* Enter the alpha value [1.0-3.0]: '))
    beta = int(input('* Enter the beta value [0-100]: '))
except ValueError:
    print('Error, not a number')


for c in range(image.shape[2]):
    new_image[y,x,c] = np.clip(alpha*image[y,x,c] + beta, 0, 255)

# Show stuff
cv.imshow('Original Image', image)
cv.imshow('New Image', new_image)
# Wait until user press some key
cv.waitKey()

new_image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)