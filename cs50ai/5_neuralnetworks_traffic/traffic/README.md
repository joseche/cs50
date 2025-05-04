Work log:

Starting with a basic setup based on:
https://cs231n.github.io/convolutional-networks/#architectures

[Input] → [Conv2D + ReLU] → [Conv2D + ReLU] → [MaxPooling] →
→ [Conv2D + ReLU] → [MaxPooling] → [Flatten] → [Dense] → [Softmax]

# Try #1
```py
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(NUM_CATEGORIES, activation="softmax"))
```

Results:
333/333 - 4s - 12ms/step - accuracy: 0.9820 - loss: 0.0830
python traffic.py gtsrb  1020.62s user 147.81s system 518% cpu 3:45.39 total

# Try #2

Removing the second layer.

```py
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2)))
    # model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    # model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(NUM_CATEGORIES, activation="softmax"))
```

Results:
333/333 - 3s - 10ms/step - accuracy: 0.9804 - loss: 0.0752
python traffic.py gtsrb  920.38s user 164.96s system 419% cpu 4:18.94 total

# Try #3

Reduce in half the hidden layer

```py
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2)))
    # model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    # model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation="relu"))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(NUM_CATEGORIES, activation="softmax"))
```

Results:
333/333 - 3s - 10ms/step - accuracy: 0.0549 - loss: 3.5065
python traffic.py gtsrb  826.33s user 142.79s system 447% cpu 3:36.61 total

Horribly bad!!!

# try 4

Increase hidden layers

```py
    model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2)))
    # model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    # model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(NUM_CATEGORIES, activation="softmax"))
```

Results:

333/333 - 4s - 12ms/step - accuracy: 0.9615 - loss: 0.1785
python traffic.py gtsrb  920.44s user 158.50s system 469% cpu 3:49.57 total

# Try #5, repeat the prev best results

```py
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(NUM_CATEGORIES, activation="softmax"))
```

Results:
333/333 - 5s - 15ms/step - accuracy: 0.9805 - loss: 0.0839
python traffic.py gtsrb  917.11s user 169.94s system 457% cpu 3:57.39 total

# Try #6, duplicating the first layer

```py
    model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2)))
    # model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    # model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(NUM_CATEGORIES, activation="softmax"))
```

Results:

333/333 - 6s - 19ms/step - accuracy: 0.9865 - loss: 0.0716
python traffic.py gtsrb  1927.13s user 250.52s system 554% cpu 6:32.98 total

# Try #7, second conv net added

```py
    model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D((2, 2)))
    # model.add(layers.Conv2D(64, (3, 3), activation="relu"))
    # model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(NUM_CATEGORIES, activation="softmax"))
```

Results:

333/333 - 9s - 26ms/step - accuracy: 0.9926 - loss: 0.0286
python traffic.py gtsrb  2745.29s user 298.86s system 601% cpu 8:25.95 total
