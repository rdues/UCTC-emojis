
import sys, re, argparse, emoji

parser = argparse.ArgumentParser(description='Generate word freqs from tokenised text file')
parser.add_argument('tok', help='input tok file')
parser.add_argument('out', help='output txt file containing the freqs')

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

types = {}
emojis = {}
words = {}
token_count = 0
emoji_count = 0
word_count = 0

with open(args.tok, 'r', encoding='utf-8') as f:
	for line in f:
		line = line.strip()
		if line:
			tokens = re.split('\s+', line)
			l = len(tokens)
			for i in range(l):
				tok = tokens[i]
				
				if not tok in types:
					types[tok] = 1
				else:
					types[tok] += 1
				token_count += 1
				
				if is_emoji(tok):
					if not tok in emojis:
						emojis[tok] = 1
					else:
						emojis[tok] += 1
					emoji_count += 1
				else:
					if not tok in words:
						words[tok] = 1
					else:
						words[tok] += 1
					word_count += 1
		
		progress()
	
	progress('finished')

with open(args.out + '.typ.txt', 'w', encoding='utf-8') as fout:
	print("FREQ\tWORD\tFPM", file=fout)
	for tok in sorted(types, key=types.get, reverse=True):
		fpm = 1000000.0 * types[tok] / token_count
		print ('{}\t{}\t{}'.format(types[tok], tok, fpm), file=fout)

with open(args.out + '.wd.txt', 'w', encoding='utf-8') as fout:
	print("FREQ\tWORD\tFPM", file=fout)
	for tok in sorted(words, key=words.get, reverse=True):
		fpm = 1000000.0 * words[tok] / token_count
		print ('{}\t{}\t{}'.format(words[tok], tok, fpm), file=fout)

with open(args.out + '.em.txt', 'w', encoding='utf-8') as fout:
	print("FREQ\tWORD\tFPM\tEXTRA", file=fout)
	for tok in sorted(emojis, key=emojis.get, reverse=True):
		fpm = 1000000.0 * emojis[tok] / token_count
		em = emoji.emojize(tok)
		print ('{}\t{}\t{}\t{}'.format(emojis[tok], tok, fpm, em), file=fout)

print ('Token count: {}'.format(token_count))
print ('Word count: {}'.format(word_count))
print ('Emoji count: {}'.format(emoji_count))

