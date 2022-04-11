import numpy as np

def invH(H: np.ndarray) -> np.ndarray:
    R = H[:3, :3]
    d = H[:3, 3]
    Hinv = np.zeros((4,4))
    Rinv = np.transpose(R)
    Hinv[:3,:3] = Rinv
    Hinv[:3, 3] = -Rinv @ d
    Hinv[3,3] = 1
    return Hinv

def rot_trans_to_H(R: np.ndarray, T: np.ndarray) -> np.ndarray:
    H = np.zeros((4,4), dtype=R.dtype)
    H[:3, :3] = R
    H[:3, 3] = T
    H[3,3] = 1
    return H

def transformPoints(points: np.ndarray, H: np.ndarray) -> np.ndarray:
    hPoints = np.vstack((points, np.ones((1, points.shape[1]))))
    hPointsNew = H @ hPoints
    return hPointsNew[:3, :]