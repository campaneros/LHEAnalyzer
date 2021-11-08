import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing


process = cms.Process("LHE")


options = VarParsing.VarParsing ('standard')

# setup any defaults you want
options.output = "Rootfiles/lhe_M3000.root"
options.files= 'file:pwgevents.lhe'
#options.files= 'root://eoscms///eos/cms/store/cmst3/user/santanas/MCsamples/TrijetRes_g_ggg_BP2_testV2/TrijetRes_g_ggg_BP2_testV2_MGKK2000R0p7_slc6_amd64_gcc481_CMSSW_7_1_30_GEN.root'
options.maxEvents = -1
options.parseArguments()

process.MessageLogger.cerr.FwkReport.reportEvery = 100

 
process.source = cms.Source("LHESource",
   	fileNames = cms.untracked.vstring(options.files)
)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.configurationMetadata = cms.untracked.PSet(
	version = cms.untracked.string('alpha'),
	name = cms.untracked.string('LHEF input'),
	annotation = cms.untracked.string('ttbar')
)

process.load("FWCore.MessageService.MessageLogger_cfi")
#process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cout = cms.untracked.PSet( threshold = cms.untracked.string('INFO') )

process.LHE = cms.OutputModule("PoolOutputModule",
	dataset = cms.untracked.PSet(dataTier = cms.untracked.string('LHE')),
	fileName = cms.untracked.string(options.output)
)

#process.lhedump = cms.EDAnalyzer("DummyLHEAnalyzer",
#                                 src = cms.InputTag("source")
#                                 )


process.outpath = cms.EndPath(process.LHE)
