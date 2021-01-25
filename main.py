import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import json

st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>',
         unsafe_allow_html=True)

st.title('DataViz APP')
st.markdown('Choose your plot and get the code.')

plot_type = st.selectbox(
    "Plot type:",
    ("Line", "Bar", "Histogram")
)

if(plot_type == 'Line'):

    st.markdown('### Templates:')
    with open('jsons/line_plots.json', 'rb') as f:
        line_plots = json.load(f)

    images = [Image.open(_['image']) for _ in line_plots]

    st.image([im.resize((
                min(int(im.size[0]*.1), 150), 
                min(int(im.size[1]*.1), 60)
              ))
              for im in images],
             [f'Plot {i}' for i in range(len(line_plots))])

    pick_img = st.radio("Choose plot:",
                        [str(i) for i in range(len(line_plots))])

    st.markdown('## Line plot')

    st.markdown('Font: [%s](%s)' % (line_plots[int(pick_img)]['font'],
                                    line_plots[int(pick_img)]['link']))

    im = images[int(pick_img)]
    st.image(im.resize((
        min(int(im.size[0]*.5), 800),
        min(int(im.size[1]*.5), 600)
    )))
    
    st.markdown('Code')
    with open(line_plots[int(pick_img)]['code'], 'r') as f:
        code = f.read()
    print(code)
    st.code(code)