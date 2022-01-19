import spacy
from spacy import displacy
from spacy.matcher import Matcher

from entity_relation.entity_relation import *
from text_preprocessing.Text_Preprocessing import *


import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config
from entity_relation import *


nlp = spacy.load("en_core_web_sm")


# article = nlp('Borden Inc said it is acquiring Prince Co Inc and three companies producing grocery products for 180 mln dlrs. Borden said the four companies are expected to have 1987 sales totaling 230 mln dlrs. It said Prince, a Lowell, Mass., producer of pasta and Italian food sauces, is expected to account for 210 mln dlrs of this total. This years sales of Borden pasta -- by the 13 regional brands and the premium Creamette brand distributed on a nearly national basis -- are expected to toal 285 mln dlrs, it said. Borden said the other three companies being acquired are Steero Bouillon of Jersey City, N.J., Blue Channel Inc, a Beaufort, S.C., producer of canned crabmeat, and the canned shrimp products line of DeJean Packing Inc of Biloxi, Miss. Borden also said the divestment of three operations with about 50 mln dlrs a year in sales is expected to produce nearly 45 mln dlrs in cash for use toward the purchase of new businesses. It said the sale of Polyco of Cincinnati, Ohio, which makes polyvinyl acetate emulsions, to Rohm and Haas Co ROH was announced by the buyer last month.  Borden said the divestment of two producers of toy models and hobby items -- Heller in France and Humbrol in England -- is in process.')


# Create a page dropdown
page = st.selectbox("Choose your page", ["Page 1", "Page 2", "Page 3"])
# Display details of page 1elif page == "Page 2":
# Display details of page 2elif page == "Page 3":
# Display details of page 3


if page == "Page 1":

    sentence = st.text_input("Input your sentence here:")
    if sentence:
        # st.write(sentence)
        sentence = normalize_docs_text(sentence)
        # st.write(sentence)

        # st.write(type(sentence))
        article = nlp(sentence)
        # html_text = displacy.render(article, style='ent')
        # components.html(html_text,
        # height=600
        # )

        input_df = find_rel(article, nlp)
        st.dataframe(input_df)

        nodes = []
        edges = []

        len_df = len(input_df)

        for i in range(len_df):

            nodes.append(
                Node(id=input_df.iloc[i, 0], label=input_df.iloc[i, 0], size=800)
            )

            nodes.append(
                Node(id=input_df.iloc[i, 2], label=input_df.iloc[i, 2], size=800)
            )

            edges.append(
                Edge(
                    source=input_df.iloc[i, 0],
                    label=input_df.iloc[i, 1],
                    target=input_df.iloc[i, 2],
                    type="CURVE_SMOOTH",
                    strokeWidth=1.5,
                )
            )

        config = Config(
            width=800,
            height=800,
            directed=True,
            node={"labelProperty": "label"},
            link={"labelProperty": "label", "renderLabel": True}
            # **kwargs e.g. node_size=1000 or node_color="blue"
        )

        return_value = agraph(nodes=nodes, edges=edges, config=config)

        # nodes_list = []
        # edges_list = []
        # len_df = len(input_df)

        # nodes_list.append({"id": "lol", "label": "lol", "shape": "dot", "size": 10})

        # for i in range(len_df):
        #     nodes_list.append({"id": input_df.iloc[i,0], "label": input_df.iloc[i,0], "shape": "dot", "size": 10})
        #     edges_list.append({"from": input_df.iloc[i,0], "relation":input_df.iloc[i,1], "to": input_df.iloc[i,2], "weight": 1})

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

    df = pd.read_excel("assets//" + "preprocessed_text.xlsx")

    option = st.selectbox("What category do you want to test?", df.categories.unique())
    option_clean = option.replace("['", "").replace("']", "")

    st.write("You selected:", option_clean)

    data = df[df.categories == (option)]["text"]
    entity_set = []
    for entity in data:
        article = nlp(entity)
        for ne in article.ents:
            if ne.label_ == "ORG":
                entity_set.append(ne.text)
    input_df = pd.DataFrame(
        {
            "source": entity_set,
            "relation": ["has article related to"] * len(entity_set),
            "target": option_clean,
        }
    ).drop_duplicates()

    nodes_list = []
    edges_list = []
    nodes_list.append(
        {"id": option_clean, "label": option_clean, "shape": "dot", "size": 10}
    )
    len_df = len(input_df)
    if len_df >= 21:
        for i in range(21):
            nodes_list.append(
                {
                    "id": input_df.iloc[i, 0],
                    "label": input_df.iloc[i, 0],
                    "shape": "dot",
                    "size": 10,
                }
            )
            edges_list.append(
                {
                    "from": input_df.iloc[i, 0],
                    "relation": input_df.iloc[i, 1],
                    "to": option_clean,
                    "weight": 1,
                }
            )
    else:
        for i in range(len_df):
            nodes_list.append(
                {
                    "id": input_df.iloc[i, 0],
                    "label": input_df.iloc[i, 0],
                    "shape": "dot",
                    "size": 10,
                }
            )
            edges_list.append(
                {
                    "from": input_df.iloc[i, 0],
                    "relation": input_df.iloc[i, 1],
                    "to": option_clean,
                    "weight": 1,
                }
            )

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
    #         nodes = new vis.DataSet(""" + str(nodes_list)+""");
    #         edges = new vis.DataSet(""" + str(edges_list)+""");

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
    #                 height=1200, width=700)
