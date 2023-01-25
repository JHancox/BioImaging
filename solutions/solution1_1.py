from timeit import default_timer as timer

def time_loading_at_resolution(slide, level): # slide 
    
    start = timer()

    w, h = slide.level_dimensions[level]
    img = slide.read_region((0,0), level,(w, h))

    end = timer()
    
    return end - start