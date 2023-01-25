# evaluates whether the block contains tissue to analyse
def threshold(arr, threshold_value=80):
    
    if arr.flatten().var() > threshold_value:
        return True
    else:
        return False