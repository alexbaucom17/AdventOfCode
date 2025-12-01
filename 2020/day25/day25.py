
def transform(subject, loops, value=1):
    for n in range(loops):
        value *= subject
        value %= 20201227
    return value

def find_loop_value(public_key):
    max_search = 10000000
    public_subject = 7
    value = 1
    for i in range(max_search):
        if i % (max_search/10) == 0:
            print("Search num: {}".format(i))
        value = transform(public_subject, 1, value)
        if value == public_key:
            return i+1
    return None

def find_private_key(pub1, pub2):
    loop1 = find_loop_value(pub1)
    if loop1 is None:
        raise ValueError("No loop value found, try increasing search limit")
    private_key = transform(pub2, loop1)
    return private_key


if __name__ == '__main__':

    sample_data = (5764801, 17807724)
    data = (9093927, 11001876)

    d = data
    print(find_private_key(d[0], d[1]))
