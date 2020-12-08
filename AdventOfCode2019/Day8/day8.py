import numpy as np
from matplotlib import pyplot as plt

def data_to_array(data, px_width, px_height):
    arr = np.asarray(data).reshape((px_width, px_height, -1), order='F')
    return np.transpose(arr, (1,0,2))

def layer_with_fewest_zeros(pic):
    return np.argmin(np.sum(pic == 0,axis=(0,1)))

def compute(pic_layer):
    return np.sum(pic_layer == 1) * np.sum(pic_layer == 2)

def find_px_for_stack(stack):
    idx = np.where(stack < 2)
    return stack[idx[0][0]]


if __name__ == '__main__':

    with open('Day8/input.txt','r') as f:
        text = f.read()
        data = [int(x) for x in text]
        arr = data_to_array(data,25,6)
        out = np.zeros((6,25),dtype=int)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                stack = arr[i,j,:]
                out[i,j] = find_px_for_stack(stack)

        plt.imshow(out, vmin=0, vmax=1)
        plt.show()


