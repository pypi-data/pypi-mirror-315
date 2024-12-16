# import sys
# import os

# # Add src to the system path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# # Now import the package


from NCBI_grab_package import NCBI_ID_grab

bacteria = ['Eubacterium_sp.', 'Ruminococcaceae_', 'Blautia_', 'Lactiplantibacillus_plantarum']
dict_1 = NCBI_ID_grab.find_NCBI_ID_from_Bacterial_list(bacteria)
dict_1
