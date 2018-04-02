#########################################################################################################
#########################################################################################################
## Greig Cowan
## 31st August 2015
#########################################################################################################
#########################################################################################################

import GaudiKernel.SystemOfUnits as Units
from Gaudi.Configuration import *
from PhysSelPython.Wrappers import AutomaticData, Selection, SelectionSequence
from Configurables import FilterDesktop
from Configurables import DaVinci
from Configurables import DecayTreeTuple
from Configurables import TupleToolDecay
from Configurables import GaudiSequencer,Pi0Veto__Tagger
from Configurables import CombineParticles,DaVinci__N4BodyDecays
from Configurables import CondDB
from Configurables import LoKi__Hybrid__TupleTool
from Configurables import LoKi__Hybrid__TupleTool
from Configurables import LoKi__Hybrid__EvtTupleTool
from Configurables import MCTupleToolHierarchy
from Configurables import TupleToolMCTruth
from Configurables import TupleToolMCBackgroundInfo
from Configurables import TupleToolTISTOS, TriggerTisTos

EVTMAX = -1
MODE = 'data'
OUTPUTLEVEL = ERROR

#########################################################################################################
# Build the candidates, with selections following the WG productions
#########################################################################################################


############
InputJpsi= AutomaticData(Location = '/Event/Dimuon/Phys/FullDSTDiMuonJpsi2MuMuDetachedLine/Particles')

FilteredJpsi= FilterDesktop("FilteredJpsi")
FilteredJpsi.Code = "(INTREE((ABSID=='mu+')&(PT>550*MeV)&(TRCHI2DOF<4)&(PIDmu>0)))"

SelJpsi = Selection("Selpsi", Algorithm =FilteredJpsi, RequiredSelections = [InputJpsi] )

############
SelPhotons = AutomaticData(Location = 'Phys/StdLooseAllPhotons/Particles')

MakeChic2JpsiGamma = CombineParticles("MakeChic2JpsiGamma") 
MakeChic2JpsiGamma.DecayDescriptors = ['chi_c1(1P) -> J/psi(1S) gamma'] 
MakeChic2JpsiGamma.CombinationCut = "( AM - AM1 ) < 700 * MeV"
MakeChic2JpsiGamma.MotherCut = "MM<10000.*MeV"
MakeChic2JpsiGamma.DaughtersCuts= {
        "J/psi(1S)" : "M  < ( 3.100 + 0.120 ) * GeV",
        'gamma'     : "PT > 400 * MeV "
        }
SelChic = Selection(
        "SelChic",
        Algorithm = MakeChic2JpsiGamma,
        RequiredSelections = [SelJpsi,SelPhotons]
        )

############
SelKaons = AutomaticData(Location = 'Phys/StdAllLooseKaons/Particles')
MakeBp2Chic3K = DaVinci__N4BodyDecays("MakeBp2Chic3K")
MakeBp2Chic3K.DecayDescriptor = "[B+ -> chi_c1(1P) K+ K+ K-]cc"
MakeBp2Chic3K.Combination12Cut  = "( AM < 6 * GeV  ) & ( ACHI2DOCA(1,2) < 20 )"
MakeBp2Chic3K.Combination123Cut = "( AM < 6 * GeV  ) & ( ACHI2DOCA(1,3) < 20 ) & ( ACHI2DOCA(2,3) < 20 )"
MakeBp2Chic3K.CombinationCut = "in_range ( 4.75 * GeV , AM , 5.85 * GeV ) &( ACHI2DOCA(1,4) < 20 ) & (ACHI2DOCA(2,4) < 20 ) & (ACHI2DOCA(3,4) < 20 ) "
MakeBp2Chic3K.MotherCut = "(VFASPF(VCHI2PDOF)<10) & (BPVLTIME()>0.333333*ps)"
MakeBp2Chic3K.DaughtersCuts={
        "K+":" (PT> 200 * MeV ) & ( CLONEDIST> 5000) & (TRGHOSTPROB < 0.5) & (TRCHI2DOF< 4) & in_range (2, ETA,5) & in_range (3.2*GeV, P,150 * GeV ) & HASRICH & (PROBNNk> 0.1) & (MIPCHI2DV()>4)"
            }


SelBp= Selection(
        "SelBp",
        Algorithm = MakeBp2Chic3K,
        RequiredSelections = [SelChic, SelKaons]
        )
BpVetoPi0 = Pi0Veto__Tagger(
        "BpVetoPi0",
        MassWindow     = 25,
        MassChi2       = -1 ,
        ExtraInfoIndex = 25013 ## unique ! 
        )
