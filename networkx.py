# Networkx graph creation with pyvis for interactiveness

import spacy
#import re
import pandas as pd
#import bs4
#import requests
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')
import numpy as np


from spacy.matcher import Matcher
matcher = Matcher(nlp.vocab)

from spacy.tokens import Span 

import networkx as nx
from pyvis import network as net

import matplotlib.pyplot as plt
from tqdm import tqdm

pd.set_option('display.max_colwidth', 200)

# read csv file

kg_df = pd.read_csv("/home/becode/Entity_Recognition/assets/input-data-for-graph_1.csv")

# create a directed-graph from a dataframe
def graph(kg_df):
    G=nx.from_pandas_edgelist(kg_df, "source", "target", 
                          edge_attr=True, create_using=nx.MultiDiGraph())
    return G

# assign dataframe to G
G= graph(kg_df)

# Plot the network graph
def plot(G):
    plt.figure(figsize=(12,12))
    pos = nx.spring_layout(G)
    edge_labels = nx.from_pandas_edgelist(G,'relation')
    nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
    nx.draw_networkx_edge_labels(G, pos=pos)
    
    return plt.show()

plot(G)
