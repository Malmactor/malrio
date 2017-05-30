import tensorflow as tf
import numpy as np

__author__ = "Chang Gao"
__copyright__ = "Copyright (c) 2017 Malmactor"
__license__ = "MIT"

def write_batch_to_tfrecord(batch, tfrecord_file):
    writer = tf.python_io.TFRecordWriter(tfrecord_file)
    for data in batch:
        example = tf.train.Example(features=tf.train.Features(feature={
                    'data': tf.train.Feature(float_list=tf.train.FloatList(value=data))
                    }))
        # print(example)
        writer.write(example.SerializeToString())
    writer.close()


def read_batch_from_tfrecord(filename, datalen=4, num_epochs=1, capacity=3):
    filename_queue = tf.train.string_input_producer([filename], num_epochs, capacity)
    reader = tf.TFRecordReader()
    _, tfrecord_serialized = reader.read(filename_queue)

    features = tf.parse_single_example(
      tfrecord_serialized,
      features={
          'data': tf.FixedLenFeature([datalen], tf.float32)
      })

    data = features['data']
    print data

    # init = tf.global_variables_initializer()
    # with tf.Session() as sess:
    #     sess.run(init)
    #     coord = tf.train.Coordinator()
    #     threads = tf.train.start_queue_runners(coord=coord, sess=sess)
    #
    #     try:
    #         step = 0
    #         while not coord.should_stop():
    #             data = sess.run([data])
    #             print data
    #             step += 1
    #     except tf.errors.OutOfRangeError:
    #         print 'Total Features:', step
    #     finally:
    #         coord.request_stop()
    #         coord.join(threads)
    #         sess.close()
    #
    #     coord.request_stop()
    #     coord.join(threads)


def main():
    tfrecord_file = 'store.tfrecord'
    testarray = np.array(
        [[0.1, 0.2, 0.3, 0.4],
         [0.3, 0.4, 0.5, 0.6],
         [0.5, 0.6, 0.7, 0.8]]
    )
    write_batch_to_tfrecord(testarray, tfrecord_file)
    read_batch_from_tfrecord(tfrecord_file)

if __name__ == "__main__":
    main()
