# Profiling.
#from pycallgraph import PyCallGraph
#from pycallgraph.output import GraphvizOutput
import logging
logging.basicConfig(filename=None, format='%(asctime)-6s: %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


cg_path = './tests/callgraphs/'
profile = False     # If True, will generate callgraphs.

class Profile(object):
    def __init__(self, pcgpath):
        if profile:
            self.p = PyCallGraph(output=GraphvizOutput(output_file=pcgpath))
    
    def __enter__(self):
        if profile:
            self.p.start()

    def __exit__(self, *args):
        if profile:
            self.p.done()
            del self.p

# Paths.
datapath = './tests/data'
picklepath = './tests/data/pickles'

temppath = './tests/sandbox/temp'
outpath = './tests/sandbox/out'
mallet_path = '/Applications/mallet-2.0.7'
dtm_path = './tethne/model/bin/dtm'

# TODO: remove this later.
import sys
sys.path.append('/Users/bpeirson/Repositories/tethne')
#sys.path.append('/Users/erickpeirson/tethne')
