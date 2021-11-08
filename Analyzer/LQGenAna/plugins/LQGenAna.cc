#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "FWCore/Utilities/interface/EDMException.h"
#include <iomanip>
#include <iostream>
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include <memory>
#include <iostream>
#include <sstream>
#include <istream>
#include <fstream>
#include <iomanip>
#include <string>
#include <cmath>
#include <functional>
#include <vector>
#include <cassert>

#include "FWCore/Framework/interface/Frameworkfwd.h"


#include "TFile.h"
#include "TH1D.h"
#include "TMath.h"
#include "TLorentzVector.h"
#include "TTree.h"
#include "TF1.h"

using namespace std;
using namespace edm;
using namespace lhef;

struct tree_struc_{
long unsigned int event;

int GenLepID;
int FinalLepID;
int GenQuarkID;
int FinalQuarkID;



float LQ_M;
float LQ_pz;
float LQ_E;
float LQ_ID;


float GenLep_pz;
float GenQuark_pz;




float FinalLep_pz;
float FinalLep_px;
float FinalLep_py;
float FinalLep_E;
float FinalLep_M;

float FinalQuark_pz;
float FinalQuark_px;
float FinalQuark_py;
float FinalQuark_E;
float FinalQuark_M;



float FinalQuark_pt;
float FinalQuark_eta;
float FinalQuark_phi;

float FinalQuark_Et;

float FinalLep_pt;
float FinalLep_eta;
float FinalLep_phi;

float FinalLep_Et;

double Xsec;
double XsecErr;
double XMaxUp;
double LPRUP;
};


class LQGenAna : public EDAnalyzer {
private: 
  bool dumpEvent_;
  bool dumpHeader_;
 edm::Service<TFileService> fs_;

  TTree* tree;
  tree_struc_ tree_;

  unsigned long int event=0;

public:
  explicit LQGenAna( const ParameterSet & cfg ) :
    dumpEvent_( cfg.getUntrackedParameter<bool>("dumpEvent",true) ),
    dumpHeader_( cfg.getUntrackedParameter<bool>("dumpHeader",false) ),
    tokenLHERunInfo_(consumes<LHERunInfoProduct,edm::InRun>(cfg.getUntrackedParameter<edm::InputTag>("moduleLabel", std::string("source")) ) ),
    tokenLHEEvent_(consumes<LHEEventProduct>(cfg.getUntrackedParameter<edm::InputTag>("moduleLabel", std::string("source")) ) )
  {
  }
private:

