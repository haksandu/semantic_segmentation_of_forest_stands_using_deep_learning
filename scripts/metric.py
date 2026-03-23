

import numpy as np
import tensorflow as tf
from keras import backend as K


def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall_keras = true_positives / (possible_positives + K.epsilon())
    return recall_keras


def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision_keras = true_positives / (predicted_positives + K.epsilon())
    return precision_keras

def f1(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    return 2 * ((p * r) / (p + r + K.epsilon()))

from tensorflow.keras import backend as K # type: ignore

def MCC(y_true, y_pred):
    """Calculates the MCC for binary classification"""
    tp = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    tn = K.sum(K.round(K.clip((1 - y_true) * (1 - y_pred), 0, 1)))
    fp = K.sum(K.round(K.clip((1 - y_true) * y_pred, 0, 1)))
    fn = K.sum(K.round(K.clip(y_true * (1 - y_pred), 0, 1)))

    num = tp * tn - fp * fn
    den = K.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    mcc = num / (den + K.epsilon())
    # print(f'tp: {tp},tn: {tn},fp: {fp}, fn: {fn}')
    return mcc

def mMCC(y_true, y_pred):
    """
    Extends the MCC metric for use in multiclass cases.
    Macro average of MCC:
    MCC is calculated for each class separately before averaging the results.
    Every class is given the same importance.
    Expects one-hot encoded tensors of shape: (N, H, W, C)
    """ 
    num_classes = tf.shape(y_true)[-1]  # Find number of classes
    mcc_accumulated = tf.cast(0, tf.float32)  # start mcc counter
    for class_index in range(num_classes):
        y_true_binary = y_true[..., class_index] 
        y_pred_binary = y_pred[..., class_index]
        mcc_value = MCC(y_true_binary, y_pred_binary)
        mcc_accumulated += mcc_value
        # print(f'class: {class_index}, mcc: {mcc_value}')
        # print(f'accumulated mcc: {mcc_accumulated}')
    return mcc_accumulated / tf.cast(num_classes, tf.float32)

def microMCC(y_true, y_pred):
    """
    Extends the MCC metric for use in multiclass cases.
    Micor average of MCC:
    TP, TN, FP, and FN are summed for all classes, and used as basis for calculating MCC.
    Every instance is given the same importance.
    Expects one-hot encoded tensors of shape (N, H, W, C)
    """
    flat_true = tf.reshape(y_true, [-1])
    flat_pred = tf.reshape(y_pred, [-1])

    return MCC(flat_true, flat_pred)

def mIOU(y_true, y_pred):
    """
    Calculate the mean Intersection over Union (mIoU) metric.
    
    Arguments:
        y_true: The true labels (ground truth).
        y_pred: The predicted labels.
        
    Returns:
        mIoU score.
    """
    # Convert predictions to binary values (0 or 1)
    y_pred = K.round(y_pred)
    
    # Calculate the intersection and union for each class
    intersection = K.sum(K.abs(y_true * y_pred), axis=[1,2,3])
    union = K.sum(K.clip(y_true + y_pred, 0, 1), axis=[1,2,3])
    
    # Compute the IoU (Intersection over Union)
    iou = intersection / (union + K.epsilon())  # Adding a small value to avoid division by zero
    
    # Compute the mean over classes
    m_iou = K.mean(iou)
    
    return m_iou

class MacroPrecision(tf.keras.metrics.Metric):
    def __init__(self, name="macro_precision", **kwargs):
        super(MacroPrecision, self).__init__(name=name, **kwargs)
        self.precisions = []
        
    def update_state(self, y_true, y_pred, sample_weight=None):
        y_pred = tf.argmax(y_pred, axis=-1)
        y_true = tf.cast(y_true, dtype=tf.int32)
        num_classes = tf.reduce_max(y_true) + 1

        # Compute precision per class
        precisions = []
        for i in range(num_classes):
            y_true_i = tf.cast(tf.equal(y_true, i), tf.float32)
            y_pred_i = tf.cast(tf.equal(y_pred, i), tf.float32)
            precision = tf.reduce_sum(y_true_i * y_pred_i) / (tf.reduce_sum(y_pred_i) + tf.keras.backend.epsilon())
            precisions.append(precision)
        
        self.precisions.append(tf.reduce_mean(precisions))

    def result(self):
        return tf.reduce_mean(self.precisions)

    def reset_states(self):
        self.precisions = []

class MacroRecall(tf.keras.metrics.Metric):
    def __init__(self, name="macro_recall", **kwargs):
        super(MacroRecall, self).__init__(name=name, **kwargs)
        self.recalls = []
        
    def update_state(self, y_true, y_pred, sample_weight=None):
        y_pred = tf.argmax(y_pred, axis=-1)
        y_true = tf.cast(y_true, dtype=tf.int32)
        num_classes = tf.reduce_max(y_true) + 1

        # Compute recall per class
        recalls = []
        for i in range(num_classes):
            y_true_i = tf.cast(tf.equal(y_true, i), tf.float32)
            y_pred_i = tf.cast(tf.equal(y_pred, i), tf.float32)
            recall = tf.reduce_sum(y_true_i * y_pred_i) / (tf.reduce_sum(y_true_i) + tf.keras.backend.epsilon())
            recalls.append(recall)
        
        self.recalls.append(tf.reduce_mean(recalls))

    def result(self):
        return tf.reduce_mean(self.recalls)

    def reset_states(self):
        self.recalls = []


