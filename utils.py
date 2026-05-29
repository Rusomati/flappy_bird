def sublist_iterator(lst, start, end):
    return map(lambda i: lst[i+start], range(len(lst) - (start+end)))
