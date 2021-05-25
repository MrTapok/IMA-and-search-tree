import copy
import utils


def solve(s_formula, p_formula, variables_dict):
    new_variables_dict = copy.copy(variables_dict)
    variables = p_formula.variables
    s_values = s_formula.consts

    for i in range(0, len(variables)):
        if new_variables_dict[variables[i]] is None or new_variables_dict[variables[i]] == s_values[i]:
            new_variables_dict[variables[i]] = s_values[i]
        else:
            return False, {}

    check = [i for i in new_variables_dict.values() if i]

    if len(set(check)) < len(check): # проверка на то, не присвоили ли мы одно и то же значение разным переменным
        return False, {}

    return True, new_variables_dict


def check_f_collection(s_list, p_list, variables_dict):
    result = 0  # 0 - продолжаем, 1 - тупиковый, 2 - пустой; продолжаем, пока не тупиковый
    if not (None in variables_dict.values()):  # если словарь полный, значит список либо пустой, либо тупиковый
        result = 2  # пустой, пока не тупиковый

    for p_formula in p_list:
        if p_formula.deleted:  # если удалили формулу в течение работы IMA, проверять её не надо
            continue

        p_values = p_formula.get_values(variables_dict) # достаем значения
        find = False
        if not(None in p_values):  # если формула заполнена, только тогда проверяем
            for s_formula in s_list:
                if len(s_formula.consts) == len(p_values) and s_formula.name == p_formula.name:  # совпадение имени и длины ведет к проверке значений
                    s_values = s_formula.consts
                    if p_values == s_values:
                        find = True
                        break
                else:
                    if len(s_formula.consts) > len(p_values):
                        break
        else:
            continue

        if not find:
            return 1  # если не нашли, значит тупиковый в любом случае
    return result


def IMA_first_full(ss_list, p_list, variables_dict):

    s_list = utils.sort_s_list(ss_list, p_list)

    dict_buffer = [copy.copy(variables_dict)]
    deleted_formulas_buffer = []  # формулы сейчас удаленные для всех
    deleted_dict = {}  # словарь с формулами удаленными для конкретных формул

    for p_formula in p_list:
        deleted_dict[p_formula] = []

    while True:

        if utils.check_undeleted_list(s_list):
            return False, {}

        for p_formula in p_list:
            # print(p_formula.variables)
            name_exist = False  # флаг для прерывания, если формулы решающей систему не существует
            name_found = False  # флаг для прерывания, если больше имен нет

            if not p_formula.check_fullness(dict_buffer[-1]) and not p_formula.deleted:  # Если мы нашли формулу, которая не удалена и список её переменных не заполнен, можем искать продолжение решения

                for s_formula in s_list:  # просматриваем список формул с константами
                    # print(s_formula.consts)

                    if p_formula.name == s_formula.name and ((s_formula in deleted_dict[p_formula]) or (s_formula in deleted_formulas_buffer)):  # если формула с таким именем уже была, но ее удалили, запоминаем существование имени
                        name_found = True
                        name_exist = True

                    if p_formula.name == s_formula.name and not (s_formula in deleted_dict[p_formula]) and not (s_formula in deleted_formulas_buffer):  # нашли неудаленную формулу в теории подходящую к решению
                        deleted_dict[p_formula].append(s_formula)  # пометили её как удаленную для этой формулы
                        deleted_formulas_buffer.append(s_formula)
                        name_found = True  # написали что такое имя существует
                        name_exist = True
                        flag, new_variables = solve(s_formula, p_formula, dict_buffer[-1])

                        if not flag:
                            continue
                        else:
                            dict_buffer.append(new_variables)

                        collection_status = check_f_collection(s_list, p_list, dict_buffer[-1])  # Проверка того, что стало со списком, после того, как мы получили новые значения

                        if collection_status == 0:  # Если еще есть формулы с переменными - продолжаем
                            # print(dict_buffer[-1])
                            break

                        if collection_status == 1:  # Если тупиковый - отменяем удаление или уходим
                            if len(dict_buffer) > 1:
                                dict_buffer.pop()
                                deleted_formulas_buffer.pop()
                            else:
                                return False, {}

                        if collection_status == 2:  # Если пустой - всё хорошо, возвращаем результат
                            return True, dict_buffer[-1]

                    else:
                        if p_formula.name != s_formula.name and name_found:  #  срабатывает, если мы для текущей формулы с переменными перебрали все формулы с константами, с совпадающими именами
                            return False, {}
                            #if len(dict_buffer) > 1:
                            #    dict_buffer.remove(-1)
                            #    formula_doesnt_exist = True
                            #    break
                            #else:
                            #    return False, {}

                if not name_exist:  # срабатывает, если мы перебрали весь список формул с константами и не нашли ни одного подходящего предиката
                    return False, {}


