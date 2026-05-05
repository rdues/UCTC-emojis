# UCTC
A repository containing supporting files for [ADD PAPER REFERENCE ONCE PUBLISHED]

# Folders

## data
This folder contains the raw output of the analysis tools. All of the data is broken down into separate files for each company that was included in the study and split between tweets sent from the company and those sent to the company.

File suffixes show which types are contained in each file:
- .em - emojis in shortcode format
- .wd - words

The folder is broken down into the following sub-folders:
- types - contains word and emoji frequency lists for each company
- collocates - contains collocates of emojis for each company
- tweetids - original tweet ID numbers

## code
This folder contains the Python scripts used for the analysis.
- tokenise_emoji.py - uses spaCy and spacymoji to tokenise txt files into tokens separated by spaces (punctuation removed)
- emoji_stats_tok.py - counts the number of tweets and tokens that are emojis or words
- tok2types.py - converts tokenised text into type frequency lists, separating words and emojis
- tok2colls.py - converts tokenised text into emoji-emoji and emoji-word pairs with frequency
- coll_stats.py - uses the output of the above to filter and sort collocates using z-score
- find_node.py - reformats the output of coll_stats.py to create the figures/tables used in the paper, with options for filtering out stopwords
- find_conc.py - search plain text files for emojis
