import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import pandas as pd
import spacy

nlp = spacy.load('en_core_web_lg')


label = "select a file please"
df = pd.read_excel("Assets/preprocessed_text.xlsx")
option = st.selectbox(
    'What category do you want to test?',
    df.categories.unique())
option_clean = option.replace("['", "").replace("']", "")

st.write('You selected:', option_clean)


data = df[df.categories == (option)]['text']
entity_set = []
for entity in data:
    article = nlp(entity)
    for ne in article.ents:
        if ne.label_ == 'ORG':
            entity_set.append(ne.text)
input_df = pd.DataFrame({'source': entity_set, 'relation': [
                        'has article related to'] * len(entity_set), 'target': option_clean}).drop_duplicates()
st.dataframe(input_df)


nodes_list = []
edges_list = []
nodes_list.append(
    {"id": option_clean, "label": option_clean, "shape": "dot", "size": 10})
for i in range(21):
    nodes_list.append(
        {"id": input_df.iloc[i, 0], "label": input_df.iloc[i, 0], "shape": "dot", "size": 10})
    edges_list.append(
        {"from": input_df.iloc[i, 0], "relation": input_df.iloc[i, 1], "to": option_clean, "weight": 1})


st.write(len(nodes_list))
st.write(len(edges_list))

st.write(str(nodes_list))
st.write(str(edges_list))


nodes = []
edges = []

nodes.append(
    Node(id=option_clean,
            label=option_clean,
            size=800
            )
)

for i in range(8):
    nodes.append(
        Node(id=input_df.iloc[i, 0],
             label=input_df.iloc[i, 0],
             size=800
             )

    )

    edges.append(Edge(source=input_df.iloc[i, 0],
                  label=input_df.iloc[i, 1],
                  target=input_df.iloc[i, 2],
                  type="CURVE_SMOOTH",
                  strokeWidth=1.5

                  )
             )  


config = Config(width=800,
                height=800,
                directed=True,
                node={'labelProperty': 'label'},
                link={'labelProperty': 'label', 'renderLabel': True}
                # **kwargs e.g. node_size=1000 or node_color="blue"
                )


return_value = agraph(nodes=nodes,
                      edges=edges,
                      config=config)





# nodes.append(Node(id="Spiderman",
#                   label="Peter Parker",
#                   size=800,
#                   svg="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png")
#              )  # includes **kwargs
# nodes.append(Node(id="Captain_Marvel",
#                   size=400,
#                   svg="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png")
#              )
# edges.append(Edge(source="Captain_Marvel",
#                   label="friend_of",
#                   target="Spiderman",
#                   type="CURVE_SMOOTH",
#                   strokeWidth=4

#                   )
#              )  # includes **kwargs

# config = Config(width=500,
#                 height=500,
#                 directed=True,
#                 nodeHighlightBehavior=True,
#                 highlightColor="#F7A7A6",  # or "blue"
#                 collapsible=True,
#                 node={'labelProperty': 'label'},
#                 link={'labelProperty': 'label', 'renderLabel': True}
#                 # **kwargs e.g. node_size=1000 or node_color="blue"
#                 )

# return_value = agraph(nodes=nodes,
#                       edges=edges,
#                       config=config)
