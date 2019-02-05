# MaGeHDF5converter
So it converts the root files into a HDF5 format without using any extra classes in the final hdf5, I removed some stuff I think which are unneccesary. There is a list of the branches at the end, which shows which are used and which i skipped



Problems I have

- compression, file size is mainly driven by the strings. There are two option , see line 263-266.
  if i use vlen=str the files are smaller, but the processname is not an array, its one long string. This could be split, but thats an extra step
  if I use the fixed size with 'S...' the names are split but also the size is much bigger
  
- needs a lot of ram
  I write the lists first and then to file. I found some example in the web where this is done the other way around, the datasets are first created and then filled while looping. But, when I tried this first i had troubles due to the flexible step size
  
- troubles with the MGMCRun (an MGDO class) there is the 
  std::map< std::string, int > fSensitiveVolumeIDs with a function using it. But I cant access the map itself
