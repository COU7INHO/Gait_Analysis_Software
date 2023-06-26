lst = [10, 100, 2, 1, 43, 23, 39]

'''
ni = 0
new_lst = []
for n in lst:
    if ni > n:
        ni = n
        new_lst.append(ni)
    else:
        new_lst.append(n)
print(new_lst)
'''

i = 0
n_max = 0
for num in lst:
    if num > n_max:
        n_max = num

    i += 1

print(n_max)
