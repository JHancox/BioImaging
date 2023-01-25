%%time

# iterate over a set of regions from which to threshold
def process_tile(start_loc_list):
    # Load the image and threshold at each location
    slide = CuImage(input_file)
    res = []
    for start_loc in start_loc_list:
        region = np.array(slide.read_region(start_loc, [tile_size, tile_size], 0))
        if threshold(region):
            res.append((start_loc[0], start_loc[1], region))
        
    return res


# map each patch to a process
chunk_size = len(patches) // num_chunks   

# generate a list of coordinates at which to threshold
start_loc_data = [(sx+res[0], sy+res[1])
                  for res in patches
                      for sy in range(0, patch_size, tile_size)
                          for sx in range(0, patch_size, tile_size)]

start_loc_list2 = [start_loc_data[i:i+chunk_size]  for i in range(0, len(start_loc_data), chunk_size)]
future_result2 = list(client.map(process_tile, start_loc_list2))

tiles = compile_results(future_result2)

print("Number of 64 x 64 tiles found = {}".format(len(tiles)))