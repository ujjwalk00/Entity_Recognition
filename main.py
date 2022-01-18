import streamlit as st
import spacy
from spacy import displacy
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from streamlit_agraph import agraph, Node, Edge, Config



def find_rel(doc):
    df = pd.DataFrame()
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
            sub= get_full_word(sub)
            obj = find_obj(token)
            if obj is None:
                continue
#             obj = get_full_word(obj)
            subject.append(sub)
            target.append(obj)
            relation.append(rel)
    input_df = pd.DataFrame({'source':subject, 'relation':relation, 'target': target})
    print(input_df)
    return input_df

    # input_df.to_csv("../Assets/input-data-for-graph_1.csv", index= False)
            
def find_sub(pred):
    if len(list(pred.lefts))>0:
        for token in pred.lefts:
            if token.dep_ in ['nsubj', 'nsubjpass']:
                return token
#     if pred.head != pred and not is_passive(pred): 
#         print("Head of ",pred,' is ',pred.head)
    
#         return find_sub(pred.head)
#     else:
#         return None 
    else:
        if pred.nbor(-1).dep_ != 'punct':
            return pred.nbor(-1)
        else:
            return pred.nbor(-2)
        
def find_obj(doc):
    obj_dep= ['dobj', 'pobj', 'iobj', 'obj', 'obl']
    obj = None
    for token in doc.rights:
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
    for token in doc.lefts:
        if token.dep_ == 'ccomp':
            obj = find_sub(token)
#     print(obj)
    if obj != None:
        if obj.nbor().pos_=="CCONJ":
            obj = get_conj_words(obj)
        else:
            obj = get_full_word(obj)
    return obj
            
def is_passive(token):
    if token.dep_.endswith('pass'): # noun
        return True
    for left in token.lefts: # verb
        if left.dep_ == 'auxpass':
            return True
    return False

def get_full_word(token):
    noun_words = [ent for ent in article.noun_chunks]
    for words in noun_words:
        print(words)
        if token in words:
#             print(words.)
            return get_conj_words(words)
        
    return token

def get_conj_words(token):
    for words in conj_list:
#         print(token)
        if words.find(token.text) != -1:
            print(words)
#         if tok.pos_ != "CCONJ":
#             obj = obj+" "+get_full_word(tok).text
#         else:
#             obj = obj.text+" "+tok.text
            return words
    return token.text
#     print(*token.rights)





nlp = spacy.load('en_core_web_lg')

# Create a page dropdown 
page = st.selectbox("Choose your page", ["Page 1", "Page 2", "Page 3"]) 
    # Display details of page 1elif page == "Page 2":
    # Display details of page 2elif page == "Page 3":
    # Display details of page 3


if page == "Page 1":
    df = pd.read_excel("Assets//"+"preprocessed_text.xlsx")
    st.dataframe(df)
    sentence = st.text_input('Input your sentence here:') 
    article = nlp(sentence)
    html_text = displacy.render(article, style='ent')
    components.html(html_text,
    height=600
    )
    # input_df = find_rel(article)


    # nodes_list = []
    # edges_list = []
    # nodes_list.append({"id": option_clean, "label": option_clean, "shape": "dot", "size": 10})
    # len_df = len(input_df)
    # if len_df>=21:
    #     for i in range(21):
    #         nodes_list.append({"id": input_df.iloc[i,0], "label": input_df.iloc[i,0], "shape": "dot", "size": 10})
    #         edges_list.append({"from": input_df.iloc[i,0], "relation":input_df.iloc[i,1], "to": option_clean, "weight": 1})
    # else:
    #     for i in range(len_df):
    #         nodes_list.append({"id": input_df.iloc[i,0], "label": input_df.iloc[i,0], "shape": "dot", "size": 10})
    #         edges_list.append({"from": input_df.iloc[i,0], "relation":input_df.iloc[i,1], "to": option_clean, "weight": 1})
    
    


    # html_str = """
    # <html>
    # <head>
    # <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.css" type="text/css" />
    # <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis-network.min.js"> </script>
    # <center>
    # </center>

    # <!-- <link rel="stylesheet" href="../node_modules/vis/dist/vis.min.css" type="text/css" />
    # <script type="text/javascript" src="../node_modules/vis/dist/vis.js"> </script>-->

    # <style type="text/css">

    #         #mynetwork {
    #             width: 100%;
    #             height: 700px;
    #             background-color: #ffffff;
    #             border: 1px solid lightgray;
    #             position: relative;
    #             float: left;
    #         }

    #         #config {
    #             float: left;
    #             width: 1000px;
    #             height: 600px;
    #         }
            
    # </style>

    # </head>

    # <body>
    # <div id = "mynetwork"></div>


    # <div id = "config"></div>

    # <script type="text/javascript">

    #     // initialize global variables.
    #     var edges;
    #     var nodes;
    #     var network; 
    #     var container;
    #     var options, data;

        
    #     // This method is responsible for drawing the graph, returns the drawn network
    #     function drawGraph() {
    #         var container = document.getElementById('mynetwork');
            
            

    #         // parsing and collecting nodes and edges from the python
    #         nodes = new vis.DataSet(""" +str(nodes_list)+""");
    #         edges = new vis.DataSet(""" +str(edges_list)+""");

    #         // adding nodes and edges to the graph
    #         data = {nodes: nodes, edges: edges};

    #         var options = {
    #     "configure": {
    #         "enabled": true,
    #         "filter": [
    #             "physics"
    #         ]
    #     },
    #     "edges": {
    #         "color": {
    #             "inherit": true
    #         },
    #         "smooth": {
    #             "enabled": false,
    #             "type": "continuous"
    #         }
    #     },
    #     "interaction": {
    #         "dragNodes": true,
    #         "hideEdgesOnDrag": false,
    #         "hideNodesOnDrag": false
    #     },
    #     "physics": {
    #         "enabled": true,
    #         "stabilization": {
    #             "enabled": true,
    #             "fit": true,
    #             "iterations": 1000,
    #             "onlyDynamicEdges": false,
    #             "updateInterval": 50
    #         }
    #     }
    # };
            
    #         // if this network requires displaying the configure window,
    #         // put it in its div
    #         options.configure["container"] = document.getElementById("config");
            

    #         network = new vis.Network(container, data, options);
        
    #         return network;

    #     }

    #     drawGraph();

    # </script>
    # </body>
    # </html>
    #     """

    # components.html(html_str,
    #     height=1200,width=700)






            

