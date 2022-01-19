from re import A
import pandas as pd

def find_rel(doc):
    subject =[]
    target = []
    relation = []
    for token in doc:
        if token.dep_== 'ccomp' or token.dep_=='ROOT' or token.pos_ =='VERB':
            sub = find_sub(token)
            if token.nbor().dep_ == 'agent':
                rel = " ".join([token.text,token.nbor().text])
            else:
                rel = token.text
            if sub is None:
                continue
            sub= get_full_word(sub, doc)
            obj = find_obj(token, doc)
            if obj is None:
                continue
            subject.append(sub)
            target.append(obj)
            relation.append(rel)
    input_df = pd.DataFrame({'source':subject, 'relation':relation, 'target': target})
    print(input_df)
    #input_df.to_csv("Assets/input-data-for-graph_1.csv", index= False)
    return input_df
            
def find_sub(pred):
    if len(list(pred.lefts))>0:
        for token in pred.lefts:
            if token.dep_ in ['nsubj', 'nsubjpass']:
                return token
    else:
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
            else:
                if token.dep_ == 'ccomp':
                    obj = find_sub(token)
                for right in token.rights:
                    obj = right
        else:
            break
    for token in pred.lefts:
        if token.dep_ == 'ccomp':
            obj = find_sub(token)
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
    noun_words = [ent for ent in article.ents]
    for words in noun_words:
        if token.i in range(words.start,words.end):
            return words.text
        
    return token.text
