# This is an early attempt at replicating the Shake-Shake ResNet architecture in TensorFlow
#     https://github.com/xgastaldi/shake-shake
# This hasn't been tested much so is likely to be buggy. It only reaches a validation error of
# 6.9% with simple data augmentation (flipping and cropping) which is quite
# below the expected validation error of 4.3%.
#
# Main differences:
# - Use the standard momentum optimizer with a fixed learning rate schedule rather than learning
#   rate annealing.
# - For the first block where the stride is 1 but the number of input and output features are
#   different, use a single 2d convolution rather than two of them.
import numpy as np
import tensorflow as tf

mode = 'even'

def unpickle(file):
  import cPickle
  fo = open(file, 'rb')
  dict = cPickle.load(fo)
  fo.close()
  if 'data' in dict:
    dict['data'] = dict['data'].reshape((-1, 3, 32, 32)).swapaxes(1, 3).swapaxes(1, 2) / 256.
  return dict

def load_data_one(f):
  batch = unpickle(f)
  data = batch['data']
  labels = batch['labels']
  print "Loading %s: %d" % (f, len(data))
  return data, labels

def load_data(files, data_dir, label_count):
  data, labels = load_data_one(data_dir + '/' + files[0])
  for f in files[1:]:
    data_n, labels_n = load_data_one(data_dir + '/' + f)
    data = np.append(data, data_n, axis=0)
    labels = np.append(labels, labels_n, axis=0)
  labels = np.array([ [ float(i == label) for i in xrange(label_count) ] for label in labels ])
  return data, labels

def run_in_batch_avg(session, tensors, batch_placeholders, feed_dict={}, batch_size=128):                              
  res = [ 0 ] * len(tensors)                                                                                           
  batch_tensors = [ (placeholder, feed_dict[ placeholder ]) for placeholder in batch_placeholders ]                    
  total_size = len(batch_tensors[0][1])                                                                                
  batch_count = (total_size + batch_size - 1) / batch_size                                                             
  for batch_idx in xrange(batch_count):                                                                                
    current_batch_size = None                                                                                          
    for (placeholder, tensor) in batch_tensors:                                                                        
      batch_tensor = tensor[ batch_idx*batch_size : (batch_idx+1)*batch_size ]                                         
      current_batch_size = len(batch_tensor)                                                                           
      feed_dict[placeholder] = tensor[ batch_idx*batch_size : (batch_idx+1)*batch_size ]                               
    tmp = session.run(tensors, feed_dict=feed_dict)                                                                    
    res = [ r + t * current_batch_size for (r, t) in zip(res, tmp) ]                                                   
  return [ r / float(total_size) for r in res ]

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.01)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.01, shape=shape)
  return tf.Variable(initial)

def conv2d(input, in_features, out_features, kernel_size, stride):
  W = weight_variable([ kernel_size, kernel_size, in_features, out_features ])
  return tf.nn.conv2d(input, W, [ 1, stride, stride, 1 ], padding='SAME')

def basic_block(input, in_features, out_features, stride, is_training):
  if in_features == out_features:
    assert(stride == 1);
    shortcut = input
  else:
    input_relu = tf.nn.relu(input)
    if stride == 1:
      shortcut = conv2d(input_relu, in_features, out_features, 1, 1)
    else:
      shortcut1 = conv2d(input_relu[:,::stride,::stride,:], in_features, out_features/2, 1, 1)
      shortcut2 = conv2d(input_relu[:,1::stride,1::stride,:], in_features, out_features/2, 1, 1)
      shortcut = tf.concat([ shortcut1, shortcut2 ], 3)
    shortcut = tf.contrib.layers.batch_norm(shortcut, scale=True, is_training=is_training, updates_collections=None)

  def branch(current):
    current = tf.nn.relu(current)
    current = conv2d(current, in_features, out_features, 3, stride)
    current = tf.contrib.layers.batch_norm(current, scale=True, is_training=is_training, updates_collections=None)
    current = tf.nn.relu(current)
    current = conv2d(current, out_features, out_features, 3, 1)
    current = tf.contrib.layers.batch_norm(current, scale=True, is_training=is_training, updates_collections=None)
    return current
  branch1 = branch(input)
  branch2 = branch(input)
  if mode == 'even':
    alpha = 0.5
  elif mode == 'shake':
    alpha = tf.cond(is_training, lambda: tf.random_uniform([ 1 ]), lambda: tf.constant(0.5)) # per batch shake/keep for now...
  else:
    raise Exception('unknown mode ' + mode)
  return shortcut + alpha * branch1 + (1 - alpha) * branch2

