#####################################################
#use as 
#python converter.py [inDir] [inFile] [outDir]
#####################################################

#!/usr/bin/env python
import sys, time, os, pywt
from ROOT import TFile, TTree, TBranch, TEntryList, gDirectory, TNamed, std, TObject, MGTWaveform, MGTMCRun, MGTMCEventSteps, MGTMCEventHeader, MGTMCStepData
import ROOT as R
import numpy as np
import pandas as pd
import warnings
import h5py

#####################################################
def main(argv):
	inDir, outDir = ".", "."
	
	if len(argv) == 0: 
		return
	###############
	###open File
	inDir = str(argv[0])
	inFileName = str(argv[1])
	outDir = str(argv[2])
	outFileName = outDir + '/' + inFileName.split('.')[0] + '.hdf5'
	print ("Scanning File: {}".format(inFileName))
	
	inFile = TFile("%s/%s" % (inDir, inFileName))
	mageTree = inFile.Get("fTree")

	###############
	###open set Tree Branches 
	#mageTree.Print()
	numberOfEvents = mageTree.GetEntries() - 1
	print ("File with ", numberOfEvents, " Events");
	#numberOfEvents = 2000

	runHeader = MGTMCRun()
	eventHeader = MGTMCEventHeader()
	eventSteps = MGTMCEventSteps()
	primaryStep = MGTMCEventSteps()
	mageTree.SetBranchAddress('fMCRun', runHeader);
	mageTree.SetBranchAddress('eventHeader', eventHeader);
	mageTree.SetBranchAddress('eventSteps', eventSteps);
	mageTree.SetBranchAddress('eventPrimaries', primaryStep);

	stepData = MGTMCStepData()
	
	###############
	###set the output lists

	List_EventID = []
	List_RandGenState = []
	List_TotalEnergy = []
	List_IsHeartbeatEvent = []

	List_StepIsPreStep = []
	List_StepParticleID = []
	List_StepTrackID = []
	List_StepParentTrackID = []
	List_StepProcessName = []
	List_StepPhysVolName = []
	List_StepCopyNo = []
	List_StepSensVolID = []
	List_StepT = []
	List_StepToffset = []
	List_StepEdep = []
	List_StepKineticE = []
	List_StepLength = []
	List_StepTotalTrackLength = []
	List_StepX = []
	List_StepY = []
	List_StepZ = []
	List_StepLocalX = []
	List_StepLocalY = []
	List_StepLocalZ = []
	List_StepPx = []
	List_StepPy = []
	List_StepPz = []
	List_StepNumber = []

	List_StartIsPreStep = []
	List_StartParticleID = []
	List_StartTrackID = []
	List_StartParentTrackID = []
	List_StartProcessName = []
	List_StartPhysVolName = []
	List_StartCopyNo = []
	List_StartSensVolID = []
	List_StartT = []
	List_StartToffset = []
	List_StartKineticE = []
	List_StartX = []
	List_StartY = []
	List_StartZ = []
	List_StartLocalX = []
	List_StartLocalY = []
	List_StartLocalZ = []
	List_StartPx = []
	List_StartPy = []
	List_StartPz = []
	List_StartWeight = []


	###############
	###run through the tree
	for i in range(1,numberOfEvents):
		mageTree.GetEntry(i)
		if i % 1000 == 0:
			print("Event ", i, " of ", numberOfEvents)
		#information from the header
		List_EventID.append(eventHeader.GetEventID())
		List_RandGenState.append(eventHeader.GetRandGenState())
		List_TotalEnergy.append(eventHeader.GetTotalEnergy())
		List_IsHeartbeatEvent.append(eventHeader.GetIsHeartbeatEvent())

		#reset the vectors
		Event_StepIsPreStep = np.zeros(eventSteps.GetNSteps())
		Event_StepParticleID = np.zeros(eventSteps.GetNSteps())
		Event_StepTrackID = np.zeros(eventSteps.GetNSteps())
		Event_StepParentTrackID = np.zeros(eventSteps.GetNSteps())
		Event_StepProcessName = np.empty(eventSteps.GetNSteps(),dtype=np.dtype("S200"))
		Event_StepPhysVolName = np.empty(eventSteps.GetNSteps(),dtype=np.dtype("S200"))
		Event_StepCopyNo = np.zeros(eventSteps.GetNSteps())
		Event_StepSensVolID = np.zeros(eventSteps.GetNSteps())
		Event_StepT = np.zeros(eventSteps.GetNSteps())
		Event_StepToffset = np.zeros(eventSteps.GetNSteps())
		Event_StepEdep = np.zeros(eventSteps.GetNSteps())
		Event_StepKineticE = np.zeros(eventSteps.GetNSteps())
		Event_StepLength = np.zeros(eventSteps.GetNSteps())
		Event_StepTotalTrackLength = np.zeros(eventSteps.GetNSteps())
		Event_StepX = np.zeros(eventSteps.GetNSteps())
		Event_StepY = np.zeros(eventSteps.GetNSteps())
		Event_StepZ = np.zeros(eventSteps.GetNSteps())
		Event_StepLocalX = np.zeros(eventSteps.GetNSteps())
		Event_StepLocalY = np.zeros(eventSteps.GetNSteps())
		Event_StepLocalZ = np.zeros(eventSteps.GetNSteps())
		Event_StepPx = np.zeros(eventSteps.GetNSteps())
		Event_StepPy = np.zeros(eventSteps.GetNSteps())
		Event_StepPz = np.zeros(eventSteps.GetNSteps())
		Event_StepNumber = np.zeros(eventSteps.GetNSteps())

		###individual steps
		for j in range(eventSteps.GetNSteps()):
			stepData=eventSteps.GetStep(j);
			#print("---",j," ",stepData.GetEdep()," ",stepData.GetLocalX()," ",stepData.GetProcessName())
			Event_StepIsPreStep[j] = stepData.GetIsPreStep()
			Event_StepParticleID[j] = stepData.GetParticleID()
			Event_StepTrackID[j] = stepData.GetTrackID()
			Event_StepParentTrackID[j] = stepData.GetParentTrackID()
			Event_StepProcessName[j] = stepData.GetProcessName()
			Event_StepPhysVolName[j] = stepData.GetPhysVolName()
			Event_StepCopyNo[j] = stepData.GetCopyNo()
			Event_StepSensVolID[j] = stepData.GetSensitiveVolumeID()
			Event_StepT[j] = stepData.GetT()
			Event_StepToffset[j] = stepData.GetTimeOffset()
			Event_StepEdep[j] = stepData.GetEdep()
			Event_StepKineticE[j] = stepData.GetKineticE()
			Event_StepLength[j] = stepData.GetStepLength()
			Event_StepTotalTrackLength[j] = stepData.GetTotalTrackLength()
			Event_StepX[j] = stepData.GetX()
			Event_StepY[j] = stepData.GetY()
			Event_StepZ[j] = stepData.GetZ()
			Event_StepLocalX[j] = stepData.GetLocalX()
			Event_StepLocalY[j] = stepData.GetLocalY()
			Event_StepLocalZ[j] = stepData.GetLocalZ()
			Event_StepPx[j] = stepData.GetPx()
			Event_StepPy[j] = stepData.GetPy()
			Event_StepPz[j] = stepData.GetPz()
			Event_StepNumber[j] = stepData.GetStepNumber()

		List_StepIsPreStep.append(Event_StepIsPreStep)
		List_StepParticleID.append(Event_StepParticleID)
		List_StepTrackID.append(Event_StepTrackID)
		List_StepParentTrackID.append(Event_StepParentTrackID)
		List_StepProcessName.append(Event_StepProcessName)
		List_StepPhysVolName.append(Event_StepPhysVolName)
		List_StepCopyNo.append(Event_StepCopyNo)
		List_StepSensVolID.append(Event_StepSensVolID)		
		List_StepT.append(Event_StepT)
		List_StepToffset.append(Event_StepToffset)		
		List_StepEdep.append(Event_StepEdep)
		List_StepKineticE.append(Event_StepKineticE)
		List_StepLength.append(Event_StepLength)
		List_StepTotalTrackLength.append(Event_StepTotalTrackLength)
		List_StepX.append(Event_StepX)
		List_StepY.append(Event_StepY)
		List_StepZ.append(Event_StepZ)
		List_StepLocalX.append(Event_StepLocalX)
		List_StepLocalY.append(Event_StepLocalY)
		List_StepLocalZ.append(Event_StepLocalZ)
		List_StepPx.append(Event_StepPx)
		List_StepPy.append(Event_StepPy)
		List_StepPz.append(Event_StepPz)
		List_StepNumber.append(Event_StepNumber)

		###start particle information
		List_StartIsPreStep.append(primaryStep.GetStep(0).GetIsPreStep())
		List_StartParticleID.append(primaryStep.GetStep(0).GetParticleID())
		List_StartTrackID.append(primaryStep.GetStep(0).GetTrackID())
		List_StartParentTrackID.append(primaryStep.GetStep(0).GetParentTrackID())
		List_StartProcessName.append(primaryStep.GetStep(0).GetProcessName())
		List_StartPhysVolName.append(primaryStep.GetStep(0).GetPhysVolName())
		List_StartCopyNo.append(primaryStep.GetStep(0).GetCopyNo())
		List_StartSensVolID.append(primaryStep.GetStep(0).GetSensitiveVolumeID())
		List_StartT.append(primaryStep.GetStep(0).GetT())		
		List_StartToffset.append(primaryStep.GetStep(0).GetTimeOffset())		
		List_StartKineticE.append(primaryStep.GetStep(0).GetKineticE())		
		List_StartX.append(primaryStep.GetStep(0).GetX())
		List_StartY.append(primaryStep.GetStep(0).GetY())
		List_StartZ.append(primaryStep.GetStep(0).GetZ())
		List_StartLocalX.append(primaryStep.GetStep(0).GetLocalX())
		List_StartLocalY.append(primaryStep.GetStep(0).GetLocalY())
		List_StartLocalZ.append(primaryStep.GetStep(0).GetLocalZ())
		List_StartPx.append(primaryStep.GetStep(0).GetPx())
		List_StartPy.append(primaryStep.GetStep(0).GetPx())
		List_StartPz.append(primaryStep.GetStep(0).GetPz())
		List_StartWeight.append(primaryStep.GetStep(0).GetTrackWeight())

	### use the last event to get the MCRUN informations
	fRunID = runHeader.GetRunID()
	fNEvents = runHeader.GetNEvents()
	fDescription = runHeader.GetDescription()
	fWriteRandGenState = runHeader.GetWriteRandGenState()
	fWriteAllSteps = runHeader.GetWriteAllSteps()
	fWriteAllStepsInEventsThatDepositEnergy = runHeader.GetWriteAllStepsInEventsThatDepositEnergy()
	fKillAlphas = runHeader.GetKillAlphas()
	fKillBetas = runHeader.GetKillBetas()
	fKillGammas = runHeader.GetKillGammas()
	fKillNeutrons = runHeader.GetKillNeutrons()
	fStopNuclei = runHeader.GetStopNuclei()
	fUseTimeWindow = runHeader.GetUseTimeWindow()
	fTimeWindow = runHeader.GetTimeWindow()
	fUseImportanceSampling = runHeader.GetUseImportanceSampling()
	fBiasedParticleID = runHeader.GetBiasedParticleID()
	fUseImportanceProcessWindow = runHeader.GetUseImportanceProcessWindow()
	fUseParallelWorld = runHeader.GetUseParallelWorld()
	fAmax = runHeader.GetAmax()
	fAmin = runHeader.GetAmin()
	fZmax = runHeader.GetZmax()
	fZmin = runHeader.GetZmin()
	fMaGeRevision = runHeader.GetMaGeRevision()
	fMaGeTag = runHeader.GetMaGeTag()
	fMGDORevision = runHeader.GetMGDORevision()
	fMGDOTag = runHeader.GetMGDOTag()
	fGeantVersion = runHeader.GetGeantVersion()
	fCLHEPVersion = runHeader.GetCLHEPVersion()
	fROOTVersion = runHeader.GetROOTVersion()

	#print List_StepProcessName
	#print max(map(len,List_StepProcessName))
	#print List_StepPhysVolName
	#print max(map(len,List_StepPhysVolName))
	###############
	### the output
	print("write file")
	f = h5py.File(outFileName, "w") #output file

	#data types
	float_dt = h5py.special_dtype(vlen=np.dtype('f')) 
	int_dt = h5py.special_dtype(vlen=np.dtype('i')) 
	string1_dt = h5py.special_dtype(vlen=np.dtype('S{0}'.format(max(map(len,List_StepProcessName))))) 
	string2_dt = h5py.special_dtype(vlen=np.dtype('S{0}'.format(max(map(len,List_StepPhysVolName))))) 
	string1_dt = h5py.special_dtype(vlen=str) 
	string2_dt = h5py.special_dtype(vlen=str) 
	bool_dt = h5py.special_dtype(vlen=np.dtype('b')) 

	###RunInfos attached to File as attributes
	f.attrs['RunID'] = fRunID
	f.attrs['NEvents'] = fNEvents
	f.attrs['Description'] = fDescription
	f.attrs['WriteRandGenState'] = fWriteRandGenState
	f.attrs['WriteAllSteps'] = fWriteAllSteps
	f.attrs['WriteAllStepsInEventsThatDepositEnergy'] = fWriteAllStepsInEventsThatDepositEnergy
	f.attrs['KillAlphas'] = fKillAlphas
	f.attrs['KillBetas'] = fKillBetas
	f.attrs['KillGammas'] = fKillGammas
	f.attrs['KillNeutrons'] = fKillNeutrons
	f.attrs['fStopNuclei'] = fStopNuclei
	f.attrs['UseTimeWindow'] = fUseTimeWindow
	f.attrs['TimeWindow'] = fTimeWindow
	f.attrs['UseImportanceSampling'] = fUseImportanceSampling
	f.attrs['BiasedParticleID'] = fBiasedParticleID
	f.attrs['UseImportanceProcessWindow'] = fUseImportanceProcessWindow
	f.attrs['UseParallelWorld'] = fUseParallelWorld
	f.attrs['Amax'] = fAmax
	f.attrs['Amin'] = fAmin
	f.attrs['Zmax'] = fZmax
	f.attrs['Zmin'] = fZmin
	f.attrs['MaGeRevision'] = fMaGeRevision
	f.attrs['MaGeTag'] = fMaGeTag
	f.attrs['MGDORevision'] = fMGDORevision
	f.attrs['MGDOTag'] = fMGDOTag
	f.attrs['GeantVersion'] = fGeantVersion
	f.attrs['CLHEPVersion'] = fCLHEPVersion
	f.attrs['ROOTVersion'] = fROOTVersion

	###write header info
	###write the EventID array into the general info, instead of twice to start and step
	###use the EventID as DataSet, and add the MCRUN stuff as attributes
	f.create_dataset("EventHeader/EventID", data=List_EventID, compression="gzip", compression_opts=9)
	f.create_dataset("EventHeader/RandGenState", data=List_RandGenState, compression="gzip", compression_opts=9)
	f.create_dataset("EventHeader/TotalEnergy", data=List_TotalEnergy, compression="gzip", compression_opts=9)
	f.create_dataset("EventHeader/IsHeartbeatEvent", data=List_IsHeartbeatEvent, compression="gzip", compression_opts=9)

	###steps in detector informations
	f.create_dataset("Event/StepIsPreStep", data=List_StepIsPreStep, dtype=bool_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepParticleID", data=List_StepParticleID, dtype=int_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepTrackID", data=List_StepTrackID, dtype=int_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepParentTrackID", data=List_StepParentTrackID, dtype=int_dt, compression="gzip", compression_opts=9)
	f.create_dataset(u"Event/StepProcessName", data=List_StepProcessName, dtype=string1_dt, compression="gzip", compression_opts=9)
	f.create_dataset(u"Event/StepPhysVolName", data=List_StepPhysVolName, dtype=string2_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepCopyNo", data=List_StepCopyNo, dtype=int_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepSensVolID", data=List_StepSensVolID, dtype=int_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepT", data=List_StepT, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepToffset", data=List_StepToffset, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepEdep", data=List_StepEdep, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepKineticE", data=List_StepKineticE, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepLength", data=List_StepLength, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/TotalTrackLength", data=List_StepTotalTrackLength, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepX", data=List_StepX, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepY", data=List_StepY, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepZ", data=List_StepZ, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepLocalX", data=List_StepLocalX, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepLocalY", data=List_StepLocalY, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepLocalZ", data=List_StepLocalZ, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepPx", data=List_StepPx, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepPy", data=List_StepPy, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepPz", data=List_StepPz, dtype=float_dt, compression="gzip", compression_opts=9)
	f.create_dataset("Event/StepNumber", data=List_StepNumber, dtype=int_dt, compression="gzip", compression_opts=9)

	###Starting particle
	f.create_dataset("Start/IsPreStep", data=List_StartIsPreStep, compression="gzip", compression_opts=9)
	f.create_dataset("Start/ParticleID", data=List_StartParticleID, compression="gzip", compression_opts=9)
	f.create_dataset("Start/TrackID", data=List_StartTrackID, compression="gzip", compression_opts=9)
	f.create_dataset("Start/ParentTrackID", data=List_StartParentTrackID, compression="gzip", compression_opts=9)
	f.create_dataset("Start/ProcessName", data=List_StartProcessName, compression="gzip", compression_opts=9)
	f.create_dataset("Start/PhysVolName", data=List_StartPhysVolName, compression="gzip", compression_opts=9)
	f.create_dataset("Start/CopyNo", data=List_StartCopyNo, compression="gzip", compression_opts=9)
	f.create_dataset("Start/SensVolID", data=List_StartSensVolID, compression="gzip", compression_opts=9)
	f.create_dataset("Start/T", data=List_StartT, compression="gzip", compression_opts=9)
	f.create_dataset("Start/TOffset", data=List_StartToffset, compression="gzip", compression_opts=9)
	f.create_dataset("Start/KineticeE", data=List_StartKineticE, compression="gzip", compression_opts=9)
	f.create_dataset("Start/X", data=List_StartX, compression="gzip", compression_opts=9)
	f.create_dataset("Start/Y", data=List_StartY, compression="gzip", compression_opts=9)
	f.create_dataset("Start/Z", data=List_StartZ, compression="gzip", compression_opts=9)
	f.create_dataset("Start/LocalX", data=List_StartLocalX, compression="gzip", compression_opts=9)
	f.create_dataset("Start/LocalY", data=List_StartLocalY, compression="gzip", compression_opts=9)
	f.create_dataset("Start/LocalZ", data=List_StartLocalZ, compression="gzip", compression_opts=9)
	f.create_dataset("Start/Px", data=List_StartPx, compression="gzip", compression_opts=9)
	f.create_dataset("Start/Py", data=List_StartPy, compression="gzip", compression_opts=9)
	f.create_dataset("Start/Pz", data=List_StartPz, compression="gzip", compression_opts=9)
	f.create_dataset("Start/Weight", data=List_StartWeight, compression="gzip", compression_opts=9)

	f.close()


	###############
	###check afterwards
	f = h5py.File(outFileName, "r")
	print("-----------")
	print("#### attributes ####")
	for name in f.attrs.keys():
		print name
	print("#### groups ####")
	for name in f.keys():
		print name
		for item in f.require_group(name).keys():
			print("--", name, "/" ,item)


	print("-----------")

	dset0 = f['Event/StepPhysVolName']
	#dset0 = f['Event/StepLocalX']
	#print(dset0[8])
	#print(f.attrs['RunID'])

	f.close()



#####################################################

if __name__ == "__main__":
	main(sys.argv[1:])

#####################################################
###these are the baskets of the MaGe Root files
"""
	leafArray = mageTree.GetListOfLeaves()
	for i in range(leafArray.GetSize()):
		leaf = leafArray.At(i)
		branch = leaf.GetBranch()
		motherbranch = branch.GetMother()
		print i," ",branch.GetName()," ",motherbranch.GetName(), " leaf ",leaf.GetTypeName()," ",leaf.GetName()


not neccesary	0   fMCRun
not neccesary	1   MGTDataObject
done					2   fRunID
done					3   fNEvents
done					4   fDescription
dont know how	5   fSensitiveVolumeIDs
done					6   fWriteRandGenState
done					7   fWriteAllSteps
done					8   fWriteAllStepsInEventsThatDepositEnergy
done					9   fKillAlphas
done					10   fKillBetas
done					11   fKillGammas
done					12   fKillNeutrons
done					13   fStopNuclei
done					14   fUseTimeWindow
done					15   fTimeWindow
done					16   fUseImportanceSampling
done					17   fBiasedParticleID
done					18   fUseImportanceProcessWindow
done					19   fUseParallelWorld
done					20   fAmax
done					21   fAmin
done					22   fZmax
done					23   fZmin
done					24   fMaGeRevision
done					25   fMaGeTag
done					26   fMGDORevision
done					27   fMGDOTag
done					28   fGeantVersion
done					29   fCLHEPVersion
done					30   fROOTVersion
not neccesary	31   eventHeader
not neccesary	32   MGTDataObject
done					33   fEventID
done					34   fRandGenState
done					35   fTotalEnergy
done					36   fIsHeartbeatEvent
skipped				37   fEnergyOfDetectorID
skipped				38   eventSteps
skipped				39   MGTDataObject
skipped				40   fEventID
skipped				41   fNSteps
not neccesary	42   fSteps
not neccesary	43   fSteps.MGTDataObject
done    			44   fSteps.fIsPreStep
done    			45   fSteps.fParticleID
done    			46   fSteps.fTrackID
done    			47   fSteps.fParentTrackID
done    			48   fSteps.fProcessName
done    			49   fSteps.fPhysVolName
done    			50   fSteps.fCopyNo
done    			51   fSteps.fSensVolID
done    			52   fSteps.fT
done    			53   fSteps.fTimeOffset
done    			54   fSteps.fEdep
done					55   fSteps.fKineticEnergy
done					56   fSteps.fStepLength
done					57   fSteps.fTotalTrackLength
done					58   fSteps.fX
done					59   fSteps.fY
done					60   fSteps.fZ
done					61   fSteps.fLocalX
done					62   fSteps.fLocalY
done					63   fSteps.fLocalZ
done					64   fSteps.fPx
done					65   fSteps.fPy
done					66   fSteps.fPz
done					67   fSteps.fStepNumber
done					68   fSteps.fTrackWeight
not neccesary	69   eventPrimaries
not neccesary	70   MGTDataObject
skipped				71   fEventID
skipped				72   fNSteps
not neccesary	73   fSteps
not neccesary	74   fSteps.MGTDataObject
done					75   fSteps.fIsPreStep
done					76   fSteps.fParticleID
done					77   fSteps.fTrackID
done					78   fSteps.fParentTrackID
done					79   fSteps.fProcessName
done					80   fSteps.fPhysVolName
done					81   fSteps.fCopyNo
done					82   fSteps.fSensVolID
done					83   fSteps.fT
done 					84   fSteps.fTimeOffset
skipped				85   fSteps.fEdep
done 					86   fSteps.fKineticEnergy
skipped				87   fSteps.fStepLength
skipped				88   fSteps.fTotalTrackLength
done					89   fSteps.fX
done					90   fSteps.fY
done					91   fSteps.fZ
done					92   fSteps.fLocalX
done 					93   fSteps.fLocalY
done 					94   fSteps.fLocalZ
done					95   fSteps.fPx
done					96   fSteps.fPy
done 					97   fSteps.fPz
skipped 			98   fSteps.fStepNumber
done    			99   fSteps.fTrackWeight 
"""				

