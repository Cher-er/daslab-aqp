import numpy as np


def sMAPE(truth, aqp):
    result = 2 * (truth - aqp).abs() / (truth.abs() + aqp.abs())
    result[np.isinf(result)] = 0
    return result.mean()
