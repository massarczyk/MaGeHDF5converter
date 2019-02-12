#!/usr/bin/env python3
import h5py
import uproot
import awkward
import argparse

def main():
    """
    python converter_v2.py [/path/to/inFile] [outDir]
    """
    par = argparse.ArgumentParser(description="MaGe ROOT->HDF5 converter")
    arg = par.add_argument
    arg('in_file', action="store", type=str, help="input file (required)")
    arg('out_dir', action="store", type=str, help="output directory (required)")
    arg('-t', "--test", action="store_true", help="test mode")
    arg('-r', "--read", action="store_true", help="read mode")
    arg('-m', "--manual", action="store_true", help="manual conversion mode")
    args = vars(par.parse_args())

    # get input and output files
    tmp = args["in_file"].split("/")
    in_path = "/".join(tmp[:-1])
    in_file = tmp[-1]
    out_file = "{}/{}.h5".format(args["out_dir"], in_file.split(".")[0])

    print("Converting file: {}\n     into file: {}".format(in_file, out_file))

    if args["test"]:
        test_uproot()
        exit()

    if args["read"]:
        read_file(out_file)
        exit()

    if args["manual"]:
        manual_convert(in_file, out_file)
        exit()

    # default (no options) -- run conversion
    uproot_file(in_file, out_file)


def uproot_file(in_file, out_file):
    """
    use uproot to make this a breeze
    """
    tt = uproot.open(in_file)["fTree"]
    arrs = tt.arrays() # supposed to read everything

    f_out = h5py.File(out_file, "w")
    ah5 = awkward.hdf5(f_out)

    for key in arrs:

        k = key.decode("utf-8")

        if isinstance(arrs[key], awkward.ObjectArray) or "MGTDataObject" in k:
            # skip these for now
            continue

        if "." in k:
            k = k.replace(".","/")

        ah5[k] = arrs[key]

    f_out.close()


def read_file(in_file):

    print("Reading file:", in_file)

    f = h5py.File(in_file)

    mylist = []
    f.visit(mylist.append)

    for grp in mylist:
        print(grp, type(f[grp]))

    f.close()


def manual_convert(in_file, out_file):
    """
    manually convert to h5py, checking for data types, etc.
    load the mage tree and loop over all interesting branches
    that can be converted to numpy types
    """
    from ROOT import TFile, TTree
    from ROOT import MGTMCRun, MGTMCEventHeader, MGTMCEventSteps, MGTMCStepData

    tf = TFile(in_file)
    mage_tree = tf.Get("fTree")
    # mage_tree.Print("toponly")

    # nl = mage_tree.GetListOfLeaves().GetEntries()
    for leaf in mage_tree.GetListOfLeaves():

        br = leaf.GetBranch()
        br_name = leaf.GetName()
        br_size = br.GetZipBytes()
        br_class = br.GetClassName() # this will be one of the classes we imported above

        if any(x in br_name for x in ["_","MGTDataObject"]) or br_size==0:
            print("    skipping:", br_name)
            continue

        print(br_name, br_size, br.GetClassName())

        # TODO: finish this
        # need to manually check for datatypes, specify the numpy datatype
        # we want to convert to, then run h5py.create_group and
        # h5py.create_dataset


def test_uproot():

    in_file = "Pos-04-00040.root"

    f = uproot.open(in_file)
    # f_keys = f.keys()

    tt = uproot.open(in_file)['fTree'] # <class 'uproot.rootio.TTree'>
    # print(tt.allkeys())
    # print(type(tt))
    # tt.show() # print a big list of everything uproot can access

    # [b'fMCRun', b'eventHeader', b'eventSteps', b'eventPrimaries']
    # print(tt.keys())

    # print(tt["eventSteps"])
    # tt.arrays(["eventSteps"])

    fsteps = tt["fSteps.fX"].array() # <class 'awkward.array.jagged.JaggedArray'>
    print(fsteps.shape)
    print(type(fsteps))

    print(tt["fSteps.fX"])

    # print(tt["fSteps.fX"].array())

    # for key in tt.allkeys():
    #
    #     dtype = tt[key].interpretation
    #     if dtype is None:
    #         # print("Can't read branch:", key)
    #         continue
    #
    #     # can swap out the interpretation
    #     # tree.arrays({"Float64": uproot.asarray(">f8", myarray)})
    #
    #     arr = tt[key].array()
    #
    #     print(key, arr.shape, type(arr))
    #     # exit()

    # explictly say which branches we can and can't read
    # branch_list = []
    # for key in tt.allkeys():
    #     if tt[key].interpretation is None:
    #         continue
    #     branch_list.append(key)

    # reads the tree once, returns a dict
    arrs = tt.arrays()

    # for key in arrs:
    #     print(key, type(arrs[key]), arrs[key].shape)
    #     if isinstance(arrs[key], awkward.JaggedArray):
    #         print("found one")

    test_arr = tt["fSteps.fPx"].array()

    # print(type(test_arr))

    # test hdf5 output

    # the source code is at:
    # https://github.com/scikit-hep/awkward-array/blob/01baec9b44e2a17a709c6c1d4cba2df753618c59/awkward/persist.py

    # Write
    with h5py.File("decode_test.h5", "w") as hf:
        # a = awkward.JaggedArray.fromiter(input_arr)
        ah5 = awkward.hdf5(hf)
        print(type(ah5))
        ah5["example"] = test_arr

    # Read
    with h5py.File("decode_test.h5") as hf:
        ah5 = awkward.hdf5(hf)
        b = ah5["example"]

    assert test_arr.tolist() == b.tolist()

    # print(test_arr.tolist() == b.tolist())



if __name__=="__main__":
    main()