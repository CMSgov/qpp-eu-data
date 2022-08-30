import argparse
import logging as logger

from processors.generator import Generator
from processors.utils import Config

logger.basicConfig(level='INFO',
                    format='%(levelname).1s %(asctime)s %(filename)s:%(lineno)s [%(funcName)s] %(message)s')

def main():
    """
    Generates and publishes EUC county zipcode walkthrough file.
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', '--year', default=2022)
    args = parser.parse_args()
    config = Config()
    generator = Generator(config, args.year )
    generator.generate()


if __name__=='__main__':
    main()
