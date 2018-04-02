from ROOT import *
import sys

index=0
if len(sys.argv)>1:
    index = int(sys.argv[-1])

dt = [ "MC2011.root" ,"MC2012.root" ,"MU2011.root" ,"MD2011.root" ,"MU2012.root" ,"MD2012.root"][index]

test=0
if  test: dt = "raw/2988_88.root"

fr = TFile(dt)
oldtr = fr.Get("TUPLE/DecayTree")


fo=TFile(dt.replace(".root","Update.root"),"recreate")

oldtr.SetBranchStatus("*",0)
oldtr.SetBranchStatus("*_M",1)
oldtr.SetBranchStatus("*_PT",1)
oldtr.SetBranchStatus("*_PZ",1)
oldtr.SetBranchStatus("*_P",1)
oldtr.SetBranchStatus("*PE",1)
oldtr.SetBranchStatus("*_IPCHI2_OWNPV",1)
oldtr.SetBranchStatus("Bp_Const*PE",0)
oldtr.SetBranchStatus("Bp_Const*PZ",0)

oldtr.SetBranchStatus("kaon*_ProbNNk",1)
oldtr.SetBranchStatus("kaon*_ProbNNpi",1)
oldtr.SetBranchStatus("kaon*_PT",1)
oldtr.SetBranchStatus("Bp_ConstChic1Fit_nPV",1)
oldtr.SetBranchStatus("Bp_ConstChic1Fit_M",1)
oldtr.SetBranchStatus("Bp_ConstChic1Fit_chi2",1)
oldtr.SetBranchStatus("Bp_ConstChic1Fit_nDOF",1)
oldtr.SetBranchStatus("Bp_ConstChic2Fit_nPV",1)
oldtr.SetBranchStatus("Bp_ConstChic2Fit_M",1)
oldtr.SetBranchStatus("Bp_ConstChic2Fit_chi2",1)
oldtr.SetBranchStatus("Bp_ConstChic2Fit_nDOF",1)
oldtr.SetBranchStatus("Bp_ENDVERTEX_CHI2",1)
oldtr.SetBranchStatus("Bp_ENDVERTEX_NDOF",1)
oldtr.SetBranchStatus("Bp_FDCHI2_OWNPV",1)
oldtr.SetBranchStatus("Bp_pi0veto",1)
oldtr.SetBranchStatus("gamma_*",1)

#for MC, add truth info
if "MC" in dt:
    oldtr.SetBranchStatus("*MC*",1)
    oldtr.SetBranchStatus("*BKGCAT",1)
    oldtr.SetBranchStatus("*TRUE*",1)

newtr=oldtr.CloneTree(0)


from array import array

#add new branches
minPT=array("d",[0.])
minIPCHI2=array("d",[0.])
minPID=array("d",[0.])
bkg=array("d",[0.])
newtr.Branch("minPT",minPT,"minPT/D")
newtr.Branch("minIPCHI2",minIPCHI2,"minIPCHI2/D")
newtr.Branch("minPID",minPID,"minPID/D")



totEntry = oldtr.GetEntries()
for ii in range(totEntry):
    oldtr.GetEntry(ii)
    minIPCHI2[0] = min(min(oldtr.kaonp1_IPCHI2_OWNPV,oldtr.kaonp2_IPCHI2_OWNPV),oldtr.kaonm_IPCHI2_OWNPV)
    minPT[0]     = min(min(oldtr.kaonp1_PT,oldtr.kaonp2_PT),oldtr.kaonm_PT)
    minPID[0]    = min(min(oldtr.kaonp1_ProbNNk,oldtr.kaonp2_ProbNNk),oldtr.kaonm_ProbNNk)
    if "MC" in dt:  #only for B+ -> chi_c pi pi K MC, not for signal MC
        minPID[0]    = min(min(oldtr.kaonp1_ProbNNk,2.),2.)
    newtr.Fill()
newtr.Write()
newtr.Show(0)



