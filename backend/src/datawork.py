def data_format(a):
    if len(list(a.split())) == 1:
        a = list(a.split('-'))
        a.reverse()
        a = date(int(a[0]), int(a[1]), int(a[2]))
    else:
        a = list(a.split())[0]
        a = list(a.split('-'))
        a = date(int(a[0]), int(a[1]), int(a[2]))
    return a

def result(a, b):  # b = '30-10-2021' a = '2021-06-08 07:03:52.294000'
    y = str(abs(a - b)).split()
    if len(y) == 1:
        return 0
    else:
        result = int(str(abs(a - b)).split()[0])
        result = result // 30
        return result


def fall_rate(n, length):
    for i in range(length):
        if n > 500:
            n = int(n * 0.8)
        else:
            n -= 100
    return n

k = str(datetime.datetime.now())
k = '-'.join(reversed(k.split()[0].split('-')))
k = data_format(k)
dict = {'now':k}

with open("output_full_csv.csv", encoding='utf-8') as r_file:
    file_reader = csv.reader(r_file, delimiter=";")
    counter = 1
    for r in file_reader:
        if counter == 1:
            counter += 1
            continue
        else:
            if r[0] + r[1] not in dict:
                r[2] = data_format(r[2])
                dict[r[0] + r[1]] = [[r[2], r[5]]]
            else:
                r[2] = data_format(r[2])
                dict[r[0] + r[1]].append([r[2], r[5]])

z = dict.keys()
for i in z:
    answer = []
    rate = 0
    if i == 'now':
        continue
    x = []
    for q in dict[i]:
        x.append(q[0])
    if len(x) == 1:
        mouths = result(x[0], dict['now'])
        rate = fall_rate(rate, mouths)
        answer.append(int(dict[i][0][1]))
        dict[i] = [rate, answer]
    else:
        answer = []
        for l in range(len(x) - 1):
            length = result(x[l], x[l + 1])
            rate += 100
            rate = fall_rate(rate, length)
            answer.append(int(dict[i][l][1]))
        mouths = result(x[-1], dict['now'])
        rate = fall_rate(rate, mouths)
        dict[i] = [rate, answer]

for i in z:
    if i != 'now':
        print(i, dict[i])

