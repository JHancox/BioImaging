from timeit import default_timer as timer

def time_loading_at_resolution(level, use_cucim):
    
    start = timer()

    # TODO insert code to load the image at the specified resolution reduction level and with the 
    # full width and height at that resolution
    if use_cucim:
        sizes=wsi.metadata["cucim"]["resolutions"]
        width = sizes["level_dimensions"][level][0]
        height = sizes["level_dimensions"][level][1]
        img = wsi.read_region((0,0),(width, height), level)
    else:
        width, height = slide.level_dimensions[level]
        img = slide.read_region((0,0), level, (width, height))

    end = timer()
    
    return end - start