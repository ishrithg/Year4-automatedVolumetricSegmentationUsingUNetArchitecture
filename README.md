# Automatic Volumetric Segmentation Through the Implementation of UNET Architecture
**This project segments glioblastoma brain tumors from MRI scans using a deep learning model.**

**Data**
- The data consists of MRI slices and segmentations of glioblastoma tumors
- It is split into training, validation, and test sets
- Images are preprocessed by resizing, converting to grayscale etc.
  
**Model Architecture**
- A UNet architecture is built using Keras
- It has convolutional and upsampling layers
- Sigmoid activation is used for binary segmentation
- Model is compiled with binary cross-entropy loss
  
**Training**
- Model is trained for 50 epochs with early stopping
- Training and validation generators are used
- Learning curves plot model convergence
  
**Prediction and Visualization**
- Model makes predictions on test MRI slices
- 3D volume is constructed from slice predictions
- Marching cubes algorithm extracts tumor surface
- 3D mesh plot is generated for visualization
  
The pipeline demonstrates how deep learning and 3D graphics can be combined for medical imaging tasks. Accurate segmentation is important for analyzing tumor shape and size.

**Usage**

**To apply the model to new data:**
- Prepare MRI slices and segmentations
- Preprocess images as done in training
- Pass slices through trained model
- Construct 3D volume and visualize
  
**The model outputs precise glioblastoma tumor segmentations from MRI scans, enabling downstream analysis.**
