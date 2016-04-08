import argparse
import sys
import pynliner


parser = argparse.ArgumentParser(
    prog='python -m pynliner',
    description='Pynline HTML+CSS to inline styles')
parser.add_argument('html', metavar='HTMLFILE', type=str,
                    help='the HTML to convert (`-` to read from stdin)')
parser.add_argument('css_files', metavar='CSSFILE', type=open, nargs='*',
                    help='additional CSS files to apply')

args = parser.parse_args()

if args.html == '-':
    source = sys.stdin
else:
    source = open(args.html, 'r')

p = pynliner.Pynliner()
p.from_string(source.read())
for f in args.css_files:
    p.with_cssString(f.read())
sys.stdout.write(p.run())
