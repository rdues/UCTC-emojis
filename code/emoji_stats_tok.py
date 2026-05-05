
import sys, re, emoji
from collections import Counter

targets_file = sys.argv[1]
output_file = sys.argv[2]

targets = []
with open(targets_file, 'r', encoding='utf-8') as f:
	for line in f:
		line = line.strip()
		if line:
			targets.append(line)

with open(output_file, 'w', encoding='utf-8') as outf:
	emojis = Counter()

	for targ in targets:
		print(targ)
	
		total_tweets = 0
		tweets_with_emoji = 0
		total_tokens = 0
		emoji_count = 0
		
		with open(targ, 'r', encoding='utf-8') as f:
			for line in f:
				line = line.strip()
				if line:
					total_tweets += 1
					has_emoji = False
				
					for m in re.finditer(r':\w+:', line):
						has_emoji = True
						emoji_count += 1
						emojis[m.group(0)] += 1
					
					for token in line.split():
						total_tokens += 1
						
					if has_emoji == True:
						tweets_with_emoji += 1

		print('{}\t{}\t{}\t{}\t{}'.format(total_tweets, tweets_with_emoji, total_tokens, emoji_count, targ), file=outf)

	print()
	for em in sorted(emojis, key=emojis.get, reverse=True):
		u = emoji.emojize(em)
		print('{}\t{}\t{}'.format(emojis[em], em, u), file=outf)
