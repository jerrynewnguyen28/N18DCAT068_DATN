import tensorflow as tf
import cv2
import numpy as np
import os
from keras.models import load_model
from keras.preprocessing import image
from keras.models import Sequential
import matplotlib.pyplot as plt
img_height = 200
img_width = 67
batch_size = 64
# test_ds = tf.keras.utils.image_dataset_from_directory(
#     'datasetimg_test', labels='inferred', 
#     label_mode='int',
#     color_mode='rgb', 
#     batch_size=batch_size, 
#     image_size=(img_height,img_width), 
#     shuffle=True,
#     seed=132496,
#     interpolation='bilinear'
# )
def load_image(image_name):
    img = tf.keras.utils.load_img(image_name, target_size=(200, 67))
    x = tf.keras.utils.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    return images
model = load_model('./modelsave/mymodel.h5')

model.compile(loss='sparse_categorical_crossentropy', 
                optimizer=tf.optimizers.SGD(learning_rate=0.001), 
                metrics=['accuracy'])
print("test")
# loss, acc = model.evaluate(test_ds, return_dict=True)


# img = tf.keras.utils.load_img('./predict/BAD_611.png', target_size=(200, 67))
# x = tf.keras.utils.img_to_array(img)
# x = np.expand_dims(x, axis=0)

# images = np.vstack([x])
# classes = (model.predict(images) > 0.5).astype("int32")
# classes_predict=np.argmax(classes,axis=1)
# print(classes)
# print(classes_predict)

path_predict = './predict/'
for filename in os.listdir(path_predict):
    print('--------------------------------------')
    ten_image = path_predict + filename
    array_img = load_image(ten_image)
    classes = (model.predict(array_img) > 0.5).astype("int32")
    classes_predict=np.argmax(classes,axis=1)
    print(filename)
    # print(classes)
    # print(classes_predict)
    if classes_predict == 1:
        print("good")
    else:
        print("bad")