SelMyBp= Selection(
        "SelMyBp",
        Algorithm = BpVetoPi0,
        RequiredSelections = [SelBp]
        )



#rootInTES = '/Event/PSIX'
#location='Phys/SelPsiPKForPsiX/Particles'

#########################################################################################################
# Now set up the DecayTreeTuples for the reconstructed particles
#########################################################################################################


tupletools = []
tupletools.append("TupleToolKinematic")
tupletools.append("TupleToolGeometry")
tupletools.append("TupleToolTrackInfo")
tupletools.append("TupleToolPid")
tupletools.append("TupleToolRecoStats")
tupletools.append("TupleToolEventInfo")
triglist = [
	 "L0PhysicsDecision"
	,"L0MuonDecision"
	,"L0DiMuonDecision"
	,"L0MuonHighDecision"
	,"L0HadronDecision"
	,"L0ElectronDecision"
	,"L0PhotonDecision"
	,"Hlt1DiMuonHighMassDecision"
	,"Hlt1DiMuonLowMassDecision"
	,"Hlt1SingleMuonNoIPDecision"
	,"Hlt1SingleMuonHighPTDecision"
	,"Hlt1TrackAllL0Decision"
	,"Hlt1TrackMuonDecision"
	,"Hlt1TrackPhotonDecision"
	,"Hlt1L0AnyDecision"
	,"Hlt2Topo2BodySimpleDecision"
	,"Hlt2Topo3BodySimpleDecision"
	,"Hlt2Topo4BodySimpleDecision"
	,"Hlt2Topo2BodyBBDTDecision"
	,"Hlt2Topo3BodyBBDTDecision"
	,"Hlt2Topo4BodyBBDTDecision"
	,"Hlt2TopoMu2BodyBBDTDecision"
	,"Hlt2TopoMu3BodyBBDTDecision"
	,"Hlt2TopoMu4BodyBBDTDecision"
	,"Hlt2TopoE2BodyBBDTDecision"
	,"Hlt2TopoE3BodyBBDTDecision"
	,"Hlt2TopoE4BodyBBDTDecision"
	,"Hlt2MuonFromHLT1Decision"
	,"Hlt2DiMuonDecision"
    ,"Hlt2DiMuonDetachedDecision"
    ,"Hlt2DiMuonDetachedJPsiDecision"
    ,"Hlt2DiMuonDetachedHeavyDecision"
    ,"Hlt2DiMuonLowMassDecision"
	,"Hlt2DiMuonJPsiDecision"
	,"Hlt2DiMuonJPsiHighPTDecision"
	,"Hlt2DiMuonPsi2SDecision"
	,"Hlt2DiMuonBDecision"
]
TISTOSTool = TupleToolTISTOS('TISTOSTool')
TISTOSTool.VerboseL0   = True
TISTOSTool.VerboseHlt1 = True
TISTOSTool.VerboseHlt2 = True
TISTOSTool.TriggerList = triglist[:]
TISTOSTool.addTool( TriggerTisTos, name="TriggerTisTos")

LoKi_B = LoKi__Hybrid__TupleTool("LoKi_B")
LoKi_B.Variables =  {
        "ETA" : "ETA",
        "PHI" : "PHI",
        "FDCHI2"          : "BPVVDCHI2",
        "FDS"             : "BPVDLS",
        "DIRA"            : "BPVDIRA",
        "pi0veto"         : "CHILDFUN ( PINFO( 25013 , -1 ) , 'gamma' == ABSID ) "
    }

LoKi_Mu = LoKi__Hybrid__TupleTool("LoKi_Mu")
LoKi_Mu.Variables =  {
    "NSHAREDMU" : "NSHAREDMU"
    }

