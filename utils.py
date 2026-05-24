def str_to_image(s):
    s = s[1:-1] # remove surrounding endlines
    return [list(line) for line in s.split()]

def copy_image(img):
    return [line[:] for line in img]

def sublist(lst, start, end):
    return map(lambda i: lst[i+start], range(len(lst) - (start+end)))
