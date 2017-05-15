import tensorflow as tf
import numpy as np


def write_batch_to_tfrecord(batch, tfrecord_file):
    writer = tf.python_io.TFRecordWriter(tfrecord_file)
    for data in batch:
        example = tf.train.Example(features=tf.train.Features(feature={
                    'data': tf.train.Feature(float_list=tf.train.FloatList(value=data))
                    }))
        writer.write(example.SerializeToString())
    writer.close()


def read_batch_from_tfrecord(filename):
    filename_queue = tf.train.string_input_producer([filename], num_epochs=1)
    reader = tf.TFRecordReader()
    _, tfrecord_serialized = reader.read(filename_queue)

    features = tf.parse_single_example(
      tfrecord_serialized,
      features={
          'data': tf.FixedLenFeature([], tf.float32)
      })

    data = features['data']
    print data

    # with tf.Session() as sess:
    #     coord = tf.train.Coordinator()
    #     threads = tf.train.start_queue_runners(coord=coord)
    #     data = sess.run([data])
    #     print data
    #     coord.request_stop()
    #     coord.join(threads)


def main():
    tfrecord_file = 'store.tfrecord'
    testarray = np.array(
        [[0.1, 0.2],
         [0.3, 0.4]]
    )
    write_batch_to_tfrecord(testarray, tfrecord_file)
    read_batch_from_tfrecord(tfrecord_file)

if __name__ == "__main__":
    main()
