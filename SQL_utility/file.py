













a = 1
cut = 999998    # 1 строка будет пустая, и еще одна уйдет на заголовок
def pizda(x, y, z):
    if x < y-1:
        return cut
    return z%cut

with open(r'C:/projects/update_maker/SQL_utility/text.txt', 'r', encoding= 'Windows-1251') as File_post:
    # читаем быстро кол-во строк в файле
    lenght = sum(1 for line in File_post)
    # поставим курсор в начало файла, так как он сьехал вконец на строке выше
    File_post.seek(0, 0)
    fract_all = lenght//cut + 1
    if lenght >= cut:    # Если строк больше 1млн то дробим файл на части
        for i in range(fract_all):     
            fract = [next(File_post) for x in range(pizda(i, fract_all, lenght))]
            with open(r'C:/projects/update_maker/SQL_utility/text_' + str(i) + r'.txt', 'w', encoding= 'Windows-1251') as File_pre:
                for o in fract:
                    File_pre.write(o)

    