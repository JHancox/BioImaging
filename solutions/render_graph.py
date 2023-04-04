def render_graph(nucleus_type=4, distance_threshold=20):

    colors = ["blue", "gold", "lawngreen", "red"]
    
    if nucleus_type > len(colors) or nucleus_type <1 :
        print("Nucleus Type needs to be >0 and <=4")
        return
        
    
    color = colors[nucleus_type-1]

    cdf_x = cdf.loc[cdf["type"]==nucleus_type]
    cdf_x = cdf_x.reset_index()
    cdf_x["index"] = cdf_x.index

    knn_cuml = NearestNeighbors()
    knn_cuml.fit(cdf_x)

    D_cuml, I_cuml = knn_cuml.kneighbors(cdf_x, 5)

    I_cuml.columns=['ix1','n1','n2','n3','n4'] 
    D_cuml.columns=['ix2','d1','d2','d3','d4'] 
    all_cols = cudf.concat([I_cuml, D_cuml],axis=1)

    # remove the index and distance from the self-referenced nearest neighbour
    all_cols = all_cols[['n1','n2','n3','n4','d1','d2','d3','d4']]
    # Reformat the data to match the way edges are defined in cuGraph
    all_cols['index1'] = all_cols.index

    c1 = all_cols[['index1','n1','d1']]
    c1.columns=['source','target','distance']
    c2 = all_cols[['index1','n2','d2']]
    c2.columns=['source','target','distance']
    c3 = all_cols[['index1','n3','d3']]
    c3.columns=['source','target','distance']
    c4 = all_cols[['index1','n4','d4']]
    c4.columns=['source','target','distance']

    edges_dfx = [c1,c2,c3,c4]
    edges_dfx = cudf.concat(edges_dfx)

    # remove the old dataframe from memory
    del(all_cols)

    edges_dfx = edges_dfx[['source','target','distance']]
    edges_dfx = edges_dfx.loc[edges_dfx["distance"] < distance_threshold*distance_threshold ]

    nodes_x = cdf_x[['row','col']]

    # Vertex refers to the index of an item in the 
    nodes_x['vertex']=nodes_x.index
    nodes_x.columns=['x','y','vertex']

    cux_dfx = cuxfilter.DataFrame.load_graph((nodes_x, edges_dfx))
    chartx = cuxfilter.charts.graph(edge_color_palette=['gray', 'black'],
                                                timeout=200, 
                                                node_aggregate_fn='mean', 
                                                node_color_palette=[color],
                                                edge_render_type='direct',
                                                edge_transparency=0.5
                                              )


    cux_dfx.dashboard([chartx], layout=cuxfilter.layouts.double_feature)

    return chartx
    
chartx = render_graph()
chartx.view()