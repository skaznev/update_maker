



































# n       = int(input())
# i       = 0
# team_A  = ''
# count_A = 0
# team_B  = ''
# count_B = 0
# result = 
# while i < n:
#     s = input().split(';')
#     team_A  = s[0]
#     count_A = int(s[1])
#     team_B  = s[2]
#     count_B = int(s[3])
#     result[team_A] = []
#     if count_A > count_B:
#         #team A - winner!!!
#     if count_A < count_B:
#         #team B - winner!!!
#     if count_A == count_B:
#         #ничья!!!!
    







# Напишите программу, которая принимает на стандартный вход список игр футбольных команд с результатом матча и выводит на стандартный вывод сводную таблицу результатов всех матчей.

# За победу команде начисляется 3 очка, за поражение — 0, за ничью — 1.

# Формат ввода следующий:
# В первой строке указано целое число nn — количество завершенных игр.
# После этого идет nn строк, в которых записаны результаты игры в следующем формате:
# Первая_команда;Забито_первой_командой;Вторая_команда;Забито_второй_командой

# Вывод программы необходимо оформить следующим образом:
# Команда:Всего_игр Побед Ничьих Поражений Всего_очков

# Конкретный пример ввода-вывода приведён ниже.

# Порядок вывода команд произвольный.

# Sample Input:

# 3
# Зенит;3;Спартак;1
# Спартак;1;ЦСКА;1
# ЦСКА;0;Зенит;2
# Sample Output:

# Зенит:2 2 0 0 6
# ЦСКА:2 0 1 1 1
# Спартак:2 0 1 1 1


# n       = 0
# d       = int(input())
# l       = int()
# slovar  = list()
# text    = list()
# ext     = list()

# while n < d:
#     n += 1
#     inp = input()
#     slovar += [inp]

# l       = int(input())
# n       = 0

# while n < l:
#     n += 1
#     inp = input()
#     text += [inp]

# slovar2 = list()
# for item in slovar:
#     slovar2 += [item.lower()]

# for string in text:
#     for item in string.split(' '):
#         if slovar2.count(item.lower()) < 1:
#             if ext.count(item)< 1:
#                 ext += [item]
        
# for i in ext:
#     print(i)





# def hui(text):
#   s = ''
#   ss1 = 0
#   ss2 = 0
#   ss3 = 0
#   row = list()
  
#   for line in lines:
#     n = 0
#     row = line.split(';')
#     for i in range(1,len(row)):
#       n += int(row[i])/3
#       if i == 1:
#         ss1 += int(row[i])/len(lines)
#       if i == 2:
#         ss2 += int(row[i])/len(lines)
#       if i == 3:
#         ss3 += int(row[i])/len(lines)
#     s += str(n) + '\n'
#   s += str(ss1) + ' ' + str(ss2) + ' ' + str(ss3)
#   return (s)
# with open('file.txt', 'r') as file:
#     lines = ''
#     lowlines = ''
#     lines = file.readlines() #line.strip()
#     #lowlines += line.strip().lower()
#     with open ('file2.txt', 'w') as file2:
#         file2.write(hui(lines))










# def hui(text, lowtext):
#     word = ''
#     n = 0 
#     if 'abc' > 'ABC':
#       print ('hui')
#     words = text.split(' ')
#     lowtext = lowtext.split(' ')
#     for item in words:
#       if lowtext.count(item.lower()) > n:
#         n = lowtext.count(item.lower())
#         word = item
#       elif lowtext.count(item.lower()) == n:
#         if item.lower() < word.lower():
#           word = item
#       print ('word = ' + str(word) + ' n = ' + str(n))
#       print ('item = ' + str(item) + ' n = ' + str(lowtext.count(item.lower())))
#     return (word + ' ' + str(n))
# with open('file.txt', 'r') as file:
#     lines = ''
#     lowlines = ''
#     for line in file:        
#         lines += line.strip()
#         lowlines += line.strip().lower()
#     with open ('file2.txt', 'w') as file2:
#         file2.write(hui(lines,lowlines))





# def hui(text):
#     s = ''
#     x = ''
#     n = ''
#     ifnum = False
#     for i in (text + 'a'):
#         print ('i = ' + str(i) + '\nn = ' + str(n))
#         if i >= 'A':
#             print ('string')
#             print (n)
#             if ifnum:
#                 s += x*int(n)
#             ifnum = False
#             x = i
#             continue
#         else:
#             print ('! string')
#             if ifnum != True:
#                 n = i
#             else:
#                 n += i
#             ifnum = True           
#     return (s)
# with open('file.txt', 'r') as file:
#     for line in file:
#         line = line.strip().lower()
#     with open ('file2.txt', 'w') as file2:
#         file2.write(hui(line))