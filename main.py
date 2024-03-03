"""The script is utilizing file system paths and directories to facilitate the training and evaluation of a deep learning model,
specifically a UNET-based architecture for the segmentation of glioblastoma multiforme, a highly malignant form of brain cancer.
These file paths are programmatically assigned to specific directories on the researcher's local machine,
including the location of the data slices and the location of the pre-trained UNET model.
Moreover, these file paths are utilized to specify the locations of the
training, validation, and testing sets for both the images and corresponding masks.
Furthermore, the script also defines the location for storing the output generated by the prediction generator,
as well as the location of the volume image and mask datasets.
These file paths will be utilized eventually in the script for loading the data and model,
as well as saving the output from the model."""


import os
import imageio
import matplotlib.pyplot as plt
import numpy as np
import plotly
import plotly.graph_objs as go
import seaborn as sns
from PIL import Image
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from plotly.subplots import make_subplots
from skimage.filters import threshold_otsu
from skimage.io import imread
from skimage.measure import marching_cubes
from skimage.morphology import opening
from tensorflow import keras


dataDirectory = r"C:\Users\kpr18\Desktop\Model Dataset\Slices"
modelPath = r"C:\Users\kpr18\Desktop\Model Dataset\Glioblastoma Multiforme UNET-Segmentation Model.h5"


dataDirectoryTrain = os.path.join(dataDirectory, 'Training')
dataDirectoryTrainImage = os.path.join(dataDirectoryTrain, 'Image')
dataDirectoryTrainMask = os.path.join(dataDirectoryTrain, 'Mask')


dataDirectoryValidation = os.path.join(dataDirectory, 'Validation')
dataDirectoryValidationImage = os.path.join(dataDirectoryValidation, 'Image')
dataDirectoryValidationMask = os.path.join(dataDirectoryValidation, 'Mask')


dataDirectoryTest = os.path.join(dataDirectory, 'Testing')
dataDirectoryTestImage = os.path.join(dataDirectoryTest, 'Image')
dataDirectoryTestMask = os.path.join(dataDirectoryTest, 'Mask')


predictionGeneratorOutputPath = r"C:\Users\kpr18\Pictures\2022-23 ISEF"
volumeImageDataset = r"C:\Users\kpr18\Desktop\Model Dataset\Volumes\Image"
volumeMaskDataset = r"C:\Users\kpr18\Desktop\Model Dataset\Volumes\Mask"










"""MODEL PRE-PROCESSING:"""
"""The script presented contains a suite of functions for performing data preprocessing tasks,
specifically tailored for facilitating the training and evaluation of a deep learning model.
The first function, named "Mask_Creator", takes as input the file system path to a directory containing the raw data,
and the file system path to a directory where the processed data will be written.
The function iterates over all files in the input directory,
utilizing the "imread" function from the scikit-image library to read the image data.
Also, an Otsu thresholding algorithm is applied to the image data, resulting in a binary mask.
This mask is then cast to a numeric data type, and written to the specified output directory, with a modified file extension.
The second function, "Image_Resizer", takes as input the file system path to a directory containing the raw data,
and the desired width and height of the output images. The function iterates over all files in the input directory,
utilizing the PIL library to open each file, and resize the image to the specified width and height.
The resized image is then written back to the input directory, with the same file name.
The third function "grayscaleConverter" takes as input the file system path to a directory containing the raw data.
The function iterates over all files in the input directory, utilizing the PIL library to open each file,
and then converts the image to grayscale. The grayscale image is then written back to the input directory, with the same file name.
The fourth function, "modelPreProcessing", takes several parameters,
including the file system paths to the directories containing the training and validation images and masks.
This function utilizes the ImageDataGenerator class from the Keras library to instantiate generator objects for the training,
validation and testing sets, with a specified target size and color mode.
These generator objects are then returned from the function to be used in the training and evaluation of the deep learning model."""


def Mask_Creator(inputDirectory, outputDirectory):
  for file in os.listdir(inputDirectory):
      filePath = os.path.join(inputDirectory, file)
      dicomImage = imread(filePath)
      threshold = threshold_otsu(dicomImage)
      mask = dicomImage > threshold
      numericMask = mask.astype(int)
      outputPath = os.path.join(outputDirectory, file[:-4] + "-Mask.png")
      imageio.imwrite(outputPath, numericMask)


