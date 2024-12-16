import os
import sys

if not __package__:
    # Make CLI runnable from source tree
    package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)

from NCBI_grab_package import NCBI_ID_grab

bacteria = ['Eubacterium_sp.', 'Ruminococcaceae_', 'Blautia_', 'Lactiplantibacillus_plantarum']
NCBI_ID_grab.find_NCBI_ID_from_Bacterial_list(bacteria)