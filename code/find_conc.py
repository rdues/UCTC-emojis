
import sys, re, argparse, math, emoji
sys.stdout.reconfigure(encoding='utf-8')

parser = argparse.ArgumentParser(description='Find concs from txt file')
parser.add_argument('targets', help='the file containing files to search')
parser.add_argument('terms', nargs='+', help='the term to search for')

args = parser.parse_args()

search_pats = []
num_terms = len(args.terms)

for term in args.terms:
	pat = None
	if term[0] == ':' and term[-1] == ':':
		term = emoji.emojize(term)
		pat = re.compile(term, flags=re.U | re.I)
	else:
		pat = re.compile(r'\b' + term + r'\b', flags=re.U | re.I)
	search_pats.append(pat)

targets = []
with open(args.targets, 'r', encoding='utf-8') as f:
	for line in f:
		line = line.strip()
		if line:
			targets.append(line)

for targ in targets:
	with open(targ, 'r', encoding='utf-8') as f:
		for line in f:
			line = line.strip()
			match_count = 0
			for pat in search_pats:
				if pat.search(line):
					match_count += 1
			if match_count == num_terms:
				print(targ, '\t', line)
