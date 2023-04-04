from timeit import default_timer as timer

def time_loading_at_resolution(slide, level): # slide 
    
    start = timer()
    
    # TODO - insert code to print out the dimensions and load the image at the specified level
    w, h = slide.level_dimensions[level]
    print(w,h)
    img = slide.read_region((0,0), level,(w, h))

    end = timer()
    
    return end - start