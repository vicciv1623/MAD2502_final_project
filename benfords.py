def get_digit_frequencies(filename):
    file = open(filename, 'r')
    str_list = []
    while True:
        line = file.readline()
        if not line:
            break
        str_list.append(line)
    ret_list = [0] * 10
    for line in str_list:
        ret_list[int(line[0])] += 1
    return(ret_list)