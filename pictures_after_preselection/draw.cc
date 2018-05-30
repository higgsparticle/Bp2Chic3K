void func ( TTree* MCTree, TTree* DTTree, TString num, TString expression, Double_t Low_edge, Double_t High_edge );
void PreSelection ( TTree* MCTree, TTree* DTTree, TString expression, Long64_t SigTotal, Long64_t DTTotal);
void draw(){
   TChain* MCChain = new TChain("TUPLE/DecayTree");
   TChain* DTChain = new TChain("TUPLE/DecayTree");

   MCChain->Add("/home/wangzh/workdir/B2chicPhiK/tuples/MC2011.root"); 
   MCChain->Add("/home/wangzh/workdir/B2chicPhiK/tuples/MC2012.root"); 
   DTChain->Add("/home/wangzh/workdir/B2chicPhiK/tuples/MU2011.root"); 
   DTChain->Add("/home/wangzh/workdir/B2chicPhiK/tuples/MU2012.root"); 
   DTChain->Add("/home/wangzh/workdir/B2chicPhiK/tuples/MD2011.root"); 
   DTChain->Add("/home/wangzh/workdir/B2chicPhiK/tuples/MD2012.root");

   TCut TruthMatch("(abs(Bp_TRUEID)==521) && ((abs(chi_c_TRUEID)==20443)||(abs(chi_c_TRUEID)==100445)) && (abs(Jpsi_TRUEID)==443) && (abs(muplus_TRUEID)==13) && (abs(muminus_TRUEID)==13) && (gamma_TRUEID==22) && (abs(kaonp1_TRUEID)==321) && (abs(kaonp2_TRUEID)==211) && (abs(kaonm_TRUEID)==211) && (abs(chi_c_MC_MOTHER_ID)==521) && ((abs(Jpsi_MC_MOTHER_ID)==20443) ||(abs(Jpsi_MC_MOTHER_ID)==100445)) && (abs(muplus_MC_MOTHER_ID)==443) && (abs(muminus_MC_MOTHER_ID)==443) && ((gamma_MC_MOTHER_ID==20443)||(gamma_MC_MOTHER_ID==100445)) && (kaonp1_MC_MOTHER_ID==521) && (kaonp2_MC_MOTHER_ID==521) && (kaonm_MC_MOTHER_ID==521) && (abs(Jpsi_MC_GD_MOTHER_ID)==521) && ((abs(muplus_MC_GD_MOTHER_ID)==20443)||(abs(muplus_MC_GD_MOTHER_ID)==100445)) && ((abs(muminus_MC_GD_MOTHER_ID)==20443)||(abs(muminus_MC_GD_MOTHER_ID)==100445)) && (gamma_MC_GD_MOTHER_ID==521) && (abs(muplus_MC_GD_GD_MOTHER_ID)==521) && (abs(muminus_MC_GD_GD_MOTHER_ID)==521)");
   //TCut Cut1 ("Bp_DIRA>0.9998 && Bp_ENDVERTEX_CHI2<31 && TMath::Min(muplus_ProbNNmu, muminus_ProbNNmu)>0.15 && Bp_IPCHI2_OWNPV<25");
   //TCut Cut2 ("TMath::Min(muplus_IPCHI2_OWNPV, muminus_IPCHI2_OWNPV)>7.5 && Bp_FDS>13 && kaonp1_ProbNNk>0.125");
   //TCut MassWindow ("Bp_M-chi_c_M+3510>5100 && Bp_M-chi_c_M+3510<5400");
   TCut Cut1 ("Bp_DIRA>0.9998 && TMath::Min(muplus_IPCHI2_OWNPV, muminus_IPCHI2_OWNPV)>7.5 && Bp_IPCHI2_OWNPV<25 && Bp_ENDVERTEX_CHI2<31");
   TCut Cut2 ("Bp_FDS>12.7 && kaonp1_ProbNNk>0.125 && TMath::Min(muplus_ProbNNmu, muminus_ProbNNmu)>0.15");

   TTree* MCTree = (TTree*) MCChain -> CopyTree(TruthMatch && Cut1 && Cut2);
   TTree* DTTree = (TTree*) DTChain -> CopyTree(Cut1 && Cut2);

   //Long64_t SigTotal = MCTree -> GetEntries();
   //Long64_t BKGTotal = DTTree -> GetEntries();
   //PreSelection (MCTree, DTTree, "Bp_ENDVERTEX_CHI2<31", SigTotal, BKGTotal);
   //PreSelection (MCTree, DTTree, "Bp_IPCHI2_OWNPV<25", SigTotal, BKGTotal);
   //PreSelection (MCTree, DTTree, "Bp_FDS>12.7", SigTotal, BKGTotal);
   //PreSelection (MCTree, DTTree, "Bp_DIRA>0.9998", SigTotal, BKGTotal);
   //PreSelection (MCTree, DTTree, "gamma_CL>0.005", SigTotal, BKGTotal);
   //PreSelection (MCTree, DTTree, "TMath::Min(muplus_IPCHI2_OWNPV, muminus_IPCHI2_OWNPV)>7.5", SigTotal, BKGTotal);
   //PreSelection (MCTree, DTTree, "TMath::Max(muplus_ProbNNghost, muminus_ProbNNghost)<0.26", SigTotal, BKGTotal);
   //PreSelection (MCTree, DTTree, "TMath::Min(muplus_ProbNNmu, muminus_ProbNNmu)>0.145", SigTotal, BKGTotal);
   //PreSelection (MCTree, DTTree, "TMath::Min(muplus_PT, muminus_PT)>585", SigTotal, BKGTotal);
   //PreSelection (MCTree, DTTree, "TMath::Min(kaonp1_P, TMath::Min(kaonp2_P, kaonm_P))>3500", SigTotal, BKGTotal);
   //PreSelection (MCTree, DTTree, "TMath::Min(kaonp1_PT, TMath::Min(kaonp2_PT, kaonm_PT))>220", SigTotal, BKGTotal);
   //PreSelection (MCTree, DTTree, "TMath::Max(kaonp1_TRACK_CHI2NDOF, TMath::Max(kaonp2_TRACK_CHI2NDOF, kaonm_TRACK_CHI2NDOF))<2.7", SigTotal, BKGTotal);
   //PreSelection (MCTree, DTTree, "TMath::Max(kaonp1_TRACK_GhostProb, TMath::Max(kaonp2_TRACK_GhostProb, kaonm_TRACK_GhostProb))<0.25", SigTotal, BKGTotal);
   //PreSelection (MCTree, DTTree, "kaonp1_ProbNNk>0.125", SigTotal, BKGTotal);

   TString DM = "Bp_M-chi_c_M+3510";

   func ( MCTree, DTTree, "00",(TString) DM, 5100, 5500 );
   func ( MCTree, DTTree, "01",(TString) "Bp_ENDVERTEX_CHI2", 0, 35 );
   func ( MCTree, DTTree, "02",(TString) "Bp_IPCHI2_OWNPV", 0, 30 );
   func ( MCTree, DTTree, "03",(TString) "Bp_FDS", 10, 250 );
   func ( MCTree, DTTree, "04",(TString) "Bp_DIRA", 0.9998, 1 );
   func ( MCTree, DTTree, "05",(TString) "gamma_CL", 0, 1 );
   func ( MCTree, DTTree, "06",(TString) "muplus_IPCHI2_OWNPV", 0, 1200 );
   func ( MCTree, DTTree, "07",(TString) "muminus_IPCHI2_OWNPV", 0, 1200 );
   func ( MCTree, DTTree, "08",(TString) "Jpsi_ENDVERTEX_CHI2", 0, 12 );
   func ( MCTree, DTTree, "09",(TString) "muplus_ProbNNghost", 0, 0.4 );
   func ( MCTree, DTTree, "10",(TString) "muminus_ProbNNghost", 0, 0.4 );
   func ( MCTree, DTTree, "11",(TString) "muplus_ProbNNmu", 0.1, 1 );
   func ( MCTree, DTTree, "12",(TString) "muminus_ProbNNmu", 0.1, 1 );
   func ( MCTree, DTTree, "13",(TString) "muplus_PT", 400, 12000 );
   func ( MCTree, DTTree, "14",(TString) "muminus_PT", 400, 12000 );
   func ( MCTree, DTTree, "15",(TString) "kaonp1_P", 0, 100000 );
   func ( MCTree, DTTree, "16",(TString) "kaonp2_P", 0, 100000 );
   func ( MCTree, DTTree, "17",(TString) "kaonm_P", 0, 100000 );
   func ( MCTree, DTTree, "18",(TString) "kaonp1_PT", 0, 6000 );
   func ( MCTree, DTTree, "19",(TString) "kaonp2_PT", 0, 6000 );
   func ( MCTree, DTTree, "20",(TString) "kaonm_PT", 0, 6000 );
   func ( MCTree, DTTree, "21",(TString) "kaonp1_IPCHI2_OWNPV", 0, 500 );
   func ( MCTree, DTTree, "22",(TString) "kaonp2_IPCHI2_OWNPV", 0, 500 );
   func ( MCTree, DTTree, "23",(TString) "kaonm_IPCHI2_OWNPV", 0, 500 );
   func ( MCTree, DTTree, "24",(TString) "kaonp1_TRACK_CHI2NDOF", 0, 3 );
   func ( MCTree, DTTree, "25",(TString) "kaonp2_TRACK_CHI2NDOF", 0, 3 );
   func ( MCTree, DTTree, "26",(TString) "kaonm_TRACK_CHI2NDOF", 0, 3 );
   func ( MCTree, DTTree, "27",(TString) "kaonp1_TRACK_GhostProb", 0, 0.3 );
   func ( MCTree, DTTree, "28",(TString) "kaonp2_TRACK_GhostProb", 0, 0.3 );
   func ( MCTree, DTTree, "29",(TString) "kaonm_TRACK_GhostProb", 0, 0.3 );
   func ( MCTree, DTTree, "30",(TString) "kaonp1_ProbNNk", 0.1, 1 );
}

