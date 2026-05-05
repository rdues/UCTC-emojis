
import sys, re, argparse, math, emoji

parser = argparse.ArgumentParser(description='Generate coll stats from freq info')
parser.add_argument('typ', help='input type list file')
parser.add_argument('col', help='input coll pair file')
parser.add_argument('out', help='output file')
parser.add_argument('-spansize', action='store', default=1, help='span size (will not be changed regarding direction)')
parser.add_argument('-corpsize', action='store', default=0, help='size of the corpus in tokens (default is to calcualte from the type list)')
parser.add_argument('-minfreq', action='store', default=4, help='min co freq')
parser.add_argument('-minscore', action='store', default=2.0, help='min score')

args = parser.parse_args()

class Coll:
	node = ''
	coll = ''
	co_freq = 0.0
	score = 0.0

def calc_zscore(co_freq, node_freq, coll_freq, corp_size, span_size):
	expected = span_size * node_freq * (coll_freq / corp_size)
	if expected != 0.0:
		expected = expected / (1.0 - math.exp(-expected))
	return (co_freq - expected) / math.sqrt(expected)


spansize = float(args.spansize)
corpsize = float(args.corpsize)
calc_corpsize = False
if corpsize == 0.0:
	calc_corpsize = True
min_freq = float(args.minfreq)
min_score = float(args.minscore)
	
types = {}

with open(args.typ, 'r', encoding='utf-8') as f:
	next(f)
	for line in f:
		line = line.strip()
		if line:
			l = line.split('\t')
			freq = l[0]
			s = l[1]
			f = float(freq)
			types[s] = f
			if calc_corpsize:
				corpsize += f

print('Corp size: {}'.format(corpsize))
print('Span size: {}'.format(spansize))
print('Min co freq: {}'.format(min_freq))
print('Min score: {}'.format(min_score))

colls = []

with open(args.col, 'r', encoding='utf-8') as f:
	for line in f:
		line = line.strip()
		if line:
			freq, node, coll = line.split('\t')
			co_freq = float(freq)
			if co_freq >= min_freq:
				score = calc_zscore(co_freq, types[node], types[coll], corpsize, spansize)
				if score >= min_score:
					c = Coll()
					c.node = node
					c.coll = coll
					c.co_freq = co_freq
					c.score = score
					colls.append(c)

colls.sort(key=lambda x: x.score, reverse=True)

with open(args.out, 'w', encoding='utf-8') as fout:
	print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format('SCORE', 'CO_FREQ', 'NODE_FREQ', 'COLL_FREQ', 'NODE', 'COLL', 'EM_N', 'EM_C'), file=fout)
	for c in colls:
		em_n = ''
		if c.node.startswith(':') and c.node.endswith(':'):
			em_n = emoji.emojize(c.node)
		em_c = ''
		if c.coll.startswith(':') and c.coll.endswith(':'):
			em_c = emoji.emojize(c.coll)
		print ('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(c.score, c.co_freq, types[c.node], types[c.coll], c.node, c.coll, em_n, em_c), file=fout)
