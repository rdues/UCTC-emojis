
import sys, re, argparse, math, emoji, random

parser = argparse.ArgumentParser(description='Find concs from txt file')
parser.add_argument('txt', help='the file to search')
parser.add_argument('terms', nargs='+', help='the term to search for')
parser.add_argument('-shuf', action='store_true', help='shuffle concs')


args = parser.parse_args()

search_pats = []
num_terms = len(args.terms)
out_filename = ''

for term in args.terms:
	pat = None
	if term[0] == ':' and term[-1] == ':':
		out_filename += '-' + term[1:-1]
		term = emoji.emojize(term)
		pat = re.compile(term, flags=re.U | re.I)
	else:
		out_filename += '-' + term
		pat = re.compile(r'\b' + term + r'\b', flags=re.U | re.I)
	search_pats.append(pat)

print('PAT {}'.format(search_pats))
print('OUT {}'.format(args.txt + '.concs' + out_filename + '.htm'))

matches = []

with open(args.txt, 'r', encoding='utf-8') as f:
	for line in f:
		line = line.strip()
		match_count = 0
		for pat in search_pats:
			if pat.search(line):
				match_count += 1
		if match_count == num_terms:
			matches.append(line)

random.shuffle(matches)

with open(args.txt + '.concs' + out_filename + '.htm', 'w', encoding='utf8') as fout:
	print('<html><body><pre>', file=fout)
		
	for match in matches:
		print('', file=fout)
		print(match, file=fout)
	
	print('</pre></body></html>', file=fout)

