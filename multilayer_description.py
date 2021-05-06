import algorithm
import classes
import copy
import utils


def check_isomorphism(description_1: classes.ClassDescription, description_2: classes.ClassDescription) -> bool:

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

    return result_flag

#def layer_forming(class_description_list):

