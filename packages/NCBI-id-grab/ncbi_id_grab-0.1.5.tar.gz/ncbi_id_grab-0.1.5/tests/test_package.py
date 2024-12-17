# Testing the package for small size
from NCBI_ID_grab import IDfind

bacteria = ['Eubacterium_sp.', 'Ruminococcaceae_', 'Blautia_', 'Lactiplantibacillus_plantarum']
dict_1 = IDfind.NCBI_ID(bacteria) # Input must be a list.
print(dict_1)