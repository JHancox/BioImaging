from cuml.neighbors import NearestNeighbors as cuNN
import cuxfilter.charts as cfc
import cuxfilter.layouts as clo
import pickle

# This loads the tiles created in the previous lab
with open("data/tiles_xy", "rb") as fp: 
    tiles_xy = pickle.load(fp)
    
tiles_xy_cdf=cudf.DataFrame(tiles_xy)

knn_cuml = cuNN()
knn_cuml.fit(tiles_xy_cdf)
# Note the two_pass_precision=True flag which forces
%time D_cuml, I_cuml = knn_cuml.kneighbors(tiles_xy_cdf, 3,two_pass_precision=True)

#give the columns names because they have to be unique in the merged dataframe
I_cuml.columns=['ix1','n1','n2']
D_cuml.columns=['ix2','d1','d2']
all_cols = cudf.concat([I_cuml, D_cuml],axis=1)

# remove the index and distance from the self-referenced nearest neighbour
all_cols = all_cols[['n1','n2','d1','d2']]

# Reformat the data to match the way edges are defined in cuGraph
all_cols['index1'] = all_cols.index

c1 = all_cols[['index1','n1','d1']]
c1.columns=['source','target','weight']
c2 = all_cols[['index1','n2','d2']]
c2.columns=['source','target','weight']
   
edges = [c1,c2]
edge_df = cudf.concat(edges)

del(all_cols)

edge_df = edge_df.reset_index()
edge_df = edge_df[['source','target','weight']]

G = cugraph.Graph()
G.from_cudf_edgelist(edge_df,source='source', destination='target', edge_attr='weight', renumber=True)

nodes_ = tiles_xy_cdf
nodes_['vertex']=nodes_.index
nodes_.columns=['x','y','vertex']

cux_df = fdf.load_graph((nodes_, edge_df))

chart0 = cfc.graph(edge_color_palette=['gray', 'black'],
                                            timeout=200, 
                                            node_aggregate_fn='mean', node_pixel_shade_type='linear',
                                            edge_render_type='direct',#other option available -> 'curved'
                                            edge_transparency=0.5
                                          )
d = cux_df.dashboard([chart0], layout=clo.double_feature)

# draw the graph
chart0.view()
