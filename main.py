import streamlit as st
import spacy
from spacy import displacy
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pyvis import network as net
from IPython.core.display import display, HTML


nlp = spacy.load('en_core_web_lg')

# Create a page dropdown 
#page = st.selectbox("Choose your page", ["Page 1", "Page 2", "Page 3"]) 
    # Display details of page 1elif page == "Page 2":
    # Display details of page 2elif page == "Page 3":
    # Display details of page 3


#if page == "Page 1":
label = "select a file please"
uploaded_file = st.file_uploader(label, type=None, accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None)
if uploaded_file:
    st.write("Filename: ", uploaded_file.name)
    filetype = uploaded_file.name.split(".")[-1]
    st.write("Filetype: ",filetype)
    if filetype == "xlsx":
        df = pd.read_excel("Assets//"+uploaded_file.name)
        st.dataframe(df)
        sentence = st.text_input('Input your sentence here:') 
        article = nlp(sentence)
        html_text = displacy.render(article, style='ent')
        components.html(html_text,
        height=600
        )

        # Add selectbox in streamlit
        option = st.selectbox(
        'What category do you want to test?',
        df.categories.unique())
        st.write('You selected:', option)

        data = df[df.categories==(option)]['text']
        entity_set = []
        for entity in data:
            article = nlp(entity)
            for ne in article.ents:
                if ne.label_ == 'ORG':
                    entity_set.append(ne.text)
        input_df = pd.DataFrame({'source':entity_set, 'relation':['has article related to']* len(entity_set), 'target': option}).drop_duplicates()
        st.dataframe(input_df)



        kg_df = input_df

        def graph(kg_df):
            G=nx.from_pandas_edgelist(kg_df.head(20 +1), "source", "target", 
                                edge_attr=True, create_using=nx.MultiDiGraph())
            return G

        G= graph(kg_df)




        g4 = net.Network(height='400px', width='50%',notebook=True,heading='Graph :)')
        g4.from_nx(G)

        g4.show_buttons(filter_=['physics'])
        g4.show('graph.html')
        display(HTML('graph.html')) 

        components.html("""
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
                nodes = new vis.DataSet([{"id": "NSW", "label": "NSW", "shape": "dot", "size": 10}, {"id": "Ship", "label": "Ship", "shape": "dot", "size": 10}, {"id": "the Arbitration  Commission", "label": "the Arbitration  Commission", "shape": "dot", "size": 10}, {"id": "the NSW Trades", "label": "the NSW Trades", "shape": "dot", "size": 10}, {"id": "Labour Council", "label": "Labour Council", "shape": "dot", "size": 10}, {"id": "Flevoland", "label": "Flevoland", "shape": "dot", "size": 10}, {"id": "Graan Elevator Mij", "label": "Graan Elevator Mij", "shape": "dot", "size": 10}, {"id": "Todd Shipyards Corp", "label": "Todd Shipyards Corp", "shape": "dot", "size": 10}, {"id": "Pacific Coast  Metal Trades District Council", "label": "Pacific Coast  Metal Trades District Council", "shape": "dot", "size": 10}, {"id": "Galveston Division", "label": "Galveston Division", "shape": "dot", "size": 10}, {"id": "the Galveston Metal Trades Council", "label": "the Galveston Metal Trades Council", "shape": "dot", "size": 10}, {"id": "Seattle Division", "label": "Seattle Division", "shape": "dot", "size": 10}, {"id": "The Pacific Coast Council", "label": "The Pacific Coast Council", "shape": "dot", "size": 10}, {"id": "The Labour Council", "label": "The Labour Council", "shape": "dot", "size": 10}, {"id": "the Australian Council of  Trade Unions", "label": "the Australian Council of  Trade Unions", "shape": "dot", "size": 10}, {"id": "ACTU", "label": "ACTU", "shape": "dot", "size": 10}, {"id": "Velayati", "label": "Velayati", "shape": "dot", "size": 10}, {"id": "Kuwaiti", "label": "Kuwaiti", "shape": "dot", "size": 10}, {"id": "Foreign Ministry", "label": "Foreign Ministry", "shape": "dot", "size": 10}, {"id": "the Foreign Ministry", "label": "the Foreign Ministry", "shape": "dot", "size": 10}, {"id": "The Iranian News Agency", "label": "The Iranian News Agency", "shape": "dot", "size": 10}, {"id": "IRNA", "label": "IRNA", "shape": "dot", "size": 10}]);
                edges = new vis.DataSet([{"from": "NSW", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "the Arbitration  Commission", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "the NSW Trades", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "Labour Council", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "Flevoland", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "Graan Elevator Mij", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "Todd Shipyards Corp", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "Pacific Coast  Metal Trades District Council", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "Galveston Division", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "the Galveston Metal Trades Council", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "Seattle Division", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "The Pacific Coast Council", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "The Labour Council", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "the Australian Council of  Trade Unions", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "ACTU", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "Velayati", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "Kuwaiti", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "Foreign Ministry", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "the Foreign Ministry", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "The Iranian News Agency", "relation": "has article related to", "to": "Ship", "weight": 1}, {"from": "IRNA", "relation": "has article related to", "to": "Ship", "weight": 1}]);

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
            """,
            height=1200,width=700)

