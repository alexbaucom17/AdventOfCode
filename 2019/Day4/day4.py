import numpy as np

def check_digits(digits):
    d = np.diff(digits)
    if np.any(d < 0) or not np.any(d == 0):
        return False    
    else:
        if check_extra_digits(d):
            return True
        else:
            return False

def check_extra_digits(d):
    for i in range(5):
        a = False
        b = False
        if d[0,i] == 0:
            if i-1 < 0:
                a = True
            elif d[0,i-1] != 0:
                a = True

            if i+1 > 4:
                b = True
            elif d[0,i+1] != 0:
                b = True

            if a and b:
                return True 

    return False
 

def num_to_digits(num):
    digits = np.zeros((1,6), dtype=np.int8)
    div = 10
    for i in range(6):
        r = num % div
        digits[0,i] = r
        num -= r * (div/10)
        num /= 10

    return np.fliplr(digits)

def check_num(num):
    digits = num_to_digits(num)
    ok = check_digits(digits)
    return ok


if __name__ == '__main__':
    count = 0
    for n in range(136818,685979):
        if check_num(n):
            count += 1

    print(count)
