import sys

def ProgressBar(i,total,pretext="",posttext=""):
    twentieth = (total-1)/20
    if twentieth!=0.0:
        fullBlock='\u2588'
        fullBlocks=int((i - i%twentieth)/twentieth)

        remainder=(i%twentieth/twentieth)
        if remainder<(1/8):
            capBlock=''
        elif remainder<(2/8):
            capBlock='\u258F'
        elif remainder<(3/8):
            capBlock='\u258E'
        elif remainder<(4/8):
            capBlock='\u258D'
        elif remainder<(5/8):
            capBlock='\u258C'
        elif remainder<(6/8):
            capBlock='\u258B'
        elif remainder<(7/8):
            capBlock='\u258A'
        elif remainder<(8/8):
            capBlock='\u2589'

        sys.stdout.write('\r')
        sys.stdout.write(pretext+"[{0:20s}] {1:0.1%}".format(fullBlock*fullBlocks+capBlock, i/(total-1))+posttext)
        sys.stdout.flush()