def IMA_first_partial(sss_list, pp_list, variables_dict_1):

    ss_list, p_list = utils.strip_from_unused_names(sss_list, pp_list) # убираем имена, которые точно не будут использованы
    s_list = utils.sort_s_list(ss_list, p_list) # сортируем атомарные формулы с константами в в соответствии с порядком переменных
    variables_counter = utils.construct_dict_counter(p_list) # выделяем количество переменных
    variables_dict = utils.get_subdict_by_not_zero(variables_dict_1, variables_counter) # на случай если ушли какие-то переменные
    dict_buffer = [copy.copy(variables_dict)]

    p_deleted = False

    while True:
        if p_deleted: # если мы вернулись в цикл с удалением формулы из p_list, нам необходимо убрать все пометки об удалениях из s_list и на всякий случай взять подмножество словаря с переменными
            utils.undelete_list(s_list)
            dict_buffer = [utils.get_subdict_by_not_zero(variables_dict, variables_counter)]

        if utils.check_undeleted_list(p_list):  # если все формулы закончились - то нет смысла идти дальше
            return False, {}, []

        p_deleted = False

        for p_formula in p_list:
            # print(p_formula.variables)
            # флаг для возврата, если формулы решающей систему не существует
            name_found = False  # флаг для возврата, если больше имен нет

            if not p_formula.check_fullness(dict_buffer[
                                                -1]) and not p_formula.deleted:  # Если мы нашли формулу, которая не удалена и список её переменных не заполнен, можем искать продолжение решения

                for s_formula in s_list:  # просматриваем список формул с константами
                    # print(s_formula.consts)

                    if p_formula.name == s_formula.name and s_formula.deleted:  # если формула с таким именем уже была, но ее удалили, запоминаем существование имени
                        name_found = True

                    if p_formula.name == s_formula.name and not s_formula.deleted:  # нашли неудаленную формулу в теории подходящую к решению
                        s_formula.deleted = True  # пометили её как удаленную
                        name_found = True  # написали что такое имя существует
                        flag, new_variables = solve(s_formula, p_formula, dict_buffer[-1])

                        if not flag:
                            continue
                        else:
                            dict_buffer.append(new_variables)

                        collection_status = check_f_collection(s_list, p_list, dict_buffer[
                            -1])  # Проверка того, что стало со списком, после того, как мы получили новые значения

                        if collection_status == 0:  # Если еще есть формулы с переменными - продолжаем
                            # print(dict_buffer[-1])
                            break

                        if collection_status == 1:  # Если тупиковый - отменяем удаление или уходим
                            if len(dict_buffer) > 1:
                                dict_buffer.pop()
                            else:
                                p_formula.deleted = True
                                for i in p_formula.variables:
                                    variables_counter[i] -= 1
                                break

                        if collection_status == 2:  # Если пустой - всё хорошо, возвращаем результат
                            return True, dict_buffer[-1], p_list

                    else:
                        if p_formula.name != s_formula.name and name_found:  # срабатывает, если мы для текущей формулы с переменными перебрали все формулы с константами, с совпадающими именами
                            if len(dict_buffer) > 1:
                                dict_buffer.remove(-1)
                                break
                            else:
                                p_formula.deleted = True
                                for i in p_formula.variables:
                                    variables_counter[i] -= 1
                                break
                # выход из цикла по S

                if p_deleted: # если мы вышли из цикла удалением атомарной формулы с переменными
                    break

            # выход из цикла по P





