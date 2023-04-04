from timeit import default_timer as timer

def time_loading_at_resolution(level, use_cucim):
    
    start = timer()

    if use_cucim:
        sizes=wsi.metadata["cucim"]["resolutions"]

        # Get the dimensions at the lowest resolution level
        wt = sizes["level_dimensions"][level][0]
        ht = sizes["level_dimensions"][level][1]

        # TODO insert code to load the image at the specified resolution reduction level  
        # and with the full width and height at that resolution
        wsi_thumb = wsi.read_region(location=(0,0), size=(wt,ht), level=level)
    else:
        width, height = slide.level_dimensions[level]
        img = slide.read_region((0,0), level, (width, height))

    end = timer()
    
    return end - start