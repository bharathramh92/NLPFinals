from portal.reduction import *


def summarize(text):
    reduction = Reduction()
    reduction_ratio = .6
    reduced_text = reduction.reduce(text, reduction_ratio)
    return reduced_text

if __name__=='__main__':
    text = "We purchased these fairly easy to install as long as you have a drill.  Keeping baby out so far.  Used when tot locks were to hard to locate with magnet-better than them by far."
    summarize(text)