void func( TTree* MCTree, TTree* DTTree, TString num, TString expression, Double_t Low_edge, Double_t High_edge ){

   TH1F* MCh = new TH1F("MCh", "Distribution of "+expression, 200, Low_edge, High_edge);
   TH1F* DTh = new TH1F("DTh", "Distribution of "+expression, 200, Low_edge, High_edge);
   
   MCTree->SetAlias("MCexp", expression);
   DTTree->SetAlias("DTexp", expression);


   MCTree -> Project("MCh", "MCexp", "1");
   DTTree -> Project("DTh", "DTexp", "1");

   MCh->GetXaxis()->SetTitle(expression);
   DTh->GetXaxis()->SetTitle(expression);

   MCh->Scale(1./MCh->Integral());
   DTh->Scale(1./DTh->Integral());

   MCh->SetLineColor(kBlue);
   DTh->SetLineColor(kRed);

   TCanvas* mycanv = new TCanvas("mycanv", "", 10, 10, 800, 600);
   MCh->Draw();
   DTh->Draw("same");

   TString filename = expression;
   mycanv->SaveAs(num+"_"+filename+".pdf");

}

void PreSelection ( TTree* MCTree, TTree* DTTree, TString expression, Long64_t SigTotal, Long64_t DTTotal) {
   Long64_t SigCut = MCTree -> GetEntries(expression);
   Long64_t BKGCut = DTTree -> GetEntries(expression);

   cout << expression << ": Sigeffi: " << (Double_t)SigCut/SigTotal *100 << "%, BKG rejection: " << 100. * (1. - (Double_t)BKGCut/DTTotal) << "%" <<endl << endl;
}
