import tensorflow as tf
from modelCNN import create_model
from modelRestNet.modelResnet import resnet_18, resnet_34, resnet_50, resnet_101, resnet_152
from modelDenseNet.modelDenseNet import densenet_121, densenet_169, densenet_201, densenet_264

img_height = 200
img_width = 67
batch_size = 64

# model = model = create_model((img_height, img_width, 3))
model = resnet_18()
model.build(input_shape=(None, img_height, img_width, 3))
model.compile(loss='sparse_categorical_crossentropy', optimizer=tf.optimizers.SGD(learning_rate=0.001), metrics=['accuracy'])
model.summary()

model.load_weights('./chk_points_resnet_densenet/resnet18/checkpoint_1')
# model.load_weights('./chk_points/checkpoint_1')

test_ds = tf.keras.utils.image_dataset_from_directory(
    'datasetimg_test', labels='inferred', 
    label_mode='int',
    color_mode='rgb', 
    batch_size=batch_size, 
    image_size=(img_height,img_width), 
    shuffle=True,
    seed=6796013,
    interpolation='bilinear'
)

evaluation = model.evaluate(test_ds, return_dict=True)

print("[+] Result:")

for name, value in evaluation.items():
    print(f"{name}: {value:.4f}")
