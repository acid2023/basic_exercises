print('test 1')
# Вывести последнюю букву в слове
word = 'Архангельск'
# ???
print(word[-1])

print('test 2')
# Вывести количество букв "а" в слове
word = 'Архангельск'
# ???
letter = 'а'
print(f'С учетом регистра в слове {word} букв "а" - {word.count(letter)}')
print(f'Без учета регистра в слове {word} букв "а" - {word.lower().count(letter)}')
# Вывести количество гласных букв в слове
print('test 3')
word = 'Архангельск'
# ???
vowels = {'а', "о", "е", "и", "у", "э", "ю", "я", "ё"}
vowel_quantity = 0
for letter in word:
    if letter in vowels:
        vowel_quantity += 1
print(f'В слове {word} количество гласных букв {vowel_quantity}')

#Алтернативный вариант
print(f'В слове {word} количество гласных букв {len([letter for letter in word if letter in vowels])}')

print('test 4')
# Вывести количество слов в предложении
sentence = 'Мы приехали в гости'
# ???
print(len(sentence.split()))

# Вывести первую букву каждого слова на отдельной строке
sentence = 'Мы приехали в гости'
# ???
for word in sentence.split():
    print(word[0])


print('test 5')
# Вывести усреднённую длину слова в предложении
sentence = 'Мы приехали в гости'
# ???
total_letters = 0
words = len(sentence.split())
for word in sentence.split():
    total_letters += len(word)
print(f'Средняя длина слова в предложении "{sentence}" - {total_letters/words}')
