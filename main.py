import spacy
from spacy import displacy
from scispacy.abbreviation import AbbreviationDetector
from spacy.matcher import Matcher

from entity_relation.entity_relation import *

nlp = spacy.load('en_core_web_lg')

article = nlp('Borden Inc said it is acquiring Prince Co Inc and three companies producing grocery products for 180 mln dlrs. Borden said the four companies are expected to have 1987 sales totaling 230 mln dlrs. It said Prince, a Lowell, Mass., producer of pasta and Italian food sauces, is expected to account for 210 mln dlrs of this total. This years sales of Borden pasta -- by the 13 regional brands and the premium Creamette brand distributed on a nearly national basis -- are expected to toal 285 mln dlrs, it said. Borden said the other three companies being acquired are Steero Bouillon of Jersey City, N.J., Blue Channel Inc, a Beaufort, S.C., producer of canned crabmeat, and the canned shrimp products line of DeJean Packing Inc of Biloxi, Miss. Borden also said the divestment of three operations with about 50 mln dlrs a year in sales is expected to produce nearly 45 mln dlrs in cash for use toward the purchase of new businesses. It said the sale of Polyco of Cincinnati, Ohio, which makes polyvinyl acetate emulsions, to Rohm and Haas Co ROH was announced by the buyer last month.  Borden said the divestment of two producers of toy models and hobby items -- Heller in France and Humbrol in England -- is in process.')

df = find_rel(article)