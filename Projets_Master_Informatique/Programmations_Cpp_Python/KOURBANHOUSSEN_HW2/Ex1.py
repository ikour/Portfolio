
def is_pal(str):
    for st in str.split():
        if (st == st[::-1]) == False:
            return False 
    return True
