import csv


dict={}
with open("output_full_csv.csv", encoding='utf-8') as r_file:
    file_reader = csv.reader(r_file, delimiter=";")
    counter = 1
    for r in file_reader:
        if counter == 1:
            counter += 1
            continue
        else:
            if r[0] + r[1] not in dict:
                dict[r[0] + r[1]] = [r[2]]
            else:
                dict[r[0] + r[1]].append(r[2])

z = dict.keys()
for i in z:
    print(sorted(dict[i]))