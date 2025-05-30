Experimentation processs:

v1 Started with copy of a 'standard' cnn for img rec. ~0.05 acc

v2 Used tf.keras.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)) added 2 conv + pooling
steps Added 2 more layers with relu and 128 64 32 neurons ~.7 acc

v3
Decreased dropout. note decreasing it more leads to horrible performace. ~.95 acc