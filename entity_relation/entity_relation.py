from re import A
import pandas as pd
from spacy.matcher import Matcher


def find_rel(doc, nlp):
    subject =[]
    target = []
    relation = []
    entities = set()
    for token in doc:
        if token.dep_== 'ccomp' or token.dep_=='ROOT' or token.pos_ =='VERB':
            sub = find_sub(token)
            if token.nbor().dep_ in ['agent','prep']:
                rel = " ".join([token.text,token.nbor().text])
                obj = find_obj(token.nbor(), doc)
            else:
                rel = token.text
                obj = find_obj(token, doc)
            
            if sub is None:
                continue
            sub= get_full_word(sub, doc)
            if obj is None:
                continue
            subject.append(sub)
            target.append(obj)
            relation.append(rel)
            entities.add(sub)
            entities.add(obj)

    location_rel = find_rel_location(doc, nlp)
    for rel in location_rel:
      subject.append(rel[0])
      relation.append(rel[1])
      target.append(rel[2])
      entities.add(rel[0])
      entities.add(rel[2])
    input_df = pd.DataFrame({'source':subject, 'relation':relation, 'target': target})
    print(input_df)
    input_df.to_csv("Assets/input-data-for-graph_1.csv", index= False)
    entity_df = pd.DataFrame({'id':range(1,len(entities)+1),'entity':[*entities, ]})
    entity_df.to_csv("Assets/entities-for_graph.csv", index = False)
    return input_df
            
def find_sub(pred):
    if len(list(pred.lefts))>0:
        for token in pred.lefts:
            if token.dep_ in ['nsubj', 'nsubjpass']:
                return token
    else:
        if pred.i >1:
          if pred.nbor(-1).dep_ != 'punct':
              return pred.nbor(-1)
          else:
              return pred.nbor(-2)
        
def find_obj(pred, article):
    obj_dep= ['dobj', 'pobj', 'iobj', 'obj', 'obl']
    obj = None
    for token in pred.rights:
        if token.dep_ != 'punct':  
            if token.dep_ in obj_dep:
                obj = token
            elif token.dep_ == 'ccomp':
                    return find_sub(token)
            else:
              for right in token.rights:
                if right.dep_ == 'xcomp':
                  return find_obj(right, article)
                else:
                  if right.pos_ != 'ADP':
                    obj = right
                  else:
                    return find_obj(right, article)
        else:
            break
    for token in pred.lefts:
        if token.dep_ == 'ccomp':
            return find_sub(token)
    if obj != None:
        obj = get_full_word(obj, article)
        
    return obj

def is_passive(token):
    if token.dep_.endswith('pass'): # noun
        return True
    for left in token.lefts: # verb
        if left.dep_ == 'auxpass':
            return True
    return False

def get_full_word(token, article):
    entities = [ent for ent in article.ents]
    for words in entities:
        if token.i in range(words.start,words.end):
            return words.text
        elif token.text == article[words.start].text:
            return words.text
    nouns = [ent for ent in article.noun_chunks]
    for words in nouns:
        if token in words:
            return words.text    
    return token.text

def find_rel_location(article, nlp):
    matcher = Matcher(nlp.vocab)
    rel_list =[]
    pattern = [{'ENT_TYPE':'ORG'}, {'POS': {'IN':['ADP','PUNCT']}},{'POS': 'DET', 'OP': '?'},{'ENT_TYPE':'GPE'}]
    matcher.add("located",[pattern])
    matches = matcher(article)
    for match_id, start, end in matches:
        span = article[start:end]
        
        rel_list.append([get_full_word(span[0], article),'located in',get_full_word(span[-1], article)])
    return rel_list