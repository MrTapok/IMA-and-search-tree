import classes
import copy


def read_s_list(filename):
    s_list = []
    with open(filename) as f:
        for line in f:
            buff = line.rstrip("\n").split(',')
            s_list.append(classes.SFormula(buff[0], buff[1:]))
    return s_list


def read_p_list_and_dict(filename):
    p_list = []
    set_for_dict = set()

    with open(filename) as f:
        for line in f:
            buff = line.rstrip("\n").split(',')
            p_list.append(classes.PFormula(buff[0], buff[1:]))
            for k in buff[1:]:
                set_for_dict.add(k)
    variables_dict = dict.fromkeys(set_for_dict)
    return p_list, variables_dict


def read_classes(filename):
    name = ""
    s_temp_list = []
    p_temp_list = []
    set_for_dict = set()

    description_list = []

    first_line = True

    with open(filename) as f:
        for line in f:
            if "-" in line:
                if not first_line:

                    description_list.append(classes.ClassDescription(name, s_temp_list, sort_p_list(p_temp_list), dict.fromkeys(set_for_dict)))

                    s_temp_list = []
                    p_temp_list = []
                    set_for_dict = set()
                    name = line.strip("-").strip("\n")
                    continue

                else:
                    name = line.strip("-").strip("\n")
                    first_line = False
                    continue

            buff = line.rstrip("\n").split(',')
            s_temp_list.append(classes.SFormula(buff[0], buff[1:]))
            p_temp_list.append(classes.PFormula(buff[0], buff[1:]))
            for k in buff[1:]:
                set_for_dict.add(k)

    description_list.append(classes.ClassDescription(name, s_temp_list, sort_p_list(p_temp_list), dict.fromkeys(set_for_dict)))

    return description_list


def undelete_list(f_list):  # отмена всех удалений
    for formula in f_list:
        formula.deleted = False


def check_undeleted_list(f_list):  # проверка на то, что в списке остались неудаленные элементы
    for formula in f_list:
        if not formula.deleted:
            return False
    return True


def construct_dict_counter(f_list):  # формирование словаря с количеством переменных входящих в класс с описанием
    f_dict = {}
    for formula in f_list:
        for i in formula.variables:
            if i in f_dict.keys():
                f_dict[i] += 1
            else:
                f_dict[i] = 1
    return f_dict


def get_subdict_by_not_zero(variables_dict, variables_counter_dict):  # выделение подсловаря, если мы удалили значения некоторых переменных целиком
    temp = []
    result = {}

    for i in variables_counter_dict.keys():
        if variables_counter_dict[i] > 0:
            temp.append(i)

    for i in temp:
        result[i] = variables_dict[i]

    return result


def sort_p_list(p_list): # сортировка списка атомарных формул с переменными
    p_list_copy = copy.copy(p_list)
    p_names = {}
    sorted_p_list = []
    sorted_p_names = {}

    for p in p_list_copy:
        if p.name in p_names.keys():
            p_names[p.name] += 1
        else:
            p_names[p.name] = 1

    p_sorted_keys = sorted(p_names, key=p_names.get)
    for w in p_sorted_keys: # сортируем имена по возрастанию количества их вхождений
        sorted_p_names[w] = p_names[w]

    for k in sorted_p_names.keys(): # для каждого имени из списка имен
        for i in range(0, sorted_p_names[k]): # по количеству их вхождений
            temp_formula = None
            for formula in p_list_copy: # забираем формулу из списка и перекладываем ее в отсортированный список
                if formula.name == k:
                    temp_formula = formula
                    sorted_p_list.append(copy.copy(temp_formula))
                    break
            p_list_copy.remove(temp_formula)

    print(len(p_list_copy))

    return sorted_p_list


def sort_s_list(s_list, p_list_sorted): # сортировка списка атомарных формул с константами в соответствии с отсортированным списком с атомарными формулами с переменными
    s_list_copy = copy.copy(s_list)
    s_names = {}
    p_names = []
    sorted_s_list = []

    for p in p_list_sorted:
        if p.name not in p_names:
            p_names.append(p.name)

    print(p_names)

    for s in s_list:
        if s.name in s_names.keys():
            s_names[s.name] += 1
        else:
            s_names[s.name] = 1

    for k in p_names:
        if k not in s_names.keys():
            continue
        for i in range(0, s_names[k]):
            temp_formula = None
            for formula in s_list_copy:
                if formula.name == k:
                    temp_formula = formula
                    sorted_s_list.append(copy.copy(temp_formula))
                    break
            s_list_copy.remove(temp_formula)

    for i in s_list_copy:
        sorted_s_list.append(i)

    return sorted_s_list


def strip_from_unused_names(s_list, p_list):
    s_names = set()
    p_names = set()

    for i in s_list:
        s_names.add(i.name)
    for i in p_list:
        p_names.add(i.name)

    ss_list = []
    pp_list = []

    for i in s_list:
        if i.name in p_names:
            ss_list.append(i)

    for i in p_list:
        if i.name in s_names:
            pp_list.append(i)

    return ss_list, pp_list


def from_p_list_to_s_list(p_list):
    s_list = []

    for k in p_list:
        s_list.append(classes.SFormula(k.name, k.variables))

    return s_list


def dict_roll_over(dict):
    new_dict = {}

    for k in dict.keys():
        new_dict[dict[k]] = k

    return new_dict

