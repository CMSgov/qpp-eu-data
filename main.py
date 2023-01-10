import argparse
import logging as logger

from processors.generator import Generator
from processors.scanner import Scanner
from processors.utils import Config

logger.basicConfig(level='INFO',
                    format='%(levelname).1s %(asctime)s %(filename)s:%(lineno)s [%(funcName)s] %(message)s')

PROCESSORS = ['scanner', 'generator']

def execute_processor(config, args):
    if args.processor == 'scanner':
        scanner = Scanner(config)
        scanner.scan()
    elif args.processor == 'generator':
        generator = Generator(config, args.year)
        generator.generate()

def main():
    config = Config()
    years = list(config.get('generator'))
    default_year = max(years)

    parser = argparse.ArgumentParser(description='Run a processor for the given year')
    parser.add_argument('-p', '--processor', choices=PROCESSORS, default='scanner', help='processor to be run, default: scanner')
    parser.add_argument('-y', '--year', choices=years, default=default_year, help='year used by the processor, default: most recent configured year')
    args = parser.parse_args()
    
    execute_processor(config, args)

if __name__=='__main__':
    main()