# Mask_Creator(inputDirectory=r"C:\Users\kpr18\Desktop\manifest-1672690264629\UPENN-GBM\UPENN-GBM-00009\09-01-2002-NA-MRI BRAIN WINJMHDI-53314\DICOM Dataset",
#              outputDirectory=r"C:\Users\kpr18\Desktop\Model Dataset\Volumes")


def Image_Resizer(directory, width, height):
  for filename in os.listdir(directory):
      image = Image.open(f'{directory}/{filename}')
      size = (width, height)
      image = image.resize(size)
      width, height = image.size
      print(f'Width: {width}, Height: {height}')
      image.save(f'{directory}/{filename}')


# Image_Resizer(directory=r"C:\Users\kpr18\Desktop\Model Dataset\Slices\Validation\Mask\Files",
#               width=375,
#               height=425)


def grayscaleConverter(directoryPath):
   for filename in os.listdir(directoryPath):
       file_path = os.path.join(directoryPath, filename)
       image = Image.open(file_path).convert('L')
       image.save(file_path)


# grayscaleConverter(directoryPath=r"C:\Users\kpr18\Desktop\Model Dataset\Volumes")


def modelPreProcessing(dataDirectoryTrainImage, dataDirectoryTrainMask, dataDirectoryTestImage, dataDirectoryTestMask, dataDirectoryValidationImage, dataDirectoryValidationMask):
   datagen = ImageDataGenerator(rescale=1./255)


   trainImageGenerator = datagen.flow_from_directory(dataDirectoryTrainImage, target_size=(425, 375), batch_size=2, color_mode='grayscale', class_mode=None)
   trainMaskGenerator = datagen.flow_from_directory(dataDirectoryTrainMask, target_size=(425, 375), batch_size=2, color_mode='grayscale', class_mode=None)


   imageValidationGenerator = datagen.flow_from_directory(dataDirectoryValidationImage, target_size=(425, 375), batch_size=2, color_mode='grayscale', class_mode=None)
   maskValidationGenerator = datagen.flow_from_directory(dataDirectoryValidationMask, target_size=(425, 375), batch_size=2, color_mode='grayscale', class_mode=None)


   testImageGenerator = datagen.flow_from_directory(dataDirectoryTestImage, target_size=(425, 375), batch_size=2, color_mode='grayscale', class_mode=None)
   testMaskGenerator = datagen.flow_from_directory(dataDirectoryTestMask, target_size=(425, 375), batch_size=2, color_mode='grayscale', class_mode=None)


   trainGenerator = zip(trainImageGenerator, trainMaskGenerator)
   validationGenerator = zip(imageValidationGenerator, maskValidationGenerator)
   testGenerator = zip(testImageGenerator, testMaskGenerator)


   return trainGenerator, validationGenerator, testGenerator


trainGenerator, validationGenerator, testGenerator = modelPreProcessing(dataDirectoryTrainImage=dataDirectoryTrainImage,
                                                                       dataDirectoryTrainMask=dataDirectoryTrainMask,
                                                                       dataDirectoryTestImage=dataDirectoryTestImage,
                                                                       dataDirectoryTestMask=dataDirectoryTestMask,
                                                                       dataDirectoryValidationImage=dataDirectoryValidationImage,
                                                                       dataDirectoryValidationMask=dataDirectoryValidationMask)










"""UNET MODEL TRAINING AND EVALUATION"""
"""This script defines a function for constructing a UNET architecture,
which is a variant of convolutional neural network (CNN) designed for image segmentation tasks.
The function takes several parameters, including the input shape, number of classes,
generator objects for training, validation and testing, and the file path for saving the model.
The function initiates by instantiating the input layer using the keras.Input() function,
which takes the input_shape parameter as an argument.
Then, it creates a series of convolutional layers with rectified linear unit (ReLU) activation function,
each followed by a max pooling layer to reduce the spatial dimensions of the feature maps.
Each of these layers also utilizes the kernel initializer 'he_normal' for the weights initialization
and padding='same' to preserve the same spatial dimension as the input.
The function then constructs up-sampling layers to increase the spatial dimensions,
which are concatenated with the corresponding feature maps from the encoder path.
This process is iteratively repeated multiple times, resulting in several upsampling and concatenation layers.
Finally, the last layer is a convolutional layer with a sigmoid activation function,which will output the segmentation mask.
The function also incorporates dropout layers to mitigate overfitting.
Additionally, the function saves the model at the location specified by the modelPath parameter."""


