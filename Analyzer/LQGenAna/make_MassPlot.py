import ROOT as R
import numpy as np
import os
import sys
import math
import itertools
import json
from array import array

def Map(tf):
    """                                                                                                                  
    Maps objets as dict[obj_name][0] using a TFile (tf) and TObject to browse.                                           
    """
    m = {}
    for k in tf.GetListOfKeys():
        n = k.GetName()
        m[n] = tf.Get(n)
    return m

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input',dest='input')

args = parser.parse_args()

R.gROOT.SetBatch(True)
R.gROOT.SetStyle('Modern')


c=R.TCanvas("c1","c1",900,600)


labels={
        'pt':'pt (GeV)',
        'eta': 'eta',
        'phi': 'phi',
        'Et': 'Et (GeV)',
        'M': 'M (GeV)',

}


histos={}

histos['Mass']=R.TH1F('Mass','Mass',6000,0,6000)
f=R.TFile("Plots/"+args.input+".root")
his=Map(f)
for ip,h in enumerate(his):
	if '_M' in h:
		print(h)	
		histos['%s'%h]=f.Get('%s'%h)	
		if ip == 0:
			histos['%s'%h].Draw("AP")
		else:
			histos['%s'%h].Draw("SAME")

c.SaveAs("Plots/test.png")
