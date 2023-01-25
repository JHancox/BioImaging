# Invert the weight values so that larger distances create weaker weights
edge_df['weight'] = 1/edge_df['weight']
edge_df