def unetModel(input_shape, num_classes, trainGenerator, validationGenerator, testGenerator, modelPath):
   inputs = keras.Input(shape=input_shape)


   conv1 = keras.layers.Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(inputs)
   conv1 = keras.layers.Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv1)
   pool1 = keras.layers.MaxPooling2D(pool_size=(2, 2))(conv1)


   conv2 = keras.layers.Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool1)
   conv2 = keras.layers.Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv2)
   pool2 = keras.layers.MaxPooling2D(pool_size=(2, 2))(conv2)


   conv3 = keras.layers.Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool2)
   conv3 = keras.layers.Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv3)
   pool3 = keras.layers.MaxPooling2D(pool_size=(2, 2))(conv3)
   conv4 = keras.layers.Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool3)
   conv4 = keras.layers.Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv4)
   drop4 = keras.layers.Dropout(0.5)(conv4)
   pool4 = keras.layers.MaxPooling2D(pool_size=(2, 2))(drop4)


   up5 = keras.layers.UpSampling2D(size=(2, 2))(pool4)
   up5 = keras.layers.ZeroPadding2D(padding=((0, 1), (0, 0)))(up5)
   merge5 = keras.layers.concatenate([drop4, up5], axis=3)
   conv5 = keras.layers.Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge5)
   conv5 = keras.layers.Conv2D(512, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv5)


   up6 = keras.layers.Conv2D(256, 2, activation='relu', padding='same', kernel_initializer='he_normal')(keras.layers.UpSampling2D(size=(2, 2))(conv5))
   up6 = keras.layers.ZeroPadding2D(padding=((0, 0), (0, 1)))(up6)
   merge6 = keras.layers.concatenate([conv3, up6], axis=3)
   conv6 = keras.layers.Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge6)
   conv6 = keras.layers.Conv2D(256, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv6)
   up7 = keras.layers.Conv2D(128, 2, activation='relu', padding='same', kernel_initializer='he_normal')(keras.layers.UpSampling2D(size=(2, 2))(conv6))
   up7 = keras.layers.ZeroPadding2D(padding=((0, 0), (0, 1)))(up7)
   merge7 = keras.layers.concatenate([conv2, up7], axis=3)
   conv7 = keras.layers.Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge7)
   conv7 = keras.layers.Conv2D(128, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv7)


   up8 = keras.layers.Conv2D(64, 2, activation='relu', padding='same', kernel_initializer='he_normal')(keras.layers.UpSampling2D(size=(2, 2))(conv7))
   up8 = keras.layers.ZeroPadding2D(padding=((0, 1), (0, 1)))(up8)
   merge8 = keras.layers.concatenate([conv1, up8], axis=3)
   conv8 = keras.layers.Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge8)
   conv8 = keras.layers.Conv2D(64, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv8)


   conv9 = keras.layers.Conv2D(num_classes, 1, activation='sigmoid')(conv8)
   model = keras.Model(inputs=inputs, outputs=conv9)
   model.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-4), loss='binary_crossentropy', metrics=['accuracy'])
   history = model.fit(trainGenerator,
                       steps_per_epoch=10,
                       validation_data=validationGenerator,
                       validation_steps=5,
                       epochs=50)
   model.save(modelPath)
   print(model.summary())


   loss, accuracy = model.evaluate(testGenerator, steps=25)
   print(f'Test loss: {loss:.4f}')
   print(f'Test accuracy: {accuracy:.4f}')


   sns.set()
   plt.plot(history.history['loss'])
   plt.plot(history.history['val_loss'])
   plt.plot(history.history['accuracy'])
   plt.plot(history.history['val_accuracy'])
   plt.title('Model Performance')
   plt.ylabel('Loss / Accuracy')
   plt.xlabel('Epoch')
   plt.legend(['Loss', 'Validation Loss', 'Accuracy', 'Validation Accuracy'], loc='lower right')
   plt.show()


# unetModel(input_shape=(425, 375, 1),
#           num_classes=1,
#           trainGenerator=trainGenerator,
#           validationGenerator=validationGenerator,
#           testGenerator=testGenerator,
#           modelPath=modelPath)