from PhysConf.Selections import TupleSelection 
Bp_tuple = TupleSelection (
    'TUPLE',
    [ SelMyBp], 
    Decay = '[B+ -> ^(chi_c1(1P) -> ^(J/psi(1S) -> ^mu+ ^mu-) ^gamma) ^K+ ^K+ ^K-]CC',
    Branches = { 
          "Bp" : "[B+ ->  (chi_c1(1P) ->  (J/psi(1S) ->  mu+  mu-)  gamma)  K+ K+  K-]CC",
          "chi_c"     : "[B+ -> ^(chi_c1(1P) ->  (J/psi(1S) ->  mu+  mu-)  gamma)  K+ K+  K-]CC",
          "Jpsi"      : "[B+ ->  (chi_c1(1P) -> ^(J/psi(1S) ->  mu+  mu-)  gamma)  K+ K+  K-]CC",
          "gamma"     : "[B+ ->  (chi_c1(1P) ->  (J/psi(1S) ->  mu+  mu-) ^gamma)  K+ K+  K-]CC",
          "muplus"    : "[B+ ->  (chi_c1(1P) ->  (J/psi(1S) -> ^mu+  mu-)  gamma)  K+ K+  K-]CC",
          "muminus"   : "[B+ ->  (chi_c1(1P) ->  (J/psi(1S) ->  mu+ ^mu-)  gamma)  K+ K+  K-]CC",
          "kaonp1"    : "[B+ ->  (chi_c1(1P) ->  (J/psi(1S) ->  mu+  mu-)  gamma) ^K+ K+  K-]CC",
          "kaonp2"    : "[B+ ->  (chi_c1(1P) ->  (J/psi(1S) ->  mu+  mu-)  gamma)  K+ ^K+ K-]CC",
          "kaonm"     : "[B+ ->  (chi_c1(1P) ->  (J/psi(1S) ->  mu+  mu-)  gamma)  K+ K+ ^K-]CC",
          } 
)

mytuple = Bp_tuple.algorithm()
mytuple.ToolList = tupletools[:]
for particle in ["Bp", "chi_c", "gamma", "Jpsi", "muplus", "muminus", "kaonp1", "kaonp2", "kaonm"]:
    mytuple.addTool(TupleToolDecay, name = particle)

# List of the reconstructed tuples
tuples = [ mytuple
        ]

for tup in tuples:
    tup.ReFitPVs = True
    if MODE == "MC":
        tup.addTool(TupleToolMCTruth, name = "TruthTool")
        tup.addTool(TupleToolMCBackgroundInfo, name = "BackgroundInfo")
        tup.ToolList += ["TupleToolMCTruth/TruthTool"]
        tup.ToolList += ["TupleToolMCBackgroundInfo/BackgroundInfo"]

    tup.Bp.addTool( LoKi_B )
    tup.Bp.ToolList += ["LoKi::Hybrid::TupleTool/LoKi_B"]
    tup.muplus.addTool( LoKi_Mu )
    tup.muplus.ToolList += ["LoKi::Hybrid::TupleTool/LoKi_Mu"]
    tup.muminus.addTool( LoKi_Mu )
    tup.muminus.ToolList += ["LoKi::Hybrid::TupleTool/LoKi_Mu"]
    tup.gamma.ToolList += ["TupleToolPhotonInfo/PhotonInfo", "TupleToolPi0Info/Pi0Info"]
    for particle in [ tup.Bp ]:
        particle.addTool(TISTOSTool, name = "TISTOSTool")
        particle.ToolList += [ "TupleToolTISTOS/TISTOSTool" ]

    # Fit with chic1 mass constraint and PV constr
    chic1Const = tup.Bp.addTupleTool('TupleToolDecayTreeFitter/ConstChic1Fit')
    chic1Const.UpdateDaughters = True
    chic1Const.constrainToOriginVertex = True
    chic1Const.daughtersToConstrain += [ 'J/psi(1S)', 'chi_c1(1P)' ]
    # Fit with Bp and chic1 mass constraints and PV constr
    chic1BpConst = tup.Bp.addTupleTool('TupleToolDecayTreeFitter/ConstBpConstChic1Fit')
    chic1BpConst.UpdateDaughters = True
    chic1BpConst.constrainToOriginVertex = True
    chic1BpConst.daughtersToConstrain += [ 'B+', 'J/psi(1S)', 'chi_c1(1P)' ]
    # Fit with chic2 mass constraint and PV constr
    chic2Const = tup.Bp.addTupleTool('TupleToolDecayTreeFitter/ConstChic2Fit')
    chic2Const.UpdateDaughters = True
    chic2Const.constrainToOriginVertex = True
    chic2Const.Substitutions = { 'Beauty -> ^chi_c1(1P) Meson Meson Meson': 'chi_c2(1P)' }
    chic2Const.daughtersToConstrain += [ 'J/psi(1S)', 'chi_c2(1P)' ]
    # Fit with chic2 and Bp mass constraints and PV constr
    chic2BpConst = tup.Bp.addTupleTool('TupleToolDecayTreeFitter/ConstBpConstChic2Fit')
    chic2BpConst.UpdateDaughters = True
    chic2BpConst.constrainToOriginVertex = True
    chic2BpConst.Substitutions = { 'Beauty -> ^chi_c1(1P) Meson Meson Meson': 'chi_c2(1P)' }
    chic2BpConst.daughtersToConstrain += [ 'B+', 'J/psi(1S)', 'chi_c2(1P)' ]
    # Fit with chic1 mass constraint and PV constr
    chic1ConstNoPV = tup.Bp.addTupleTool('TupleToolDecayTreeFitter/ConstChic1FitNoPV')
    chic1ConstNoPV.UpdateDaughters = True
    chic1ConstNoPV.daughtersToConstrain += [ 'J/psi(1S)', 'chi_c1(1P)' ]
    # Fit with Bp and chic1 mass constraints and no PV constr
    chic1BpConstNoPV = tup.Bp.addTupleTool('TupleToolDecayTreeFitter/ConstBpConstChic1FitNoPV')
    chic1BpConstNoPV.UpdateDaughters = True
    chic1BpConstNoPV.daughtersToConstrain += [ 'B+', 'J/psi(1S)', 'chi_c1(1P)' ]
    # Fit with chic2 mass constraint and PV constr
    chic2ConstNoPV = tup.Bp.addTupleTool('TupleToolDecayTreeFitter/ConstChic2FitNoPV')
    chic2ConstNoPV.UpdateDaughters = True
    chic2ConstNoPV.Substitutions = { 'Beauty -> ^chi_c1(1P) Meson Meson Meson': 'chi_c2(1P)' }
    chic2ConstNoPV.daughtersToConstrain += [ 'J/psi(1S)', 'chi_c2(1P)' ]
    # Fit with chic2 and Bp mass constraints and no PV constr
    chic2BpConstNoPV = tup.Bp.addTupleTool('TupleToolDecayTreeFitter/ConstBpConstChic2FitNoPV')
    chic2BpConstNoPV.UpdateDaughters = True
    chic2BpConstNoPV.Substitutions = { 'Beauty -> ^chi_c1(1P) Meson Meson Meson': 'chi_c2(1P)' }
    chic2BpConstNoPV.daughtersToConstrain += [ 'B+', 'J/psi(1S)', 'chi_c2(1P)' ]

