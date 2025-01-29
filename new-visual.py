df = actualdf.assign(
    col1=actualdf['colA'].apply(lambda x: x.split('+')[0]),
    col2=actualdf['colA'].apply(lambda x: x.split('+')[1].split('(')[0]),
    col3=actualdf['colA'].apply(lambda x: '(' + x.split('(')[1])
)
