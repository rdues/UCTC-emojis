
import sys, re, argparse, math

parser = argparse.ArgumentParser(description='Find coll records for specified node in scored coll files')
parser.add_argument('col', help='input coll file (sorted by scores)')
parser.add_argument('node', help='the node to search for')
parser.add_argument('-ex', nargs='+', action='store', help='types to exclude')
parser.add_argument('-sw', action='store', help='stopwords file')
parser.add_argument('-exhash', action='store_true', help='exclude hashtags')
parser.add_argument('-exnum', action='store_true', help='exclude numbers')

args = parser.parse_args()

search_term = args.node
exclude_terms = args.ex
exclude_hashtags = args.exhash
exclude_numbers = args.exnum

number_re = re.compile(r'\d', re.U)
hashtag_re = re.compile(r'^#', re.U)

stopwords = {}
if args.sw:
	with open(args.sw, 'r', encoding='utf-8') as f:
		for line in f:
			line = line.strip()
			if line:
				stopwords[line.lower()] = True

with open(args.col, 'r', encoding='utf-8') as f:
	for line in f:
		line = line.strip()
		if line:
			score, freq, node_freq, coll_freq, node, coll = line.split('\t')
			if node == search_term:
				if coll in exclude_terms:
					continue
				if coll in stopwords:
					continue
				if exclude_hashtags and hashtag_re.search(coll):
					continue
				if exclude_numbers and number_re.search(coll):
					continue
				print(line)
