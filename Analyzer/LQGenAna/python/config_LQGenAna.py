import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

#process = cms.Process("Demo")

# setup 'standard'  options
options = VarParsing.VarParsing ('standard')


# setup any defaults you want
options.output = "Rootfiles/GenAna.root"
options.files= 'file:lhe.root'
#options.files= 'root://eoscms///eos/cms/store/cmst3/user/santanas/MCsamples/TrijetRes_g_ggg_BP2_testV2/TrijetRes_g_ggg_BP2_testV2_MGKK2000R0p7_slc6_amd64_gcc481_CMSSW_7_1_30_GEN.root'
options.maxEvents = -1
options.parseArguments()

process = cms.Process("dumpLHE")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring('file:lhe.root')
#)




process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(options.files)
)

process.TFileService=cms.Service("TFileService",
                                 #fileName=cms.string("test.root"),
				 fileName=cms.string(options.output),
                                closeFileFast = cms.untracked.bool(True)
                                )


process.genAnalyzer = cms.EDAnalyzer('LQGenAna',
				      moduleLabel = cms.untracked.InputTag('source'),
				      #LHEEventInfo = cms.InputTag('Info'),
)


process.p = cms.Path(process.genAnalyzer)
