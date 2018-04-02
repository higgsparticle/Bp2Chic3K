#include <cstdlib>
#include <iostream>
#include <map>
#include <string>

#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TChain.h"
#include "fstream"
#include "TROOT.h"

#include "TMVA/Factory.h"
#include "TMVA/DataLoader.h"
#include "TMVA/Tools.h"
#include "TMVA/TMVAGui.h"
#include "ConfigureEachMethod.C"

void ConfigureEachMethod(TMVA::Factory *factory,TMVA::DataLoader loader,std::map<std::string,int> Use);
void TMVAClassification(int index=0)
{

    // Default MVA methods to be trained + tested
    ifstream fconf("MethodConf.txt",ios::in);
    if(!fconf) {
        exit(0);
        cout<<"configuration files not found"<<endl;
    }
    else{
        cout<<"configuration files found"<<endl;
    }
    string method;
    int use;
    std::map<std::string,int> Use;
    while(true){
        fconf>>method>>use;
        if(fconf.eof()) break;
        Use[method] = use;
    }

    TMVA::Tools::Instance();
    std::cout << "==> Start TMVAClassification" << std::endl;
    //std::cout << "--- TMVAClassification       : Using input file: " << input->GetName() << std::endl;
    TChain *tsig1 = new TChain("DecayTree");
    tsig1->Add("../MCRunIUpdate.root");
    TTree *tsig = (TTree*) tsig1->CopyTree("Bp_BKGCAT==0||Bp_BKGCAT==50");
    std::cout<<"numSig: "<<tsig->GetEntries()<<endl;


    TChain *tbkg = new TChain("DecayTree");
    tbkg->Add("../DataRunIUpdate.root");

    std::cout<<"numBkg: "<<tbkg->GetEntries()<<endl;

    TFile* outputFile = TFile::Open( "MVAtrainning.root", "RECREATE" );

    TMVA::Factory *factory = new TMVA::Factory( "TMVAClassification", outputFile,
            "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" );

    TMVA::DataLoader *dataloader=new TMVA::DataLoader("dataset");
    //factory->SetSignalWeightExpression( "<YourSignalWeightExpression>" );
    //factory->SetBackgroundWeightExpression( "<YourBackgroundWeightExpression>" );



    dataloader->AddVariable( "minPT", 'F' );
    dataloader->AddVariable( "log(minIPCHI2)", 'F' );
    dataloader->AddVariable( "minPID", 'F' );
    dataloader->AddVariable( "gamma_CL", 'F' );
    dataloader->AddVariable( "gamma_PT", 'F' );
    dataloader->AddVariable( "Bp_IPCHI2_OWNPV", 'F' );
    dataloader->AddVariable( "Bp_PT", 'F' );
    dataloader->AddVariable( "log(Bp_FDCHI2_OWNPV)", 'F' );
    dataloader->AddVariable( "Bp_ConstChic1Fit_chi2[0]", 'F' );


    Double_t signalWeight     = 1.0;
    Double_t backgroundWeight = 1.0;

    dataloader->AddSignalTree    ( tsig,     signalWeight );
    dataloader->AddBackgroundTree( tbkg, backgroundWeight );

    TCut mycutb = "Bp_IPCHI2_OWNPV<100&&Bp_ConstChic1Fit_chi2[0]<500&&Bp_ConstChic1Fit_M[0]>5500&&Bp_ConstChic1Fit_M[0]<5600"; // for example: TCut mycuts = "abs(var1)<0.5 && abs(var2-0.5)<1";
    TCut mycuts = "Bp_IPCHI2_OWNPV<100&&Bp_ConstChic1Fit_chi2[0]<500"; // for example: TCut mycuts = "abs(var1)<0.5";

    TString train_test=TString::Format("nTrain_Signal=%i:nTrain_Background=%i:SplitMode=Random:NormMode=NumEvents:!V",
                int(tsig->GetEntries(mycuts)*0.5),
                int(tbkg->GetEntries(mycutb)*0.1)
                );
    dataloader->PrepareTrainingAndTestTree( mycuts, mycutb,train_test.Data());
    //        "SplitMode=Random:NormMode=NumEvents:!V" );
    //"nTrain_Signal=1000:nTrain_Background=1000:SplitMode=Random:NormMode=NumEvents:!V" );

    ConfigureEachMethod(factory,dataloader, Use);
    factory->TrainAllMethods();
    factory->TestAllMethods();
    factory->EvaluateAllMethods();

    outputFile->Close();
    std::cout << "==> Wrote root file: " << outputFile->GetName() << std::endl;
    std::cout << "==> TMVAClassification is done!" << std::endl;

    delete factory;
    delete dataloader;
    // Launch the GUI for the root macros
    //if (!gROOT->IsBatch()) TMVA::TMVAGui( outfileName+".root" );
    gROOT->ProcessLine(".q");

}
