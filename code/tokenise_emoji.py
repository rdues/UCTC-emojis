
import sys, re, pprint, argparse
import spacy
from spacy.language import Language
from spacy.matcher import Matcher
from spacy.tokens import Token
from spacymoji import Emoji

parser = argparse.ArgumentParser(description='Tokenise txt file')
parser.add_argument('txt', help='input txt file')
parser.add_argument('-lang', action='store', default='en', help='language (en, de)')

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

entities = {
	'&amp;': '&',
	'&apos;': "'",
	'&lt;': '<',
	'&gt;': '>',
	'&quot;': '"'
}
def rep_entity(m):
	if m.group(0) in entities:
		return entities[m.group(0)]
	else:
		print('Entity {} not recognised.'.format(m.group(0)))
		return m.group(0)
entity_re = re.compile(r'&\w+;', flags=re.U & re.I)
translit_table = str.maketrans({
	# spaces
	'\u0009': ' ',
	'\u000B': ' ',
	'\u000C': ' ',
	'\u00A0': ' ',
	'\u2000': ' ',
	'\u2001': ' ',
	'\u2002': ' ',
	'\u2003': ' ',
	'\u2004': ' ',
	'\u2005': ' ',
	'\u2006': ' ',
	'\u2007': ' ',
	'\u2008': ' ',
	'\u2009': ' ',
	'\u200A': ' ',
	'\u200B': ' ',
	'\u202F': ' ',
	'\u205F': ' ',
	'\u3000': ' ',
	'\uFEFF': ' ',
	# apostrophes
	'\u0091': '\'',
	'\u0092': '\'',
	'\u00B4': '\'',
	'\u02BC': '\'',
	'\u02CD': '\'',
	'\u2018': '\'',
	'\u2019': '\'',
	'\u201A': '\'',
	'\u201B': '\'',
	'\u0060': '\'',
	# hyphens
	'\u00AD': '-',
	'\u058A': '-',
	'\u1806': '-',
	'\u2010': '-',
	'\u2011': '-',
	'\u2012': '-',
	'\u2013': '-',
	'\u2014': '-',
	'\u2015': '-',
	'\u207B': '-',
	'\u208B': '-',
	'\u2212': '-',
})
def clean_text(text):
	text = entity_re.sub(rep_entity, text)		# replace xml entities
	text = text.translate(translit_table)		# convert spaces, hyphens and apostrophes
	text = ' '.join(text.split())				# remove multiple spaces
	return text

nlp = None
if args.lang == 'en':
	nlp = spacy.load('en_core_web_lg')
elif args.lang == 'de':
	nlp = spacy.load('de_core_news_md')

if nlp == None:
	sys.exit('Error: no language model loaded\n')

	
hashtag_re = re.compile(r'#\w+', flags=re.I & re.U)
@Language.component("rdues_hashtag")
def hashtag_pipe(doc):
	for m in hashtag_re.finditer(doc.text):
		start, end = m.span()
		span = doc.char_span(start, end)
		if span is not None:
			with doc.retokenize() as retokenizer:
				retokenizer.merge(span)
	return doc

alphanum_re = re.compile(r'\w', flags=re.I & re.U)
@Language.component("rdues_alphanum")
def alphanum_pipe(doc):
	for token in doc:
		if alphanum_re.search(token.text):
			token._.contains_alphanum = True
	return doc
Token.set_extension("contains_alphanum", default=False)

nlp.add_pipe("emoji", first=True)
nlp.add_pipe("rdues_hashtag")
nlp.add_pipe("rdues_alphanum")

sys.stdout.write('Model {}\n'.format(nlp.meta))
sys.stdout.write('Pipeline {}\n'.format([p[0] for p in nlp.pipeline]))
sys.stdout.flush()

fout = open(args.txt + '.tok', 'w', encoding='utf8')
count = 0

with open(args.txt, encoding='utf8') as f:
	text = ""
	for line in f:
		text = line.strip()
		text = clean_text(text)
		
		doc = nlp(text, disable=['parser', 'ner'])
		
		tokens = []
		for token in doc:
			if token._.is_emoji:
				if token._.emoji_desc:
					tokens.append( ':' + token._.emoji_desc.replace(' ', '_') + ':' )
				else:
					tokens.append( ':unknown_emoji:' )
			elif token._.contains_alphanum:
				tokens.append(token.lower_)
		
		if len(tokens) > 0:
			print(' '.join(tokens), file=fout)

		progress()

fout.close()

progress('finished')
