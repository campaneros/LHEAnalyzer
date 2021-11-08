import ROOT as R
import numpy as np
import os
import sys
import math
import itertools
import json
from array import array



import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input',dest='input')

args = parser.parse_args()

R.gROOT.SetBatch(True)
R.gROOT.SetStyle('Modern')

f=R.TFile(args.input)
tree=f.Get("genAnalyzer/tree")

c=R.TCanvas("c1","c1",900,600)


labels={
	'pt':'pt (GeV)',
	'eta': 'eta',
	'phi': 'phi',
	'Et': 'Et (GeV)',
	'M': 'M (GeV)',

}
#use directly the functionin ROOT::MATH note that the parameters definition is different is (alpha, n sigma, mu)





histos={}
for hh in ['Quark','Lep','LQ']:
	if 'LQ' in hh:
		histos['%s_pz'%hh]=R.TH1F('%s_pz'%hh,'%s_pz'%hh,6000,-6000,6000)
		histos['%s_M'%hh]=R.TH1F('%s_M'%hh,'%s_M'%hh,1000, 0,6000)
		histos['%s_E'%hh]=R.TH1F('%s_E'%hh,'%s_E'%hh,1000, 0,6000)
	else:
		histos['Final%s_pt'%hh]=R.TH1F('Final%s_pt'%hh,'Final%s_pt'%hh,1000,-10,2000)
		histos['Final%s_phi'%hh]=R.TH1F('Final%s_phi'%hh,'Final%s_phi'%hh,50,-5,5)
		histos['Final%s_eta'%hh]=R.TH1F('Final%s_eta'%hh,'Final%s_eta'%hh,50,-5,5)
		histos['Final%s_Et'%hh]=R.TH1F('Final%s_Et'%hh,'Final%s_Et'%hh,1000,-10,2000)
		histos['Final%s_M'%hh]=R.TH1F('Final%s_M'%hh,'Final%s_M'%hh,100,0,10)

hh=R.TH1F('Final','Final',100,0,10)
for i in range(100):
	hh.Fill(R.gRandom.Gaus(0, 3))

for hh in ['LQ']:
	for tt in ['M','E','pz']:
		tree.Project('%s_%s'%(hh,tt),'%s_%s'%(hh,tt))
		if 'M' in tt:
			peak_ori=histos['%s_%s'%(hh,tt)].GetBinCenter(histos['%s_%s'%(hh,tt)].GetMaximumBin())
			print(peak_ori)
			peak=R.RooRealVar('peak','peak',peak_ori,0.95*peak_ori,1.05*peak_ori)
			alpha=R.RooRealVar('alpha','alpha',0.1,0.,2.0)
			alpha2=R.RooRealVar('alpha2','alpha2',1,0.,2.0)
			sigma=R.RooRealVar('sigma','sigma',50.,0,100.0)
			sigma2=R.RooRealVar('sigma2','sigma2',1.,0,2.0)
			fraction=R.RooRealVar('fraction','fraction',0.5,0,1.0)
			rho1=R.RooRealVar('rho1','rho1',-1,-2,1)
			rho2=R.RooRealVar('rho2','rho2',-1,-2,1)
			xprox=R.RooRealVar('xprox','xprox',0,-0.5,0.5)
			n=R.RooRealVar('n','n',5.0,0,10)
			n2=R.RooRealVar('n2','n2',5.0,0,10)
			x=R.RooRealVar('x','x',0.9*peak_ori,1.2*peak_ori)
			y=R.RooRealVar('y','y',0,10000)
			Rpdf=R.RooBreitWigner('BT','BT', x, peak, sigma)
			#Rpdf=R.RooGaussian('gauss','gauss',x,peak,sigma)
			#Rpdf=R.RooCBShape('crystalball','crystalball',x,peak,sigma,alpha,n)
			#Rpdf2=R.RooCBShape('crystalball2','crystalball2',x,peak,sigma2,alpha2,n2)
			#SPS_pdf=R.RooAddPdf("SPS_pdf", "SPS_pdf", R.RooArgList(Rpdf, Rpdf2), R.RooArgList(fraction), R.kTRUE);
			#Rpdf=R.RooBukinPdf('bukin','bukin',x,peak,sigma,xprox,rho1,rho2)
			Rfit_hist=R.RooDataHist("Rfit_hist", "Rfit_hist", R.RooArgList(x), R.RooFit.Import(histos['%s_%s'%(hh,tt)]))	
			Rpdf.fitTo(Rfit_hist)
			Rframe=x.frame()
			Rfit_hist.plotOn(Rframe)
			Rpdf.plotOn(Rframe)
			Rframe.GetYaxis().SetTitle("Events")
			Rframe.GetXaxis().SetTitle(tt)
			Rframe.SetTitle("Mass distribution")
			Rframe.Draw()		
			#Mass_fit=R.TF1("CrystalBall","[4]*ROOT::Math::crystalball_function(x, [0], [1], [2], [3])",500,6000)
			#Mass_fit=R.TF1("gauss","[0]*TMath::Gaus(x,[1],[2])")
			#norm=float(histos['%s_%s'%(hh,tt)].GetEntries())/histos['%s_%s'%(hh,tt)].GetNbinsX()	
			#print(norm)
			#Mass_fit.SetParameter(0,0.5)
			#Mass_fit.SetParLimits(0,0,3)
			#Mass_fit.SetParameter(1,peak_ori)
			#Mass_fit.SetParLimits(1,norm*0.1,norm)
			#Mass_fit.SetParameter(2,0.30)
			#Mass_fit.SetParLimits(2,0,50)
			#Mass_fit.SetParameter(3,peak_ori)
			#Mass_fit.SetParLimits(1,0.8*peak_ori,1.2*peak_ori)
			#Mass_fit.SetParameter(0,3000)
			#Mass_fit.SetParLimits(0,norm*0.1,3000)
		        #histos['%s_%s'%(hh,tt)].Draw()
                        #histos['%s_%s'%(hh,tt)].GetXaxis().SetTitle(tt)
			#histos['%s_%s'%(hh,tt)].Fit("gauss","LR+","",2800,3200) 
		
		else:	
			histos['%s_%s'%(hh,tt)].Draw()
                	histos['%s_%s'%(hh,tt)].GetXaxis().SetTitle(tt)
                for ext in ['png','pdf']:
                        c.SaveAs('Plots/%s_%s.%s'%(hh,tt,ext))
	

for hh in ['Quark','Lep']:
	for tt in ['pt','eta','phi','Et','M']:
		tree.Project('Final%s_%s'%(hh,tt),'Final%s_%s'%(hh,tt))
		histos['Final%s_%s'%(hh,tt)].Draw()
		histos['Final%s_%s'%(hh,tt)].GetXaxis().SetTitle(tt)
		for ext in ['png','pdf']:
			c.SaveAs('Plots/%s_%s.%s'%(hh,tt,ext))





