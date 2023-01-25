print(feat_cols[0:10])

print(pca_df.memory_usage(index=True))

# Set the number of components
pca = PCA(n_components=4)

# Set the column range and row range
pca_result2 = pca.fit_transform(df[feat_cols[0:16][:1000]])

# Add the new pca column name
pca_df = pd.DataFrame(pca_result2,columns=["pca-1", "pca-2", "pca-3", "pca-4"])

print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))
print(pca_df)