  void beginJob(){
  



  tree = fs_->make<TTree>("tree","tree");
  tree->Branch("event", &tree_.event, "event/I");
  
  tree->Branch("LQ_ID", &tree_.LQ_ID, "LQ_ID/I");
  tree->Branch("LQ_M", &tree_.LQ_M, "LQ_M/F");
  tree->Branch("LQ_E", &tree_.LQ_E, "LQ_E/F");
  tree->Branch("LQ_pz", &tree_.LQ_pz, "LQ_pz/F");


  tree->Branch("GenLepID", &tree_.GenLepID, "GenLepID/I");
  tree->Branch("FinalLepID", &tree_.FinalLepID, "FinalLepID/I");

  tree->Branch("GenLep_pz", &tree_.GenLep_pz, "GenLep_pz/F");
  tree->Branch("GenQuark_pz", &tree_.GenQuark_pz, "GenQuark_pz/F");

  tree->Branch("FinalLep_pz", &tree_.FinalLep_pz, "FinalLep_pz/F");
  tree->Branch("FinalLep_px", &tree_.FinalLep_px, "FinalLep_px/F");
  tree->Branch("FinalLep_py", &tree_.FinalLep_py, "FinalLep_py/F");
  tree->Branch("FinalLep_E", &tree_.FinalLep_E, "FinalLep_E/F");
  tree->Branch("FinalLep_M", &tree_.FinalLep_M, "FinalLep_M/F");
  
  tree->Branch("GenQuarkID", &tree_.GenQuarkID, "GenQuarkID/I");
  tree->Branch("FinalQuarkID", &tree_.FinalQuarkID, "FinalQuarkID/I");

  tree->Branch("FinalQuark_pz", &tree_.FinalQuark_pz, "FinalQuark_pz/F");
  tree->Branch("FinalQuark_px", &tree_.FinalQuark_px, "FinalQuark_px/F");
  tree->Branch("FinalQuark_py", &tree_.FinalQuark_py, "FinalQuark_py/F");
  tree->Branch("FinalQuark_E", &tree_.FinalQuark_E, "FinalQuark_E/F");
  tree->Branch("FinalQuark_M", &tree_.FinalQuark_M, "FinalQuark_M/F");


  tree->Branch("FinalLep_pt", &tree_.FinalLep_pt, "FinalLep_pt/F");
  tree->Branch("FinalLep_eta", &tree_.FinalLep_eta, "FinalLep_eta/F");
  tree->Branch("FinalLep_phi", &tree_.FinalLep_phi, "FinalLep_phi/F");
  tree->Branch("FinalLep_Et", &tree_.FinalLep_Et, "FinalLep_Et/F");


  tree->Branch("FinalQuark_pt", &tree_.FinalQuark_pt, "FinalQuark_pt/F");
  tree->Branch("FinalQuark_eta", &tree_.FinalQuark_eta, "FinalQuark_eta/F");
  tree->Branch("FinalQuark_phi", &tree_.FinalQuark_phi, "FinalQuark_phi/F");
  tree->Branch("FinalQuark_Et", &tree_.FinalQuark_Et, "FinalQuark_Et/F");


  tree->Branch("XSection", &tree_.Xsec, "XSection/D");
  tree->Branch("XSectErr", &tree_.XsecErr, "XSectErr/D");
  tree->Branch("XMaxUp", &tree_.XMaxUp, "XMaxUp/D");
  tree->Branch("LPRUP", &tree_.LPRUP, "LPRUP/D");
	

}