if page == "Page 2":

    df = pd.read_excel("Assets//"+"preprocessed_text.xlsx")

    option = st.selectbox(
            'What category do you want to test?',
            df.categories.unique())
    option_clean = option.replace("['", "").replace("']", "")
    
    st.write('You selected:', option_clean)

    data = df[df.categories==(option)]['text']
    entity_set = []
    for entity in data:
        article = nlp(entity)
        for ne in article.ents:
            if ne.label_ == 'ORG':
                entity_set.append(ne.text)
    input_df = pd.DataFrame({'source':entity_set, 'relation':['has article related to']* len(entity_set), 'target': option_clean}).drop_duplicates()




    def graph(input_df):
        G=nx.from_pandas_edgelist(input_df.head(20+1), "source", "target", 
                            edge_attr=True, create_using=nx.MultiDiGraph())
        return G

    G= graph(input_df)


    nodes_list = []
    edges_list = []
    nodes_list.append({"id": option_clean, "label": option_clean, "shape": "dot", "size": 10})
    len_df = len(input_df)
    if len_df>=21:
        for i in range(21):
            nodes_list.append({"id": input_df.iloc[i,0], "label": input_df.iloc[i,0], "shape": "dot", "size": 10})
            edges_list.append({"from": input_df.iloc[i,0], "relation":input_df.iloc[i,1], "to": option_clean, "weight": 1})
    else:
        for i in range(len_df):
            nodes_list.append({"id": input_df.iloc[i,0], "label": input_df.iloc[i,0], "shape": "dot", "size": 10})
            edges_list.append({"from": input_df.iloc[i,0], "relation":input_df.iloc[i,1], "to": option_clean, "weight": 1})
    
    


    html_str = """
    <html>
    <head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.css" type="text/css" />
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis-network.min.js"> </script>
    <center>
    </center>

    <!-- <link rel="stylesheet" href="../node_modules/vis/dist/vis.min.css" type="text/css" />
    <script type="text/javascript" src="../node_modules/vis/dist/vis.js"> </script>-->

    <style type="text/css">

            #mynetwork {
                width: 100%;
                height: 700px;
                background-color: #ffffff;
                border: 1px solid lightgray;
                position: relative;
                float: left;
            }

            #config {
                float: left;
                width: 1000px;
                height: 600px;
            }
            
    </style>

    </head>

    <body>
    <div id = "mynetwork"></div>


    <div id = "config"></div>

    <script type="text/javascript">

        // initialize global variables.
        var edges;
        var nodes;
        var network; 
        var container;
        var options, data;

        
        // This method is responsible for drawing the graph, returns the drawn network
        function drawGraph() {
            var container = document.getElementById('mynetwork');
            
            

            // parsing and collecting nodes and edges from the python
            nodes = new vis.DataSet(""" +str(nodes_list)+""");
            edges = new vis.DataSet(""" +str(edges_list)+""");

            // adding nodes and edges to the graph
            data = {nodes: nodes, edges: edges};

            var options = {
        "configure": {
            "enabled": true,
            "filter": [
                "physics"
            ]
        },
        "edges": {
            "color": {
                "inherit": true
            },
            "smooth": {
                "enabled": false,
                "type": "continuous"
            }
        },
        "interaction": {
            "dragNodes": true,
            "hideEdgesOnDrag": false,
            "hideNodesOnDrag": false
        },
        "physics": {
            "enabled": true,
            "stabilization": {
                "enabled": true,
                "fit": true,
                "iterations": 1000,
                "onlyDynamicEdges": false,
                "updateInterval": 50
            }
        }
    };
            
            // if this network requires displaying the configure window,
            // put it in its div
            options.configure["container"] = document.getElementById("config");
            

            network = new vis.Network(container, data, options);
        
            return network;

        }

        drawGraph();

    </script>
    </body>
    </html>
        """

    components.html(html_str,
        height=1200,width=700)



