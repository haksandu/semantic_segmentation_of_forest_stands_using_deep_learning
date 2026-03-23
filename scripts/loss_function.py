
# LOSS FUCTIONS

## TVERSKY LOSS
import tensorflow as tf

def tversky_loss(alpha = 0.5, beta=0.5, smooth=1e-6):
    def tversky(y_true, y_pred):
        """
        Adjust Alpha and Beta to controll the trade off between False Positives and False Negatives
        
        Generally:
            alpha: Penalty for false positives
            beta: Penalty for false negatives
                
                -> 0: small penalty, 1: high penalty
            
        """
        true_positives = tf.reduce_sum(y_true * y_pred, axis=[1, 2])
        false_positives = tf.reduce_sum((1 - y_true) * y_pred, axis=[1, 2])
        false_negatives = tf.reduce_sum(y_true * (1 - y_pred), axis=[1, 2])
        
        tversky_coeff = (true_positives + smooth) / (true_positives + alpha * false_positives + beta * false_negatives + smooth)
        
        return 1 - tf.reduce_mean(tversky_coeff)
    return tversky



## Focal Tversky Loss
import tensorflow as tf

def focal_tversky_loss(alpha=0.5, beta=0.5, gamma=4/3, smooth=1e-6):
    """
    Computes Focal Tversky Loss for multiclass segmentation with multiple channels.
    TI calculated for each class separately since FP=FN in multiclass cases. 

    Args:
        alpha: Controls the weight of false positives.
        beta: Controls the weight of false negatives.
        gamma: Focusing parameter, adjusts the shape of the loss curve.
        smooth: Small constant to avoid division by zero.

    Returns:
        Loss function to minimize.
    """
    @tf.function
    def focal_tversky(y_true, y_pred):
        # Calculate Tversky Index for each class separately, assuming y_true is one-hot encoded
        true_positives = tf.reduce_sum(y_true * y_pred, axis=[0, 1, 2])         # Sum over batch and spatial dimensions
        false_positives = tf.reduce_sum((1 - y_true) * y_pred, axis=[0, 1, 2])  # Sum over batch and spatial dimensions
        false_negatives = tf.reduce_sum(y_true * (1 - y_pred), axis=[0, 1, 2])  # Sum over batch and spatial dimensions

        # Calculate per-class Tversky index
        tversky_index = (true_positives + smooth) / (true_positives + alpha * false_positives + beta * false_negatives + smooth)
        tversky_index = tf.clip_by_value(tversky_index, smooth, 1 - smooth)  # Clipping for stability

        # Focal Tversky Loss per class
        focal_tversky_value = tf.pow((1 - tversky_index), (1 / gamma))

        # Take the mean across classes and batches
        return tf.reduce_mean(focal_tversky_value)

    return focal_tversky
