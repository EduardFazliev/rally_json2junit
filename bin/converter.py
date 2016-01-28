import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--source-json', type=str, help='path to json file')
    parser.add_argument('--junit-file', type=str, defaults='output.xml',
                        help='path to result junit file')

    #testing
    args = parser.parse_args()
    print 'source is {}'.format(args.source_json)

if __name__ == '__main__':
    main()