
import sys, re, argparse

parser = argparse.ArgumentParser(description='Generate collocate pairs from tokenised text file (uses line as span)')
parser.add_argument('tok', help='input tok file')
parser.add_argument('out', help='output txt file containing co-freqs')
parser.add_argument('-ee', action='store_true', help='emojis with emojis')
parser.add_argument('-ew', action='store_true', help='emojis with words')

args = parser.parse_args()

progress_count = 0
def progress(message=None):
	global progress_count
	if message:
		sys.stdout.write('\n{}: {}\n'.format(progress_count, message))
		sys.stdout.flush()
	else:
		progress_count += 1
		if progress_count % 100000 == 0:
			sys.stdout.write('| {}\n'.format(progress_count))
			sys.stdout.flush()
		elif progress_count % 10000 == 0:
			sys.stdout.write(':')
			sys.stdout.flush()
		elif progress_count % 1000 == 0:
			sys.stdout.write('.')
			sys.stdout.flush()

def is_emoji(tok):
	return tok.startswith(':') and tok.endswith(':')

emoji_node = args.ee or args.ew
emoji_coll = args.ee

pairs = {}

with open(args.tok, 'r', encoding='utf-8') as f:
	for line in f:
		line = line.strip()
		if line:
			tokens = re.split('\s+', line)
			l = len(tokens)
			for i in range(l):
				ti = tokens[i]
				if (emoji_node and is_emoji(ti)) or (not emoji_node and not is_emoji(ti)):
					for j in range(l):
						tj = tokens[j]
						if (emoji_coll and is_emoji(tj)) or (not emoji_coll and not is_emoji(tj)):
							if i != j:
								pair = ti + '\t' + tj
						
								if not pair in pairs:
									pairs[pair] = 1
								else:
									pairs[pair] += 1
		progress()
	
	progress('finished')

with open(args.out, 'w', encoding='utf-8') as fout:
	for pair in sorted(pairs, key=pairs.get, reverse=True):
		print ('{}\t{}'.format(pairs[pair], pair), file=fout)