seq = SelectionSequence('SEQ', Bp_tuple )

##################################################################
# If we want to write a DST do this
##################################################################
from DSTWriters.microdstelements import *
from DSTWriters.Configuration import (SelDSTWriter,
        stripDSTStreamConf,
        stripDSTElements
        )
SelDSTWriterElements = {
        'default'              : stripDSTElements()
        }
SelDSTWriterConf = {
        'default'              : stripDSTStreamConf()
        }
if MODE == 'MC':
    dstWriter = SelDSTWriter( "MyDSTWriter",
            StreamConf = SelDSTWriterConf,
            MicroDSTElements = SelDSTWriterElements,
            OutputFileSuffix ='MC',
            SelectionSequences = sc.activeStreams()
            )

###################### DAVINCI SETTINGS ############################################
DaVinci().SkipEvents = 0  #1945
DaVinci().PrintFreq = 1000
DaVinci().EvtMax = EVTMAX
DaVinci().TupleFile = "Tuple.root"
DaVinci().HistogramFile = 'DVHistos.root'
DaVinci().InputType = "DST"
DaVinci().Simulation = False
DaVinci().Lumi = True
DaVinci().DataType = "2011"
CondDB( LatestGlobalTagByDataType = '2011' )

if False: # Add the DST writing algorithms
    DaVinci().appendToMainSequence( [ dstWriter.sequence(), printTree ] )

if True: # Add the ntuple writing algorithms
    DaVinci().UserAlgorithms = [seq.sequence() ]
if MODE == 'MC':
    DaVinci().Simulation = True
    DaVinci().Lumi = False
    DaVinci().UserAlgorithms += [
        mcmytuple
        ]

if OUTPUTLEVEL == DEBUG:
    DaVinci().MoniSequence += [ mctree ]

from Configurables import DaVinciInit
#DaVinciInit().OutputLevel = OUTPUTLEVEL

if MODE != "MC":
    from Configurables import LumiIntegrateFSR, LumiIntegratorConf
    LumiIntegrateFSR('IntegrateBeamCrossing').SubtractBXTypes = ['None']

MessageSvc().Format = "% F%60W%S%7W%R%T %0W%M"


#DaVinci().Input = [ '/eos/lhcb/grid/prod/lhcb/LHCb/Collision11/DIMUON.DST/00041840/0004/00041840_00048189_1.dimuon.dst' ]

###################################################################################
####################### THE END ###################################################
###################################################################################
