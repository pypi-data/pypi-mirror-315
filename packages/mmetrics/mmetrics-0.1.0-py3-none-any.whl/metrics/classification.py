import numpy as np

def confusion_matrix(y_true, y_pred):
    """Returns the confusion matrix obtained from predicted values and real values"""
    TP = np.sum((y_true == 1) & (y_pred == 1))
    TN = np.sum((y_true == 0) & (y_pred == 0))
    FP = np.sum((y_true == 0) & (y_pred == 1))
    FN = np.sum((y_true == 1) & (y_pred == 0))
    return TP, TN, FP, FN

def accuracy(y_true, y_pred):
    """Returns the accuracy obtained from predicted values and real values"""
    TP, TN, FP, FN = confusion_matrix(y_true, y_pred)
    accuracy_ = (TP + TN) / (TP + TN + FP + FN)
    return accuracy_

def precision(y_true, y_pred):
    """Returns the precision obtained from predicted values and real values"""
    TP, TN, FP, FN = confusion_matrix(y_true, y_pred)
    precision_ = TP / (TP + FP) if TP + FP > 0 else 0
    return precision_

def recall(y_true, y_pred):
    """Returns the recall obtained from predicted values and real values"""
    TP, TN, FP, FN = confusion_matrix(y_true, y_pred)
    recall_ = TP / (TP + FN) if TP + FN > 0 else 0
    return recall_

def f1_score(y_true, y_pred):
    """Returns the F1 score obtained from predicted values and real values"""
    TP, TN, FP, FN = confusion_matrix(y_true, y_pred)
    f1_score_ = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0
    return f1_score_

def jaccard_index(y_true, y_pred):
    """Returns the Jaccard index obtained from predicted values and real values"""
    TP, TN, FP, FN = confusion_matrix(y_true, y_pred)
    jaccard_index_ = (TP) / (TP + FP + FN)
    return jaccard_index_