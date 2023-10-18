import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    args = parser.parse_known_args()
    return args[0]