import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        help="debug模式运行，热更新",
        dest="debug",
    )
    args = parser.parse_known_args()
    return args[0]