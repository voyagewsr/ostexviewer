#!/usr/local/bin/python3

import sys
import getopt
import exercise


def main(argv):
    system = 'qa'
    exercise_url = 'https://exercises-%s.openstax.org' % system
    path = '/api/exercises?q='
    bypass_html = False
    build_csv = False
    csv_name = 'ex_list.csv'
    try:
        opts, args = getopt.getopt(argv, "b:s:a:i:hc:", ["book=", "system=",
                                   "address=", "id=", "nohtml", "csv="])
    except getopt.GetoptError:
        usage()
        return
    for opt, arg in opts:
        if opt in ('-s', '--system'):
            if str(arg).lower() in ['prod', 'production', 'tutor']:
                print('Using [exercises.openstax.org]')
                exercise_url = 'https://exercises.openstax.org'
            else:
                print('Using [exercises-%s.openstax.org]' % str(arg).lower())
                exercise_url = 'https://exercises-%s.openstax.org' % \
                    str(arg).lower()
        elif opt in ('-a', '--address'):
            print('Using [%s]' % arg)
            exercise_url = '%s' % arg
            path = ''
        elif opt in ('-i', '--id'):
            print('Accessing exercise [%s]' % str(arg).lower())
            path = '/api/exercises?q=tag:%s' % str(arg).lower()
        elif opt in ('-h', '--nohtml'):
            print('Bypassing HTML')
            bypass_html = True
        elif opt in ('-b', '--book'):
            print('Pulling assessments for [%s]' % str(arg).lower())
            path = '/api/exercises?q=tag:%s' % str(arg).lower()
        elif opt in ('-c', '--csv'):
            csv_name = str(arg).lower()
            csv_name = 'ex_list.csv' if csv_name == '' or csv_name is None \
                else csv_name
            print('Build CSV: %s' % csv_name)
            build_csv = True
        else:
            usage()
            return
    a = exercise.Portfolio()
    a.import_exercises('%s%s' % (exercise_url, path))
    if not bypass_html:
        a.to_html(5)
    if build_csv:
        a.to_csv(filename=csv_name, tag_types=['-ex', '-ot'])


def usage():
    print('Exercises Remote Pulling')
    print('  -s  --system=         Use a specific server instance to pull')
    print('                        default=qa')
    print('  -a  --address=        Use a specific IP to pull')
    print('  -i  --id=             Pull a single exercise')
    print('  -h  --nohtml          Do not build the HTML view page')
    print('  -c  --csv=            Build a CSV of Number@Version and Ex-IDs')
    print('                        default=ex_list.csv')

if __name__ == "__main__":
    main(sys.argv[1:])
