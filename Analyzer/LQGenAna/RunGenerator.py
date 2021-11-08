#!usr/bin/python
import os
import argparse 
import sys 
import subprocess
import datetime 
import re
from subprocess import check_output
import ROOT
import numpy as nn
from random import randint

basedir_path = os.path.dirname(os.path.realpath(__file__))
print basedir_path

usage = ""
parser = argparse.ArgumentParser(usage='\nExample: python %prog -c config_LQGenAna.py -i list.txt -t /tmp/santanas/ --outputDir `pwd`/TestOutput')
parser.add_argument("-c","--pythonConfig",action="store",type=str,dest="PYTHONCONFIG",default="")
parser.add_argument("-i","--inputGENList",action="store",type=str,dest="INPUTGENLIST",default="")
parser.add_argument("-t","--tmpDir",action="store",type=str,dest="TMPDIR",default="")
parser.add_argument("--numberOfevents",action="store",type=str,dest="NEVENTS",default="-1")
parser.add_argument("--outputDir",action="store",type=str,dest="OUTPUTDIR",default="")
parser.add_argument("--lhe",dest="lhe",action="store_true")

parser.set_defaults(lhe=False)


args = parser.parse_args()
PYTHONCONFIG = args.PYTHONCONFIG
INPUTGENLIST = args.INPUTGENLIST
TMPDIR = args.TMPDIR
NEVENTS = args.NEVENTS
OUTPUTDIR = args.OUTPUTDIR


if not args.PYTHONCONFIG:   
    parser.error('ERROR: Input python config is not given')
if not args.INPUTGENLIST:   
    parser.error('ERROR: Input GEN list is not given')
if not args.TMPDIR:   
    parser.error('ERROR: Tmp directory is not given')
if not args.OUTPUTDIR:   
    parser.error('ERROR: Output directory is not given')

#get list of lhe files
proc = subprocess.Popen(["less %s" % INPUTGENLIST], stdout=subprocess.PIPE, shell=True)
(genfilelist, err) = proc.communicate()
genfilelist = genfilelist.splitlines()
print genfilelist

#create output dir
IsEosDir = False
if ("/eos/" in OUTPUTDIR):
    print "IS EOS DIR"
    IsEosDir = True
else:
    print "IS NOT EOS DIR"
    IsEosDir = False

if IsEosDir:
    print("eos mkdir -p %s" % (OUTPUTDIR) )
    os.system("eos mkdir -p %s" % (OUTPUTDIR) )
else:
    print("mkdir -p %s" % (OUTPUTDIR) )
    os.system("mkdir -p %s" % (OUTPUTDIR) )


# loop over gripacks
for genfile in genfilelist:

#genfile=(INPUTGENLIST.split(".")[0])
	if args.lhe:
		outputfilename ="lhe_"+((genfile.split("/")[-1]).split("."))[0]+".root"
		anal_output= ((outputfilename).split(".")[0]).split("lhe_")[1]+"_LQ_LHE.root"
	else:
		outputfilename=((genfile.split("/")[-1]).split("."))[0]+"_LQ_LHE.root"
    #print outputfilename

	print("cmsRun %s files=file:%s output=%s/%s maxEvents=%s" % (PYTHONCONFIG,genfile,TMPDIR,outputfilename,NEVENTS) )
	os.system("cmsRun %s files=file:%s output=%s/%s maxEvents=%s" % (PYTHONCONFIG,genfile,TMPDIR,outputfilename,NEVENTS) )

#move output in final directory

	if IsEosDir:
		TMPFILE = ("%s/%s" % (TMPDIR,outputfilename))
		TMPFILE = re.sub("//","/",TMPFILE) 
		OUTPUTFILE = ("%s/%s" % (OUTPUTDIR,outputfilename))
		OUTPUTFILE = re.sub("//","/",OUTPUTFILE) 

		print("eos cp %s %s" % (TMPFILE,OUTPUTFILE))
		os.system("eos cp %s %s" % (TMPFILE,OUTPUTFILE))
		print("rm -f %s" % (TMPFILE))
		os.system("rm -f %s" % (TMPFILE))
	else:
		print("mv %s/%s %s/%s" % (TMPDIR,outputfilename,OUTPUTDIR,outputfilename))
		os.system("mv %s/%s %s/%s" % (TMPDIR,outputfilename,OUTPUTDIR,outputfilename))


	if args.lhe:
		print("cmsRun  python/config_LQGenAna.py files=file:%s output=%s/%s maxEvents=%s" %  (outputfilename,TMPDIR,anal_output,NEVENTS))
        	os.system("cmsRun python/config_LQGenAna.py files=file:%s/%s output=%s/%s maxEvents=%s" % (OUTPUTDIR,outputfilename,TMPDIR,anal_output,NEVENTS))

		if IsEosDir:
			TMPFILE = ("%s/%s" % (TMPDIR,anal_output))
			TMPFILE = re.sub("//","/",TMPFILE) 
			OUTPUTFILE = ("%s/%s" % (OUTPUTDIR,anal_output))
			OUTPUTFILE = re.sub("//","/",OUTPUTFILE) 

			print("eos cp %s %s" % (TMPFILE,OUTPUTFILE))
			os.system("eos cp %s %s" % (TMPFILE,OUTPUTFILE))
			print("rm -f %s" % (TMPFILE))
			os.system("rm -f %s" % (TMPFILE))
		else:
			print("mv %s/%s %s/%s" % (TMPDIR,anal_output,OUTPUTDIR,anal_output))
			os.system("mv %s/%s %s/%s" % (TMPDIR,anal_output,OUTPUTDIR,anal_output))
