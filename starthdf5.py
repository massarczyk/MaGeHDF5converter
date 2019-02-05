
import io
import h5py
import numpy as np



print("write")
f = h5py.File("mytestfile.hdf5", "w")


##store each event as one array, and array of events as list
print("-----------")
event1 = np.arange(100)
event2 = np.arange(10)
mylist = np.array([event1 , event2])
#print mylist
string_dt = h5py.special_dtype(vlen=np.dtype('float32'))
dset0 = f.create_dataset("list", data=mylist, dtype=string_dt)

###############################################

arr = np.arange(100)
print arr
dset = f.create_dataset("init", data=arr)
dset.attrs['test'] = 12612
"""
dset = f.create_dataset("mydataset", (120,), dtype='i')
grp = f.create_group("subgroup")
dset2 = grp.create_dataset("another_dataset", (50,), dtype='f')

"""
dset3 = f.create_dataset('subgroup/dataset_two', (10,), dtype='i')
dset3 = f.create_dataset('subgroup/dataset_three', (10,), dtype='i')

###############################################
print("-----------")
print("read")

f = h5py.File("mytestfile.hdf5", "r")
print list(f.keys())
for name in f:
	print name


print("-----------")
dset = f['list']
print dset[0][1]
print dset.dtype
#print dset.attrs['test']



