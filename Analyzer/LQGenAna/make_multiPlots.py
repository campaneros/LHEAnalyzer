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


c=R.TCanvas("c1","c1",900,600)


labels={
	'pt':'pt (GeV)',
	'eta': 'eta',
	'phi': 'phi',
	'Et': 'Et (GeV)',
	'M': 'M (GeV)',

}
#use directly the functionin ROOT::MATH note that the parameters definition is different is (alpha, n sigma, mu)

import glob
files=glob.glob("Rootfiles/"+args.input+"*.root")

names=[]


histos={}

x=R.RooRealVar('x','x',0,6000)

Rframe_all=x.frame(0,6000,6000)
ID=os.path.splitext(os.path.basename(args.input))[0]
out=R.TFile("Plots/"+args.input+".root","RECREATE")

histos['Mass']=R.TH1F('Mass','Mass',6000,0,6000)
for ip,file in enumerate(files):
	print(file)
	test=file.split("/")[1]
	print(test)
	name=((test.split(".")[0]).split("pwgevents_")[1]).split("_LQ")[0]
	print (name)
	names.append(name)
	print(name)	
	f=R.TFile(file)
	tree=f.Get("genAnalyzer/tree")
	Y=name.split('Lambda')[1]
	print(Y)
	Y=Y.replace("p",".")
	print(Y)
	cross=tree.AsMatrix(['XSection'])
	errcross=tree.AsMatrix(['XSectErr'])

	cross_real= (cross>1e-10)
	print(cross[cross_real])	
	for hh in ['Quark','Lep','LQ']:
		
		histos['graph_%s_%s_M'%(name,hh)]=R.TGraphErrors()
        	histos['graph_%s_%s_M'%(name,hh)].SetName('graph_%s_%s_M'%(name,hh))
        	histos['graph_%s_%s_M'%(name,hh)].SetMarkerStyle(20+ip%5)
        	histos['graph_%s_%s_M'%(name,hh)].SetMarkerSize(0.8)
		if 'LQ' in hh:
			histos['%s_%s_pz'%(name,hh)]=R.TH1F('%s_%s_pz'%(name,hh),'%s_%s_pz'%(name,hh),6000,-6000,6000)
			#nbin=int(3000*(1/float(Y)))
			nbin=6000
			histos['%s_%s_M'%(name,hh)]=R.TH1F('%s_%s_M'%(name,hh),'%s_%s_M'%(name,hh),nbin, 0,6000)
			histos['%s_%s_E'%(name,hh)]=R.TH1F('%s_%s_E'%(name,hh),'%s_%s_E'%(name,hh),1000, 0,6000)
		else:
			histos['Final%s_%s_pt'%(name,hh)]=R.TH1F('Final%s_%s_pt'%(name,hh),'Final%s_%s_pt'%(name,hh),1000,-10,6000)
			histos['Final%s_%s_phi'%(name,hh)]=R.TH1F('Final%s_%s_phi'%(name,hh),'Final%s_%s_phi'%(name,hh),50,-5,5)
			histos['Final%s_%s_eta'%(name,hh)]=R.TH1F('Final%s_%s_eta'%(name,hh),'Final%s_%s_eta'%(name,hh),50,-5,5)
			histos['Final%s_%s_Et'%(name,hh)]=R.TH1F('Final%s_%s_Et'%(name,hh),'Final%s_%s_Et'%(name,hh),1000,-10,2000)
			histos['Final%s_%s_M'%(name,hh)]=R.TH1F('Final%s_%s_M'%(name,hh),'Final%s_%s_M'%(name,hh),100,0,10)


	for hh in ['LQ']:
		for tt in ['M','E','pz']:
			tree.Project('%s_%s_%s'%(name,hh,tt),'%s_%s'%(hh,tt))
			if 'M' in tt:
				peak_ori=histos['%s_%s_%s'%(name,hh,tt)].GetBinCenter(histos['%s_%s_%s'%(name,hh,tt)].GetMaximumBin())
				print(ip,peak_ori,cross[cross_real])
				histos['graph_%s_%s_%s'%(name,hh,tt)].SetPoint(0,peak_ori,cross[cross_real])
				histos['graph_%s_LQ_M'%(name)].GetHistogram().SetBins(6,0,6000)
				#histos['graph_%s_%s_%s'%(name,hh,tt)].SetPointError(ip,0,0)
				peak=R.RooRealVar('peak','peak',peak_ori,0.95*peak_ori,1.05*peak_ori)
				sigma=R.RooRealVar('sigma','sigma', 20,0.,100.)
				x=R.RooRealVar('x','x',0.9*peak_ori,1.2*peak_ori)
		#		y=R.RooRealVar('y','y',0,10000)
				Rpdf=R.RooBreitWigner('BT','BT', x, peak, sigma)
			#Rpdf=R.RooGaussian('gauss','gauss',x,peak,sigma)
			#Rpdf=R.RooCBShape('crystalball','crystalball',x,peak,sigma,alpha,n)
			#Rpdf2=R.RooCBShape('crystalball2','crystalball2',x,peak,sigma2,alpha2,n2)
			#SPS_pdf=R.RooAddPdf("SPS_pdf", "SPS_pdf", R.RooArgList(Rpdf, Rpdf2), R.RooArgList(fraction), R.kTRUE);
			#Rpdf=R.RooBukinPdf('bukin','bukin',x,peak,sigma,xprox,rho1,rho2)
				Rfit_hist=R.RooDataHist("Rfit_hist", "Rfit_hist", R.RooArgList(x), R.RooFit.Import(histos['%s_%s_%s'%(name,hh,tt)]))	
				Rpdf.fitTo(Rfit_hist)
				Rframe=x.frame()
				Rfit_hist.plotOn(Rframe)
				Rpdf.plotOn(Rframe)
				#Rframe_all.addTH1(histos['%s_%s_%s'%(name,hh,tt)])
				#Rfit_hist.plotOn(Rframe_all)
				#Rpdf.plotOn(Rframe_all)
				Rframe.GetYaxis().SetTitle("Events")
				Rframe.GetXaxis().SetTitle(tt)
				Rframe.SetTitle("Mass distribution")
				Rframe.Draw()
				text=R.TLatex()
    				text.SetTextSize(0.03)	
				text.DrawLatexNDC(0.485,0.365,"Gamma/M= %f" %(float(sigma.getVal())/float(peak.getVal())))
				text.DrawLatexNDC(0.485,0.33, "#lambda^2/16pi = %f" %(float(Y)*float(Y)/(16*math.pi)))		
				out.cd()
				histos['%s_%s_%s'%(name,hh,tt)].Write()	
			#Mass_fit=R.TF1("CrystalBall","[4]*ROOT::Math::crystalball_function(x, [0], [1], [2], [3])",500,6000)
			#Mass_fit=R.TF1("gauss","[0]*TMath::Gaus(x,[1],[2])")
			#norm=float(histos['%s_%s_%s'%(name,hh,tt)].GetEntries())/histos['%s_%s_%s'%(name,hh,tt)].GetNbinsX()	
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
		        #histos['%s_%s_%s'%(name,hh,tt)].Draw()
                        #histos['%s_%s_%s'%(name,hh,tt)].GetXaxis().SetTitle(tt)
			#histos['%s_%s_%s'%(name,hh,tt)].Fit("gauss","LR+","",2800,3200) 
			#	histos['Mass'].Add(histos['%s_%s_%s'%(name,hh,tt)])
	
			else:	
				histos['%s_%s_%s'%(name,hh,tt)].Draw()
                		histos['%s_%s_%s'%(name,hh,tt)].GetXaxis().SetTitle(tt)
                	for ext in ['png','pdf']:
                	        c.SaveAs('Plots/%s_%s_%s.%s'%(name,hh,tt,ext))

	for hh in ['Quark','Lep']:
		for tt in ['pt','eta','phi','Et','M']:
			tree.Project('Final%s_%s_%s'%(name,hh,tt),'Final%s_%s'%(hh,tt))
			histos['Final%s_%s_%s'%(name,hh,tt)].Draw()
			histos['Final%s_%s_%s'%(name,hh,tt)].GetXaxis().SetTitle(tt)
			for ext in ['png','pdf']:
				c.SaveAs('Plots/%s_%s_%s.%s'%(name,hh,tt,ext))



#name='M3000_Lambda0p3'

for ip,i in enumerate(names):
	print(ip,name,i)
	if ip == 0:
		c.SetLogy()
		histos['graph_%s_LQ_M'%(i)].GetHistogram().SetAxisRange(1e-7, 3e-1,"Y")		
		histos['graph_%s_LQ_M'%(i)].GetXaxis().SetRangeUser(990, 5500)
		histos['graph_%s_LQ_M'%(i)].GetXaxis().SetRange(990, 5500)
		histos['graph_%s_LQ_M'%(i)].Draw("APE")
	else:	
		histos['graph_%s_LQ_M'%(i)].Draw("PESAME")
		histos['graph_%s_LQ_M'%(i)].GetXaxis().SetRangeUser(990, 5500)
		histos['graph_%s_LQ_M'%(i)].GetXaxis().SetRange(990, 5500)

#print("hello")
#Rframe_all.Draw()
#print("pd")
for ext in ['png','pdf']:
		c.SaveAs("Plots/test.%s"%ext)


