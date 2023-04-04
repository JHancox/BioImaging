# The offset of the current patch - use it to position the
# centroids relative to the Region of Interest offset
current_tile_offset = ()

# Region of Interest Offset
roi_y = 47000
roi_x = 25000

# create a function that will be added
# to the post-processing Transforms
def get_centroids(inst_info):
    
    centroids=[]
    for i in range(len(inst_info)):
        if i+1 in inst_info.keys():
            x = int(inst_info[i+1]["centroid"][0] + current_tile_offset[0])
            y = int(inst_info[i+1]["centroid"][1] + current_tile_offset[1])
            centroids.append({"x": x, "y": y, "type": inst_info[i+1]["type"]})

        
    return centroids
        
# Postprocessing transforms
post_transform_with_centroids = Compose(
    [
        HoVerNetInstanceMapPostProcessingd(sobel_kernel_size=21, marker_threshold=0.4, marker_radius=2),
        HoVerNetNuclearTypePostProcessingd(),
        Lambdad(keys="instance_info", func=get_centroids),
    ]
)

dataloader = DataLoader(dataset=dataset, batch_size=4, num_workers=8)
model.eval()
out=[]

with torch.no_grad():
    
    centroids = []
    for d in dataloader:
        # one offset for each image in the batch
        offsets = (d["image"].meta["location"][0]-roi_x, d["image"].meta["location"][1]-roi_y)
        pred = inferer(inputs=d["image"].to(device), network=model)
        nu = np.array(pred["nucleus_prediction"].cpu())
        hv = np.array(pred["horizontal_vertical"].cpu())
        tp = np.array(pred["type_prediction"].cpu())
        
        for i in range(len(nu)):
            current_tile_offset = (offsets[0][i], offsets[1][i])
            inputs =  {"nucleus_prediction": nu[i], "horizontal_vertical": hv[i], "type_prediction": tp[i]}
            out = post_transform_with_centroids(inputs)
            for item in out["instance_info"]:
                centroids.append(item)

print("Completed")