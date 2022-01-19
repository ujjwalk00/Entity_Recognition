import pandas as pd
import re
import spacy
import scispacy

from scispacy.abbreviation import AbbreviationDetector
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("abbreviation_detector")

CONTRACTION_MAP = {
"ain't": "is not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I would",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"i'd": "i would",
"i'd've": "i would have",
"i'll": "i will",
"i'll've": "i will have",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}


text_list = []


def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

def expand_abbreviation(text):
    
    text = "BORDEN &lt;BN> TO ACQUIRE MAJOR PASTA MAKER\
  Borden Inc said it is acquiring &lt;Prince\
  Co Inc> and three companies producing grocery products for 180\
  mln dlrs.\
      Borden said the four companies are expected to have 1987\
  sales totaling 230 mln dlrs.\
      It said Prince, a Lowell, Mass., producer of pasta and\
  Italian food sauces, is expected to account for 210 mln dlrs of\
  this total. This year's sales of Borden pasta -- by the 13\
  regional brands and the premium Creamette brand distributed on\
  a nearly national basis -- are expected to toal 285 mln dlrs,\
  it said.\
      Borden said the other three companies being acquired are\
  Steero Bouillon of Jersey City, N.J., Blue Channel Inc, a\
  Beaufort, S.C., producer of canned crabmeat, and the canned\
  shrimp products line of DeJean Packing Inc of Biloxi, Miss.\
      Borden also said the divestment of three operations with\
  about 50 mln dlrs a year in sales is expected to produce nearly\
  45 mln dlrs in cash for use toward the purchase of new\
  businesses.\
      It said the sale of Polyco of Cincinnati, Ohio, which makes\
  polyvinyl acetate emulsions, to Rohm and Haas Co &lt;ROH> was\
  announced by the buyer last month.\
      Borden said the divestment of two producers of toy models\
  and hobby items -- Heller in France and Humbrol in England --\
  is in process. \
  "

    doc = nlp(text)
    for abrv in doc._.abbreviations:
        text = text.replace(abrv.text,abrv._.long_form.text)
        return text




def normalize_docs(documents):

    normalized_documents = []
    for doc in documents:
        doc = expand_contractions(doc)
        doc = ' '.join(re.sub(' +', ' ',doc.replace('\'s','').replace('\'t','').replace('&lt;','').replace(">","")).split('\n')[1:]).strip().replace('  ',' ')
        doc = expand_contractions(doc)
        doc = expand_abbreviation(doc)
        normalized_documents.append(doc)
    return normalized_documents



def normalize_docs_text(doc):

    #doc = expand_contractions(doc) 
    doc = re.sub(' +\W+', ' ',doc.replace('\'s','').replace('\'t','').replace('&lt;','').replace(">","").replace('  ',' '))
    
    doc = expand_contractions(doc)
    token = nlp(doc)
    for abrv in token._.abbreviations:
        doc = doc.replace(abrv.text,abrv._.long_form.text)
    return doc
    #doc = expand_abbreviation(doc)

    



    









