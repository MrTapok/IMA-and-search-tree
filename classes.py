import collections


class PFormula:
    name = ""
    variables = []
    deleted = False
    fulled = False

    def __init__(self, name_str, variables_arr):
        self.name = name_str
        self.variables = variables_arr
        self.deleted = False
        self.fulled = False

    def __lt__(self, other):
        if len(self.variables) == len(other.variables):
            return self.name < other.name
        else:
            return len(self.variables) < len(other.variables)

    def check_fullness(self, var_dict):
        for k in self.variables:
            if var_dict[k] is None:
                return False
        return True

    def get_values(self, var_dict):
        list = []
        for k in self.variables:
            list.append(var_dict[k])
        return list

    def print(self):
        print(self.name + ": ")
        print(self.variables)
        print("\n")


class SFormula:
    name = ""
    consts = []
    deleted = False

    def __init__(self, name_str, const_arr):
        self.name = name_str
        self.consts = const_arr
        self.deleted = False

    def __lt__(self, other):
        if len(self.consts) == len(other.consts):
            return self.name < other.name
        else:
            return len(self.consts) < len(other.consts)

    def __eq__(self, other):
        return self.name == other.name

    def print(self):
        print(self.name)
        print(": ")
        print(self.consts)
        print("\n")


class ClassDescription:
    name = ""

    s_list = []
    p_list = []
    variables_dict = {}

    def get_predicate_names(self):
        temp = {}
        for k in self.s_list:
            if k.name in temp.keys():
                temp[k.name] += 1
            else:
                temp[k.name] = 1
        return temp

    def __init__(self, name, s_list, p_list, variables_dict):
        self.name = name
        self.s_list = s_list
        self.p_list = p_list
        self.variables_dict = variables_dict



