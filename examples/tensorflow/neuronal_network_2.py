import tensorflow as tf

from mlaide.client import MLAideClient, ConnectionOptions

project_key = 'neuronal-network'
options = ConnectionOptions(
  api_key='YXV0aDB8NWY0MjkxMzM0MjA3ZDEwMDZkZWM1YWYwOsKoPSJPIzTCqsK0d3R34oCT'
)
mlaide_client = MLAideClient(project_key=project_key, options=options)

run = mlaide_client.start_new_run(experiment_key='neuronal-network-debug', run_name='training')

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10)
])

predictions = model(x_train[:1]).numpy()
print(predictions)

print(tf.nn.softmax(predictions).numpy())

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
print(loss_fn(y_train[:1], predictions).numpy())

model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)
run.log_model(model, "mnist model")

print(model.evaluate(x_test,  y_test, verbose=2))

probability_model = tf.keras.Sequential([
  model,
  tf.keras.layers.Softmax()
])

print(probability_model(x_test[:5]))
