from typing import List, Tuple


def get_confusion_matrix(
    y_true: List[int],
    y_pred: List[int],
    num_classes: int,
) -> List[List[int]]:
    """
    Generate a confusion matrix in a form of a list of lists.

    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values
    :param num_classes: number of supported classes

    :return: confusion matrix
    """

    if len(y_true) != len(y_pred):
        raise ValueError("Invalid input shapes!")

    confusion_matrix = [[0] * num_classes for _ in range(num_classes)]

    for true_value, predicted_value in zip(y_true, y_pred):
        if predicted_value > num_classes or true_value > num_classes:
            raise ValueError("Invalid prediction classes!")
        confusion_matrix[true_value][predicted_value] += 1

    return confusion_matrix


def get_quality_factors(
    y_true: List[int],
    y_pred: List[int],
) -> Tuple[int, int, int, int]:
    """
    Calculate True Negative, False Positive, False Negative and True Positive
    metrics basing on the ground truth and predicted lists.

    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: a tuple of TN, FP, FN, TP
    """
    confusion_matrix = get_confusion_matrix(y_true, y_pred, 2)

    return (
        confusion_matrix[0][0],
        confusion_matrix[0][1],
        confusion_matrix[1][0],
        confusion_matrix[1][1],
    )


def accuracy_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the accuracy for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: accuracy score
    """
    factors = get_quality_factors(y_true, y_pred)

    return (factors[0] + factors[3]) / sum(factors)


def precision_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the precision for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: precision score
    """
    factors = get_quality_factors(y_true, y_pred)

    return factors[3] / (factors[3] + factors[1])


def recall_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the recall for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: recall score
    """
    factors = get_quality_factors(y_true, y_pred)

    return factors[3] / (factors[3] + factors[2])


def f1_score(y_true: List[int], y_pred: List[int]) -> float:
    """
    Calculate the F1-score for given lists.
    :param y_true: a list of ground truth values
    :param y_pred: a list of prediction values

    :return: F1-score
    """
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)

    return 2 * precision * recall / (precision + recall)