"""MODEL PREDICTION AND 3D-VISUALIZATION"""
"""The presented code consists of two distinct functions, predictionGenerator and volumeVisualization,
that serve the purpose of visualizing the performance of a pre-trained deep learning model on a specific task.
The predictionGenerator function takes three parameters as inputs:
the number of plots to generate, the file path to the pre-trained model, and the directory path for the output plots.
The function begins by instantiating the pre-trained model using the load_model function from the keras.models module.
Next, an instance of the ImageDataGenerator class is created, which serves to preprocess the input images.
Two data generators are defined, one for the test image dataset and one for the test mask dataset,
both with a target size of (425,375) and a batch size of 2, and both in grayscale.
These generators are then "zipped" together and a for loop is used to iterate the specified number of times.
On each iteration, the next test image-mask pair is obtained from the generator,
and the model is employed to make a prediction on the test image.
A helper function, named removeBlur, is defined which uses the opening function from the skimage.morphology module
to remove blur from the image. The first image and mask from the batch, as well as the first prediction from the batch, are then extracted.
Finally, using the matplotlib.pyplot module, three subplots are created, one for the original scan, one for the ground truth mask,
and one for the model-predicted mask. The resulting figure is saved to the specified output directory.
The volumeVisualization function takes one parameter as input, the file path to the pre-trained model,
which is used to instantiate the model in a similar fashion as the predictionGenerator function.
Similarly, an instance of the ImageDataGenerator class is created,
and two generators are defined for the volume image dataset and volume mask dataset.
A for loop is used to iterate 192 times, and on each iteration,
the next volume image-mask pair is obtained from the generator and the model is employed to make a prediction.
The predictions are appended to a list, which is then used to create a 3D volume using the numpy.stack function.
The marching_cubes function from the skimage.measure module is then utilized to extract an iso-surface from the volume,
and the plotly.graph_objects module is employed to create a 3D mesh plot of the iso-surface, which is saved as an HTML file."""


def predictionGenerator(numPlots, modelPath, outputDirectory):
   model = load_model(modelPath)
   datagen = ImageDataGenerator(rescale=1. / 255)
   testImageGenerator = datagen.flow_from_directory(dataDirectoryTestImage, target_size=(425, 375), batch_size=2, color_mode='grayscale', class_mode=None, shuffle=False)
   testMaskGenerator = datagen.flow_from_directory(dataDirectoryTestMask, target_size=(425, 375), batch_size=2, color_mode='grayscale', class_mode=None, shuffle=False)
   testGenerator = zip(testImageGenerator, testMaskGenerator)
   for i in range(numPlots):
       testImage, testMask = next(testGenerator)
       testPrediction = model.predict(testImage)


       def removeBlur(inputImage, kernel_size=(3, 3)):
           return opening(inputImage, footprint=np.ones(kernel_size))


       image = testImage[0, :, :, 0]
       mask = testMask[0, :, :, 0]
       prediction = removeBlur(testPrediction[0, :, :, 0], kernel_size=(3, 3))


       plt.figure(figsize=(20, 10))
       plt.subplot(1, 3, 1)
       plt.imshow(image, cmap='gray')
       plt.title("Original Scan")


       plt.subplot(1, 3, 2)
       plt.imshow(mask, cmap='gray')
       plt.title("Ground Truth Mask")


       plt.subplot(1, 3, 3)
       plt.imshow(prediction, cmap='gray')
       plt.title("Model-Predicted Mask")


       plt.savefig(outputDirectory + r"\predictionGenerator() - " + str(i + 1) + ".jpg")


# predictionGenerator(numPlots=50,
#                     modelPath=modelPath,
#                     outputDirectory=predictionGeneratorOutputPath)




def volumeVisualization(modelPath):
   model = load_model(modelPath)
   datagen = ImageDataGenerator(rescale=1. / 255)
   volumeImageGenerator = datagen.flow_from_directory(volumeImageDataset, target_size=(425, 375), batch_size=1, color_mode='grayscale', class_mode=None, shuffle=False)
   volumeMaskGenerator = datagen.flow_from_directory(volumeMaskDataset, target_size=(425, 375), batch_size=1, color_mode='grayscale', class_mode=None, shuffle=False)
   volumeGenerator = zip(volumeImageGenerator, volumeMaskGenerator)


   predictions = []
   for i in range(192):
       volumeImage, volumeMask = next(volumeGenerator)
       volumePrediction = model.predict(volumeImage)
       predictions.append(volumePrediction[0, :, :, 0])
   volume = np.stack(predictions, axis=2)
   vertices, faces, normals, values = marching_cubes(volume, level=0.5)


   fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'mesh3d'}]])
   fig.add_trace(go.Mesh3d(x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2], i=faces[:, 0], j=faces[:, 1], k=faces[:, 2], color='lightpink'))
   fig.update_layout(scene=dict(aspectmode='data'))
   plotly.offline.plot(fig, filename=r"C:\Users\kpr18\Pictures\2022-23 ISEF\Glioblastoma Multiforme.html", auto_open=False)


# volumeVisualization(modelPath=modelPath)