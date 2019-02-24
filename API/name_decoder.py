def name_decoder(name):
    sum = 0
    for c in name:
        sum += ord(c)
    return "{0:b}".format(sum)

def find_longest_consecutive(sequence):
    sum, res = 0,0
    for i in sequence:
        if i == '0':
            sum += 1
        else:
            sum = 0
        if sum > res:
            res = sum
    return res

