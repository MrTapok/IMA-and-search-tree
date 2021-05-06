import utils
import classes
import algorithm
import multilayer_description
import copy


def main():

    s_list = utils.read_s_list("test_files/s_test.pli")
    p_list, variables_dict = utils.read_p_list_and_dict("test_files/p_test.pli")

    description_list = utils.read_classes("test_files/sorting_test.pli")

    temp = utils.sort_p_list(description_list[0].p_list)

    #for k in temp:
    #    classes.PFormula.print(k)

    for k in utils.sort_s_list(description_list[1].s_list, temp):
        classes.SFormula.print(k)



if __name__ == "__main__":
    main()
