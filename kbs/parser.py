import argparse

def check_args(parser):
    args = parser.parse_args()

    if args.num_results <= 0:
        parser.error("num_results must be an positive integer.")

    return args

def arg_parse():

    # create argument parser object
    parser = argparse.ArgumentParser()

    # add -n argument with default value of 100
    parser.add_argument("-n", "--number", dest="num_results", type=int, default=100,
                        help="the positive integer value (default: 100)")

    # parse the arguments
    return check_args(parser)


# use the value of n in your code