def block_stack(input, in_features, out_features, stride, depth, is_training):
  current = basic_block(input, in_features, out_features, stride, is_training)
  for _d in xrange(depth - 1):
    current = basic_block(current, out_features, out_features, 1, is_training)
  return current

def run_model(data, image_shape, label_count):
  graph = tf.Graph()
  with graph.as_default():
    xs = tf.placeholder("float", shape=[None] + image_shape)
    ys = tf.placeholder("float", shape=[None, label_count])
    lr = tf.placeholder("float", shape=[])
    is_training = tf.placeholder("bool", shape=[])

    current = xs
    current = conv2d(current, 3, 16, 3, 1)
    current = tf.contrib.layers.batch_norm(current, scale=True, is_training=is_training, updates_collections=None)

    K = 2
    current = block_stack(current, 16,   16*K, 1, 4, is_training)
    current = block_stack(current, 16*K, 32*K, 2, 4, is_training)
    current = block_stack(current, 32*K, 64*K, 2, 4, is_training)

    current = tf.nn.relu(current)
    current = tf.reduce_mean(current, reduction_indices=[1, 2], name="avg_pool")
    final_dim = 64*K
    current = tf.reshape(current, [ -1, final_dim ])
    Wfc = weight_variable([ final_dim, label_count ])
    bfc = bias_variable([ label_count ])
    ys_ = tf.nn.softmax( tf.matmul(current, Wfc) + bfc )

    cross_entropy = -tf.reduce_mean(ys * tf.log(tf.clip_by_value(ys_, 1e-7, 1-1e-7)))

    train_step = tf.train.MomentumOptimizer(lr, 0.9, use_nesterov=True).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(ys_, 1), tf.argmax(ys, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

  with tf.Session(graph=graph) as session:
    batch_size = 64
    train_data, train_labels = data['train_data'], data['train_labels']
    batch_count = len(train_data) / batch_size
    batches_data = np.split(train_data[:batch_count*batch_size], batch_count)
    batches_labels = np.split(train_labels[:batch_count*batch_size], batch_count)
    learning_rate = 0.1
    session.run(tf.global_variables_initializer())
    saver = tf.train.Saver()
    for epoch in xrange(1, 1+90):
      if epoch == 30: learning_rate = 0.01
      if epoch == 60: learning_rate = 0.001
      for batch_idx in xrange(batch_count):
        batch_data = batches_data[batch_idx]
        batch_labels = batches_labels[batch_idx]
      
        batch_res = session.run([ train_step, cross_entropy, accuracy ],
          feed_dict = { xs: batch_data, ys: batch_labels, lr: learning_rate, is_training: True })

      save_path = saver.save(session, 'resnet_%d.ckpt' % epoch)
      test_results = run_in_batch_avg(session, [ cross_entropy, accuracy ], [ xs, ys ],
          feed_dict = { xs: data['test_data'], ys: data['test_labels'], is_training: False })
      print epoch, batch_res[1:], test_results

def run():
  data_dir = 'data'
  image_size = 32
  meta = unpickle(data_dir + '/batches.meta')
  label_names = meta['label_names']
  label_count = len(label_names)

  train_files = [ 'data_batch_%d' % d for d in xrange(1, 6) ]
  train_data, train_labels = load_data(train_files, data_dir, label_count)
  pi = np.random.permutation(len(train_data))
  train_data, train_labels = train_data[pi], train_labels[pi]
  test_data, test_labels = load_data([ 'test_batch' ], data_dir, label_count)
  print "Train:", np.shape(train_data), np.shape(train_labels)
  print "Test:", np.shape(test_data), np.shape(test_labels)
  data = { 'train_data': train_data,
      'train_labels': train_labels,
      'test_data': test_data,
      'test_labels': test_labels }
  run_model(data, [ image_size, image_size, 3 ], label_count)

run()
