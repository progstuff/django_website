def change_line(line: str):
    strt_ind = []
    end_ind = []
    cur_ind = 0

    ind = 0
    while ind >= 0:
        ind = line.find('src="', cur_ind)
        if ind > -1:
            cur_ind = ind + 5
            strt_ind.append(cur_ind)
            ind = line.find('"', cur_ind+1)
            end_ind.append(ind)
            cur_ind = ind + 1
    return strt_ind, end_ind


def add_data_to_line(app_name, line: str, a, b):
    rez = line[0:a[0]]
    for i in range(len(a)):
        old_val = line[a[i]:b[i]]
        new_val = "{% static '" + app_name + "/" + old_val + "' %}"
        rez += new_val
        if i < len(a) - 1:
            rez += line[b[i]:a[i+1]]
    rez += line[b[-1]:-1]
    return rez

if __name__ == '__main__':
    folder = 'D:\\python_projects\\python_django_diploma\\shop\\shop_cite\\templates\\shop_cite\\'
    file_name = 'about.html'
    file = open(folder + 'r' + file_name, 'w', encoding="utf-8")
    file.write('{% load static %}\n')
    with open(folder + file_name, 'r', encoding="utf-8") as f:
        line = f.read()
        a, b = change_line(line)
        if len(a) > 0:
            new_line = add_data_to_line('shop_cite', line, a, b)
            rez_line = new_line
        else:
            rez_line = line
        print(rez_line)
        file.write(rez_line)
    file.close()
