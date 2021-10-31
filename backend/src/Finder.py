import requests
import csv

def objects_city(name_object):
    answer = []
    coords = [['47.48840905', '56.124411499999994'], ['47.2435409704655', '56.13035855']]
    for coord in coords:
        string_coord = coord[0] + "," + coord[1]
        object_request = "https://search-maps.yandex.ru/v1/?text=" + name_object + "&type=biz&lang=ru_RU&ll=" \
                         + string_coord + "&spn=1,1&results=1000&apikey=6633a817-a99a-4d17-b557-a77557303ccc"
        object_response = requests.get(object_request)
        json_response = object_response.json()
        for i in json_response['features']:
            name = i['properties']['name']
            coord_object = i['geometry']['coordinates']
            if float(coord[0]) - 0.05 <= float(coord_object[0]) and float(coord_object[0]) <= float(coord[0]) + 0.05:
                answer.append([name, coord_object])
    return answer


pogr = 0.02
data = []
objects = ['аптека', 'магазин', 'школа', 'детский сад', ]
objects_dict = {}
for i in objects:
    f = objects_city(i)
    objects_dict[i] = f


with open("out.csv", encoding='utf-8') as r_file:
    file_reader = csv.reader(r_file, delimiter=";")
    for r in file_reader:
        ff = 0
        flag = 0
        question = r[3]
        coord = list(map(float, r[4].split()))
        coord.reverse()
        for k in objects:
            if k in question:
                ff = 1
                flag = 0
                for m in objects_dict[k]:
                    if coord[0] - pogr <=m[1][0] and m[1][0] <= coord[0] +pogr and coord[1] - pogr <=m[1][1] and m[1][1] <= coord[1] +pogr:
                        flag = 1
                        fik = str(m[1][1]) + ' ' + str(m[1][0])
                        break
            if ff == 1 and flag == 0:
                break
        counter = 0
        if flag == 1 and ff == 1:
            print(r)
        if flag == 1:
            r.append([str(flag), fik])
        else:
            r.append(str(flag))
        data.append(r)


myFile = open('output_full_full.csv', 'w', encoding='utf-8', newline="")
with myFile:
    writer = csv.writer(myFile, delimiter=';', lineterminator="\n")
    writer.writerows(data)