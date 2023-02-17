def plot_core_numbers(distance_threshold=20, vertex_counts=3):
   
    colors = ["blue", "gold", "lawngreen", "red"]
    data = []
    labels = (1,2,3,4)
    
    for n_type in range(4):
        cdf_x = cdf.loc[cdf["type"]==n_type+1]
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

        G = cugraph.Graph()

        G.from_cudf_edgelist(edges_dfx,source='source', destination='target', edge_attr='distance', renumber=True)
        d = cugraph.core_number(G)
        d = d.mean()["core_number"]
        data.append(d)
        
        
    y_pos = np.arange(len(data))

    plt.bar(y_pos, data, align='center', alpha=0.5,color=colors)
    plt.xticks(y_pos, labels)
    plt.ylabel('core_number')
    plt.title('Core Numbers for each Nucleus Type')

    plt.show()

plot_core_numbers(20)
