


x_curs = 0
lst = []

for staff in range(7):

    for line in range(2):
        lst.append(x_curs)
        x_curs += 10

    x_curs += 10

    for line in range(3):
        lst.append(x_curs)
        x_curs += 10

    x_curs += 10

print(lst)