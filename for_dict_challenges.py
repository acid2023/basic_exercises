# Задание 1
# Дан список учеников, нужно посчитать количество повторений каждого имени ученика
# Пример вывода:
# Вася: 1
# Маша: 2
# Петя: 2
print('test 1')
students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Петя'},
]
# ???
students_rep_list = {record['first_name']: 0 for record in students}
for record in students:
    student_name = record['first_name']
    students_rep_list[student_name] += 1
for record in students_rep_list:
    print(f'{record}: {students_rep_list[record]}')

# Задание 2
# Дан список учеников, нужно вывести самое часто повторящееся имя
# Пример вывода:
# Самое частое имя среди учеников: Маша
print('test 2')
students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Оля'},
]
# ???


def get_most_frequent_name(students):
    students_rep_list = {record['first_name']: 0 for record in students}
    for record in students:
        students_rep_list[record['first_name']] += 1
    max_name_frequency = max(students_rep_list.values())
    for record in students_rep_list:
        if students_rep_list[record] == max_name_frequency:
            return record


print(f'Самое частое имя среди учеников: {get_most_frequent_name(students)}')

print('test 3')
# Задание 3
# Есть список учеников в нескольких классах, нужно вывести самое частое имя в каждом классе.
# Пример вывода:
# Самое частое имя в классе 1: Вася
# Самое частое имя в классе 2: Маша

school_students = [
    [  # это – первый класс
        {'first_name': 'Вася'},
        {'first_name': 'Вася'},
    ],
    [  # это – второй класс
        {'first_name': 'Маша'},
        {'first_name': 'Маша'},
        {'first_name': 'Оля'},
    ], [  # это – третий класс
        {'first_name': 'Женя'},
        {'first_name': 'Петя'},
        {'first_name': 'Женя'},
        {'first_name': 'Саша'},
    ],
]
# ???
i = 1
for school_class in school_students:
    print(f'Самое частое имя в классе {i}: {get_most_frequent_name(school_class)}')
    i += 1

# Задание 4
# Для каждого класса нужно вывести количество девочек и мальчиков в нём.
# Пример вывода:
# Класс 2a: девочки 2, мальчики 0
# Класс 2б: девочки 0, мальчики 2

print('test 4')
school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '2б', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
    {'class': '2б', 'students': [{'first_name': 'Даша'}, {'first_name': 'Олег'}, {'first_name': 'Маша'}]},
]
is_male = {
    'Олег': True,
    'Маша': False,
    'Оля': False,
    'Миша': True,
    'Даша': False,
}
# ???


def get_class_gender(school):
    for school_class in school:
        number_of_boys = 0
        number_of_girls = 0
        for student in school_class['students']:
            if is_male[student['first_name']]:
                number_of_boys += 1
            else:
                number_of_girls += 1
            school_class['boys'] = number_of_boys
            school_class['girls'] = number_of_girls
    return school


school = get_class_gender(school)
for school_class in school:
    school_class_name = school_class['class']
    number_of_boys = school_class['boys']
    number_of_girls = school_class['girls']
    print(f' Класс {school_class_name}: мальчики {number_of_boys}, девочки {number_of_girls}')

# Задание 5
# По информации о учениках разных классов нужно найти класс, в котором больше всего девочек и больше всего мальчиков
# Пример вывода:
# Больше всего мальчиков в классе 3c
# Больше всего девочек в классе 2a
print('test 5')
school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '3c', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
]
is_male = {
    'Маша': False,
    'Оля': False,
    'Олег': True,
    'Миша': True,
}
# ???
school = get_class_gender(school)
number_of_boys = -1
number_of_girls = -1
for school_class in school:
    if number_of_girls < school_class['girls']:
        number_of_girls = school_class['girls']
        girl_class = school_class['class']
    if number_of_boys < school_class['boys']:
        number_of_boys = school_class['boys']
        boys_class = school_class['class']
print(f'Больше всего мальчиков в классе {boys_class} - {number_of_boys}')
print(f'Больше всего девочек в классе {girl_class} - {number_of_girls}')
