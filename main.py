import re
import csv

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
zagolovok = contacts_list.pop(0)

# разнесение фио в соответствующие им поля
for index, row in enumerate(contacts_list):
  fio = ' '.join(row[:3])
  last_name = fio.split()[0]
  first_name = fio.split()[1]
  surname = fio.split()[2] if len(fio.split()) > 2 else ''
  contacts_list[index][0] = last_name
  contacts_list[index][1] = first_name
  contacts_list[index][2] = surname

# первым проходом приводим телефоны к единообразию в соответствии с заданной маской
pattern = r'^(\+7|8)\D{0,2}(\d{3})\D{0,2}(\d{3})\D?(\d{2})\D?(\d{2})\D*?(\d{4})?'
pattern_comp = re.compile(pattern)
substr = r'+7(\2)\3-\4-\5'
for index, row in enumerate(contacts_list):
  if row[5]:
    contacts_list[index][5] = pattern_comp.sub(substr, row[5])

# вторым проходом добавляем добавочный номер там, где он есть
pattern2 = r'(.{16})\D*(\d{4}).?'
pattern_comp2 = re.compile(pattern2)
substr2 = r'\1 доб.\2'
for index, row in enumerate(contacts_list):
  if len(row[5])>16:
    contacts_list[index][5] = pattern_comp2.sub(substr2, row[5])

# удаление дублирующихся записей осуществляется двумя циклами:
# в первом сохраняется важная информация с миграцией данных
contacts_list = sorted(contacts_list)
for index, row in enumerate(contacts_list):
  if contacts_list[index][0] == contacts_list[index-1][0] and contacts_list[index][1] == contacts_list[index-1][1]:
    for i in range(2, len(zagolovok)):
      if contacts_list[index][i] == '':
        contacts_list[index][i] = contacts_list[index-1][i]

# во втором собственно удаляются дублирующиеся записи.
index = 0
for row in contacts_list:
  if contacts_list[index][0] == contacts_list[index - 1][0] and contacts_list[index][1] == contacts_list[index-1][1]:
    del contacts_list[index-1]
    continue
  index += 1

# код для записи файла в формате CSV
contacts_list.insert(0, zagolovok)
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(contacts_list)