  void analyze( const Event & iEvent, const EventSetup & iSetup ) override {


    TLorentzVector* FinalLep=new TLorentzVector();
    TLorentzVector* FinalQuark=new TLorentzVector();
	
    event++;
    edm::Handle<LHEEventProduct> evt;
    iEvent.getByToken(tokenLHEEvent_, evt);


    const lhef::HEPEUP hepeup_ = evt->hepeup();

    const int nup_ = hepeup_.NUP; 
    const std::vector<int> idup_ = hepeup_.IDUP;
    const std::vector<lhef::HEPEUP::FiveVector> pup_ = hepeup_.PUP;


    if ( !dumpEvent_ ) { return; }
//    std::cout << "Number of particles = " << nup_ << std::endl;

    if ( evt->pdf() != NULL ) {
    }

    for ( unsigned int icount = 0 ; icount < (unsigned int)nup_; icount++ ) {

/*      std::cout << "# " << std::setw(14) << std::fixed << icount 
                << std::setw(14) << std::fixed << idup_[icount] 
                << std::setw(14) << std::fixed << (pup_[icount])[0] 
                << std::setw(14) << std::fixed << (pup_[icount])[1] 
                << std::setw(14) << std::fixed << (pup_[icount])[2] 
                << std::setw(14) << std::fixed << (pup_[icount])[3] 
                << std::setw(14) << std::fixed << (pup_[icount])[4] 
                << std::endl;*/
    if (idup_[icount]>20) {
		
	tree_.LQ_M=(pup_[icount])[4];
	tree_.LQ_E=(pup_[icount])[3];
	tree_.LQ_ID=idup_[icount];
	tree_.LQ_pz=(pup_[icount])[2];
	
	}
	else if ((idup_[icount]<10) && (icount<2)){

	tree_.GenQuarkID=idup_[icount];
	tree_.GenQuark_pz=(pup_[icount])[2];	

	}
	else if ((idup_[icount]<10) && (icount>2)){
	
	
	tree_.FinalQuarkID=idup_[icount];
	tree_.FinalQuark_pz=(pup_[icount])[2];
	tree_.FinalQuark_px=(pup_[icount])[0];
	tree_.FinalQuark_py=(pup_[icount])[1];
	tree_.FinalQuark_M=(pup_[icount])[4];
	tree_.FinalQuark_E=(pup_[icount])[3];
	FinalQuark->SetPxPyPzE((pup_[icount])[0], (pup_[icount])[1], (pup_[icount])[2], (pup_[icount])[3]);
    }
	else if ((idup_[icount]>10) && (icount<2)){
	
		
	tree_.GenLepID=idup_[icount];
	tree_.GenLep_pz=(pup_[icount])[2];	
	}
	else if ((idup_[icount]>10) && (icount>2)){
    	
	
	tree_.FinalLepID=idup_[icount];
	tree_.FinalLep_pz=(pup_[icount])[2];
	tree_.FinalLep_px=(pup_[icount])[0];
	tree_.FinalLep_py=(pup_[icount])[1];
	tree_.FinalLep_M=(pup_[icount])[4];
	tree_.FinalLep_E=(pup_[icount])[3];
	FinalLep->SetPxPyPzE((pup_[icount])[0], (pup_[icount])[1], (pup_[icount])[2], (pup_[icount])[3]);


	}
}
    if( evt->weights().size() ) {
      std::cout << "weights:" << std::endl;
      for ( size_t iwgt = 0; iwgt < evt->weights().size(); ++iwgt ) {
	const LHEEventProduct::WGT& wgt = evt->weights().at(iwgt);
	std::cout << "\t" << wgt.id << ' ' 
		  << std::scientific << wgt.wgt << std::endl;
      }
    }
   tree_.event=event;
   tree_.FinalLep_pt=FinalLep->Pt();
   tree_.FinalLep_eta=FinalLep->Eta();
   tree_.FinalLep_phi=FinalLep->Phi();
   tree_.FinalLep_Et=FinalLep->Et();
   	
	
   tree_.FinalQuark_pt=FinalQuark->Pt();
   tree_.FinalQuark_eta=FinalQuark->Eta();
   tree_.FinalQuark_phi=FinalQuark->Phi();
   tree_.FinalQuark_Et=FinalQuark->Et();



   tree->Fill();

  }

  void endRun(edm::Run const& iRun, edm::EventSetup const& es) override {

    Handle<LHERunInfoProduct> run;
    //iRun.getByLabel( src_, run );
    iRun.getByToken( tokenLHERunInfo_, run );

    const lhef::HEPRUP thisHeprup_ = run->heprup();

    for ( unsigned int iSize = 0 ; iSize < thisHeprup_.XSECUP.size() ; iSize++ ) {
    std::cout  << std::setw(14) << std::fixed << thisHeprup_.XSECUP[iSize]
                 << std::setw(14) << std::fixed << thisHeprup_.XERRUP[iSize]
                 << std::setw(14) << std::fixed << thisHeprup_.XMAXUP[iSize]
                 << std::setw(14) << std::fixed << thisHeprup_.LPRUP[iSize] 
                 << std::endl;
	
	tree_.Xsec=thisHeprup_.XSECUP[iSize];
	tree_.XsecErr=thisHeprup_.XERRUP[iSize];
	tree_.XMaxUp=thisHeprup_.XMAXUP[iSize];
	tree_.LPRUP=thisHeprup_.LPRUP[iSize];
	std::cout<<thisHeprup_.XSECUP[iSize]<<std::endl;
	
    }
    std::cout << " " << std::endl;
    tree->Fill();


    if(dumpHeader_) {
      std::cout <<" HEADER "<<std::endl;
      for(auto it = run->headers_begin(); it != run->headers_end(); ++it) {
        std::cout <<"tag: '"<<it->tag()<<"'"<<std::endl;
        for(auto const& l : it->lines()) {
          std::cout<<"   "<<l<<std::endl;
        }
      }
    }

  }

  edm::EDGetTokenT<LHERunInfoProduct> tokenLHERunInfo_;
  edm::EDGetTokenT<LHEEventProduct> tokenLHEEvent_;

};

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE( LQGenAna );


