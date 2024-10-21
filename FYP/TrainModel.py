# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 14:07:12 2024

@author: uzair
"""

import tensorflow as tf
import cv2
import numpy as np
import os
import pathlib
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, LearningRateScheduler
from tensorflow.keras.layers import TimeDistributed, Conv2D, MaxPooling2D, Flatten, LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential

# Parameters
frameHeight, frameWidth = 128, 128
numFrames = 16
batchSize = 64
numClasses = 101

# Directory 
dataDir = pathlib.Path("C:/Users/uzair/OneDrive/Desktop/FinalYrProject/UCF-101")

# Function to apply augmentation to each frame of the video
def augmentVideo(video):
    video = tf.image.random_brightness(video, max_delta=0.1)
    video = tf.image.random_flip_left_right(video)
    video = tf.image.random_contrast(video, lower=0.2, upper=1.8)
    video = tf.image.random_crop(video, size=[numFrames, frameHeight - 20, frameWidth - 20, 3])
    # Resize frames back to original dimensions
    video = tf.image.resize(video, (frameHeight, frameWidth))
    return video

# Updated load and process function to include augmentation
def loadAndProcessVideoWithAugmentation(filePath, label):
    video = tf.py_function(loadVideo, [filePath], tf.float32)
    video.set_shape((numFrames, frameHeight, frameWidth, 3))
    video = augmentVideo(video)
    return video, label

# Helper function to load a single video file
def loadVideo(path):
    videoFrames = []
    cap = cv2.VideoCapture(path.numpy().decode())
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (frameHeight, frameWidth))
            videoFrames.append(frame)
    finally:
        cap.release()
    videoFrames = selectFrames(videoFrames, numFrames)
    videoFrames = np.array(videoFrames) / 255.0
    return videoFrames.astype(np.float32)

# Function to select a fixed number of evenly spaced frames from the video
def selectFrames(frames, numFrames):
    interval = len(frames) / float(numFrames)
    selectedFrames = []
    
    for i in range(numFrames):
        idx = int(i * interval)
        # Ensure idx is within the bounds of frames list
        idx = min(idx, len(frames) - 1)
        selectedFrames.append(frames[idx])
    
    return np.array(selectedFrames)

# Function to process video file paths
def processPath(filePath):
    label = tf.strings.split(filePath, os.path.sep)[-2]
    label = classNameToIndex.lookup(label)
    label = tf.one_hot(label, numClasses)
    return filePath, label

# Extract class names
classNames = np.array(sorted(item.name for item in dataDir.glob('*/') if item.is_dir()))
classNameToIndex = tf.lookup.StaticHashTable(
    initializer=tf.lookup.KeyValueTensorInitializer(
        keys=classNames,
        values=tf.range(len(classNames), dtype=tf.int64)),
    default_value=-1)

# List of video file paths and their labels
videoFiles = list(dataDir.glob('*/*.avi'))

# Shuffle video files
np.random.shuffle(videoFiles)

# Split into train and test sets
trainSplit = int(len(videoFiles) * 0.8)
trainFiles = videoFiles[:trainSplit]
testFiles = videoFiles[trainSplit:]

# Create TensorFlow datasets
trainDs = tf.data.Dataset.from_tensor_slices([str(path) for path in trainFiles])
trainDs = trainDs.map(processPath, num_parallel_calls=tf.data.experimental.AUTOTUNE)
trainDs = trainDs.cache().map(loadAndProcessVideoWithAugmentation, num_parallel_calls=tf.data.experimental.AUTOTUNE)
trainDs = trainDs.batch(batchSize).prefetch(tf.data.experimental.AUTOTUNE)

testDs = tf.data.Dataset.from_tensor_slices([str(path) for path in testFiles])
testDs = testDs.map(processPath, num_parallel_calls=tf.data.experimental.AUTOTUNE)
testDs = testDs.cache().map(loadAndProcessVideoWithAugmentation, num_parallel_calls=tf.data.experimental.AUTOTUNE)
testDs = testDs.batch(batchSize).prefetch(tf.data.experimental.AUTOTUNE)

def buildCnnLstmModel(inputShape, numClasses):
    model = Sequential()
    
    # CNN layers wrapped in TimeDistributed to process video frames
    model.add(TimeDistributed(Conv2D(32, (3, 3), activation='relu', padding='same'), input_shape=inputShape))
    model.add(TimeDistributed(MaxPooling2D((2, 2))))
    model.add(TimeDistributed(Conv2D(64, (3, 3), activation='relu', padding='same')))
    model.add(TimeDistributed(MaxPooling2D((2, 2))))
    model.add(TimeDistributed(Conv2D(128, (3, 3), activation='relu', padding='same')))
    model.add(TimeDistributed(MaxPooling2D((2, 2))))
    model.add(TimeDistributed(Flatten()))
    
    # LSTM layers to learn temporal dynamics
    model.add(LSTM(128, return_sequences=True))
    model.add(LSTM(128))

    # Fully connected layers
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(numClasses, activation='softmax'))
    
    return model

# Build and compile the model
inputShape = (numFrames, frameHeight, frameWidth, 3)  # Input shape of each video clip
model = buildCnnLstmModel(inputShape, numClasses)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

reduceLr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.00001, verbose=1)
earlyStopping = EarlyStopping(monitor='val_loss', patience=5, verbose=1, restore_best_weights=True)

def scheduler(epoch, lr):
    if epoch < 10:
        return lr
    else:
        return lr * tf.math.exp(-0.1)

lrScheduler = LearningRateScheduler(scheduler)

# Train model with callbacks
history = model.fit(trainDs, epochs=45, validation_data=testDs, callbacks=[reduceLr, earlyStopping, lrScheduler])

# Evaluate the model on the test set
testLoss, testAcc = model.evaluate(testDs)
print(f"Test accuracy: {testAcc}")

model.save("101SportsClassificationModel.keras")

# Quantise
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Enable the use of select TensorFlow ops
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,  # Enable TensorFlow Lite ops.
    tf.lite.OpsSet.SELECT_TF_OPS     # Enable TensorFlow ops.
]

# Disable the experimental lowering of tensor list ops
converter._experimental_lower_tensor_list_ops = False

tfliteQuantModel = converter.convert()

# Save the quantized model
tfliteModelPath = "quantized_65SportsClassificationModel.tflite"
with open(tfliteModelPath, 'wb') as f:
    f.write(tfliteQuantModel)
