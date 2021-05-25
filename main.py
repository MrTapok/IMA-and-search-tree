import utils
import classes
import algorithm
import multilayer_description
import copy


def main():

    s_list = utils.read_s_list("test_files/s_test.pli")
    p_list, variables_dict = utils.read_p_list_and_dict("test_files/p_test.pli")
    description_list = utils.read_classes("test_files/isomorphism_test.pli")

    temp = utils.sort_p_list(description_list[0].p_list)

    flag, result = algorithm.IMA_first_full(description_list[0].s_list, description_list[4].p_list, description_list[4].variables_dict)

    print(flag)


if __name__ == "__main__":
    main()
