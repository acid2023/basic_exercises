import re


def check_operators(operands):
    if not isinstance(operands, str):
        return True
    if operands[0] in '/*' or operands[-1] in '+/*-' or (operands[0] == '-' and operands[1] in '+/*') or (operands[0] == '+' and operands[1] in '+-/*'):
        return False
    return True


def execute_calculation(a, b, operator):
    if not check_operators(a) or not check_operators(b):
        return 'ERROR - hanging operators or oerators before numbers are not allowed2'
    try:
        a = float(a)
        b = float(b)
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            return a / b
        elif operator == '^':
            return a ** b
    except ValueError:
        return 'ERROR - incorrect values entered'
    except ZeroDivisionError:
        return 'ERROR - cannot divide by zero'
    except OverflowError:
        return '    ERROR - unfortunately the result is too large'
    except:
        if isinstance(a, complex) or isinstance(b, complex):
            print('WATNING! Complex numbers')
        return "ERROR - something went wrong, please contact the development team with bugz' report"


def substitute(list, i, char):
    a = list[i-1]
    b = list[i+1]
    del list[i+1]
    del list[i-1]
    list[i-1] = execute_calculation(a, b, char)
    return list


def utilize_minus(input_list):
    work_list = input_list.copy()
    length = len(input_list)
    if length == 2 and isinstance(input_list[1], str):
        return ['-' + input_list[1]]
    elif length == 2:
        return [-input_list[1]]
    number_pattern = r'\d*\.?\d+'
    for i, v in enumerate(input_list):
        if v == '-' and i == 0:
            if isinstance(input_list[1], str):
                work_list[1] = '-' + work_list[1]
            else:
                work_list[1] = - work_list[1]
            work_list[0] = ''
            continue
        elif v == '-' and i != length:
            if not (re.fullmatch(number_pattern, input_list[i + 1]) is None):
                if isinstance(work_list[i+1], str):
                    work_list[i + 1] = float('-' + work_list[i + 1])
                else:
                    work_list[i + 1] = - work_list[i + 1]
                work_list[i] = ''
    result = [item for item in work_list if item != '']
    print(result)
    return result


def calculate_string(string):
    operator_pattern = r'[\+\*/\^\-]'
    number_pattern = r'\d*\.?\d+'
    matches1 = [(match.group(), match.start()) for match in re.finditer(number_pattern, string)]
    matches2 = [(match.group(), match.start()) for match in re.finditer(operator_pattern, string)]
    combined_match = [match[0] for match in sorted(matches1 + matches2, key=lambda x: x[1])]
    if combined_match[0] in ['/', '*', '^'] or combined_match[-1] in ['+', '-', '/', '*', '^']:
        return 'ERROR - hanging operators before numbers are not allowed'
    elif combined_match[0] == '+':
        del combined_match[0]
    working_list = utilize_minus(combined_match)
    while True:
        new_working_list = working_list.copy()
        if len(working_list) == 1:
            try:
                result = float(working_list[0])
            except:
                result = working_list[0]
            break
        if any(char == '^' for char in working_list):
            for i, char in enumerate(working_list):
                if char == '^':
                    new_working_list = substitute(new_working_list, i, char)
                    break
        elif any(char in ['/', '*'] for char in working_list):
            for i, char in enumerate(working_list):
                if char in ['/', '*']:
                    new_working_list = substitute(new_working_list, i, char)
                    break
        elif any(char == '+' for char in working_list):
            for i, char in enumerate(working_list):
                if char == '+':
                    new_working_list = substitute(new_working_list, i, char)
                    break
        else:
            for i, char in enumerate(working_list):
                if char == '-' and i != 0:
                    new_working_list = substitute(new_working_list, i, char)
                    break
            if len(working_list) >= 2:
                for i, v in enumerate(working_list):
                    working_list[i] = float(v)
                return sum(working_list)
        working_list = new_working_list
    return result


def parenthesis_check(string):
    open_par = 0
    close_par = 0
    for char in string:
        if char == '(':
            open_par += 1
        elif char == ')':
            close_par += 1
    return open_par == close_par


test = r'^[0-9\*\-\+/\^\(\)\. ]+$'
forbidden_pattern = r'\d\s+\d'
operator_pattern = r'[\*\/][/\+\*\^]|^[\*/]'
parenthesis_test = r'[\+\-\*/\^]$'
print('\n\n')
print('welcome to python calculator.\n"+", "-", "/", "*" or "^" operators are supported.\nfloats and ints are supported.\nno spaces without operators between numbers are allowed.\nno hanging operators allowed: "/", "*" or "^" before the number or "+", "-", "/", "*" or "^" after the number will not be calculated.\n"--"is "+", "++" is "+" and "+-" or "-+" is "-".\nnumbers can be written as ".66", "0.66", "+.66", or "+0.66".\DISCLAIMER: complex numbers (a + b*1j) handling may be treated with errors!')
while True:
    print('\n\n')
    string = input('\ninput your expression: \n')
    if re.search(forbidden_pattern, string):
        print('ERROR - spaces between numbers without operator are not allowed')
        continue
    string = string.replace(' ', '')
    if re.search(operator_pattern, string):
        print('ERROR - two operators in a row are not allowed')
        continue
    string = string.replace('--', '+')
    string = string.replace('++', '+')
    string = string.replace('-+', '-')
    string = string.replace('+-', '-')
    string = string.replace('^+', '^')
    string = string.replace('*+', '*')
    break_cycle = False
    if not re.search(test, string):
        print('ERROR - incorrect input - only numbers, "(" and ")" and "+", "-", "/", "*" or "^" are allowed')
        break_cycle = False
        continue
    if not parenthesis_check(string):
        print('ERROR - the parenthesis should go in pairs - openning "(" and closing ")"')
        break_cycle = True
        continue
    while True:
        i = 0
        parentheses_end = 0
        parentheses_start = 0
        length = len(string)
        for i in range(length):
            if string[length - 1 - i] == ')':
                parentheses_end = length - 1 - i
            elif parentheses_end == -1:
                continue
            elif string[length - 1 - i] == '(':
                parentheses_start = length - i - 1
                break
            i += 1
        if parentheses_end != 0 and parentheses_start != 0:
            if string[0] != '(' and not re.search(parenthesis_test, string[: parentheses_start]):
                print('ERROR - there should be an operator before or between the parentheses')
                break_cycle = True
                break
            string_in_parentheses = string[parentheses_start + 1: parentheses_end]
            substitution_value = calculate_string(string_in_parentheses)
            if isinstance(substitution_value, str):
                print(substitution_value)
                break_cycle = True
            new_string = string[: parentheses_start] + str(substitution_value) + string[parentheses_end+1:]
            string = new_string
            print(string)
        else:
            break
        if break_cycle:
            break
    if not break_cycle:
        result = calculate_string(string)
        print(f'result: \n{result}')
