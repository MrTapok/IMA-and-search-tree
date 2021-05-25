import algorithm
import classes
import copy
import utils


def check_isomorphism(description_1: classes.ClassDescription, description_2: classes.ClassDescription):  # проверка на изоморфизм

    names_1 = description_1.get_predicate_names()
    names_2 = description_2.get_predicate_names()

    if names_1.keys() == names_2.keys():
        for k in names_1.keys():
            if names_1[k] != names_2[k]:
                return False
    else:
        return False

    result_flag, result = algorithm.IMA_first_full(description_1.s_list, description_2.p_list, description_2.variables_dict)

    utils.undelete_list(description_1.s_list)

    return result_flag, result


def layer_forming(previous_layer: list, layer_number: int, name = "a"):  # создание нового слоя в графе распознавания
    previous_layer_copy = copy.copy(previous_layer)
    new_layer_nodes = []
    new_layer_edges = {}
    new_layer_names = []

    for i in range(0, len(previous_layer)-1):
        for j in range (i+1, len(previous_layer)):

            flag, new_variables_dict, p_list = algorithm.IMA_first_partial(previous_layer_copy[i].s_list, previous_layer_copy[j].p_list, previous_layer[j].variables_dict) # получаем наибольшую изоморфную
            if flag:

                new_variables_dict_copy_straight = copy.copy(new_variables_dict)  # копия для формирования ребер графа

                for k in new_variables_dict.keys():
                    new_variables_dict[k] = None

                new_name = name + str(layer_number) + str(i) + str(j)  # конструируем имя
                buff_CD = classes.ClassDescription(new_name, utils.from_p_list_to_s_list(p_list), p_list, new_variables_dict)  # конструируем новое описание объекта

                not_isomorphed = True  # проверка на изоморфизм
                for k in new_layer_nodes:

                    iso_result_flag, iso_variables_dict = check_isomorphism(k, buff_CD)

                name_1 = previous_layer_copy[i].name
                name_2 = previous_layer_copy[j].name

                if not_isomorphed: # формируем новые ребра
                    new_layer_nodes.append(buff_CD)

                    if name_1 in new_layer_edges.keys():
                        new_layer_edges[name_1].append({new_name: new_variables_dict_copy_straight})
                    else:
                        new_layer_edges[name_1] = []
                        new_layer_edges[name_1].append({new_name: new_variables_dict_copy_straight})

                    if name_2 in new_layer_edges.keys():
                        new_layer_edges[name_2].append({new_name: utils.dict_roll_over(new_variables_dict_copy_straight)})
                    else:
                        new_layer_edges[name_2] = []
                        new_layer_edges[name_2].append({new_name: utils.dict_roll_over(new_variables_dict_copy_straight)})

    return new_layer_nodes, new_layer_edges, new_layer_names


def multilayer_construction(first_layer): # формирование графа распознавания

    graph_nodes = []
    graph_edges = {}
    graph_names = []

    layer_1 = copy.copy(first_layer)
    layer_2 = []
    i = 1
    while len(layer_1) > 1:
        i += 1
        new_layer_nodes, new_layer_edges, new_layer_names = layer_forming(layer_1, i)
        for k in new_layer_edges.keys():
            graph_edges[k] = new_layer_edges[k]
        graph_nodes.append(new_layer_nodes)
        graph_names.append(new_layer_names)
        layer_1 = copy.copy(new_layer_nodes)

    return  graph_nodes, graph_edges, graph_names