/* permet de lire les données contenues dans pulsar_coordonnees.txt*/
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include "TH1.h"
#include "TF1.h"
#include "TF2.h"
#include "TFile.h"
#include <iostream>
#include "TCanvas.h"
#include "TH2D.h"
#include "TROOT.h"
#include "TStyle.h" 
#include "TGraphAsymmErrors.h"
#include <fstream>

bool HESS=true;

//******************************************************************************************************************************************
double energy_sensibility[300],errh_energy_sensibility[300],errl_energy_sensibility[300],flux_sensibility[300],errh_flux_sensibility[300],errl_flux_sensibility[300];
 float style[300];;
 int nombre_lignes_sensibility;
 char ta_sensibility[50];
 double emax_sensibility[300];
 double emin_sensibility[300];
 double sensibility_X[300];
 double sensibility_Y[300];
 double sensibility_exl[300];
 double sensibility_exh[300];
 double sensibility_eyl[300];
 double sensibility_eyh[300];

 int read_SED_sensibility_Fermi(int i)
 {
  printf("************************sensibility***********************************\n");
  char emean_char[20];
  char flux_sensibility_char[20];
  char buffer[50000];
  char ttrc[1000];
  nombre_lignes_sensibility=0;
  
  if (i==1) sprintf(ttrc,"../Sensitivity_GalCenter.txt");
  if (i==2) sprintf(ttrc,"../Sensitivity_Intermediairy.txt");
  if (i==3) sprintf(ttrc,"../Sensitivity_GalPole.txt");
  FILE *fp;
  
   if((fp = fopen(ttrc,"r"))==NULL)
     {
      printf("Impossible d'ouvrir le fichier %s\n",ttrc);
      exit(0);
     }
  printf("%s open\n",ttrc);
  int j=0;
  while(!feof(fp))
      {
       energy_sensibility[j]=0.;
       flux_sensibility[j]=0.;
      
       buffer[0]=0;	   
       fgets(buffer,10000,fp);        
       if(!isdigit(buffer[0]))continue;       //lignes vides ou commençant par autre chose qu'un nombre
       
       sscanf(buffer,"%s %s  ",emean_char,flux_sensibility_char);
       
       energy_sensibility[j]=atof(emean_char);
       flux_sensibility[j]=atof(flux_sensibility_char);

       sensibility_X[j] = energy_sensibility[j];
       sensibility_Y[j] = flux_sensibility[j];
       sensibility_exl[j] = 0;
       sensibility_exh[j] = 0;
       sensibility_eyl[j] = 0;
       sensibility_eyh[j] = 0;
       printf("%e %e \n ",sensibility_X[j],sensibility_exl[j],sensibility_Y[j],sensibility_eyh[j]);
       j=j+1;  
       }
  fclose(fp);
  printf("%s close\n",ttrc);
  nombre_lignes_sensibility=j;
  printf("Done\n\n");
  return 0;    
 }



double energy_Fermi[300],errh_energy_Fermi[300],errl_energy_Fermi[300],flux_Fermi[300],errh_flux_Fermi[300],errl_flux_Fermi[300];
 float style[300];;
 int nombre_lignes_Fermi;
 char ta_Fermi[50];
 double emax_Fermi[300];
 double emin_Fermi[300];
 double Fermi_X[300];
 double Fermi_Y[300];
 double Fermi_exl[300];
 double Fermi_exh[300];
 double Fermi_eyl[300];
 double Fermi_eyh[300];

 int read_SED_Fermi_pointlike()
 {
  printf("************************Fermi***********************************\n");
  char emin_char[20];
  char emax_char[20];
  char errl_emin_char[20];
  char flux_Fermi_char[20];
  char errh_flux_Fermi_char[20];
  char errl_flux_Fermi_char[20];
  char buffer[50000];
  char ttrc[1000];
  nombre_lignes_Fermi=0;
  
  sprintf(ttrc,"GeV.txt");
  FILE *fp;
  
   if((fp = fopen(ttrc,"r"))==NULL)
     {
      printf("Impossible d'ouvrir le fichier %s\n",ttrc);
      exit(0);
     }
  printf("%s open\n",ttrc);
  int j=0;
  while(!feof(fp))
      {
       energy_Fermi[j]=0.;
       errh_energy_Fermi[j]=0.;
       errl_energy_Fermi[j]=0.;
       flux_Fermi[j]=0.;
       errh_flux_Fermi[j]=0.;
       errl_flux_Fermi[j]=0.;
       emax_Fermi[j]=0;
       emin_Fermi[j]=0;
      
       buffer[0]=0;	   
       fgets(buffer,10000,fp);        
       if(!isdigit(buffer[0]))continue;       //lignes vides ou commençant par autre chose qu'un nombre
       
       sscanf(buffer,"%s %s %s %s  ",emin_char,emax_char,flux_Fermi_char,errh_flux_Fermi_char);
       
      emax_Fermi[j]=atof(emax_char);
      emin_Fermi[j]=atof(emin_char);
       energy_Fermi[j]= pow( 10 , ( log10(emin_Fermi[j]) +  log10(emax_Fermi[j]) ) / 2. ) ;
       errh_energy_Fermi[j]=(emax_Fermi[j]) - energy_Fermi[j];
       errl_energy_Fermi[j]=energy_Fermi[j] - (emin_Fermi[j]);
        flux_Fermi[j]=atof(flux_Fermi_char);
        errh_flux_Fermi[j]=atof(errh_flux_Fermi_char);
        errl_flux_Fermi[j]=atof(errh_flux_Fermi_char);

       Fermi_X[j] = energy_Fermi[j];
       Fermi_Y[j] = flux_Fermi[j];
       Fermi_exl[j] = errl_energy_Fermi[j];
       Fermi_exh[j] = errh_energy_Fermi[j];
       Fermi_eyl[j] = errl_flux_Fermi[j];
       Fermi_eyh[j] = errh_flux_Fermi[j];
       printf("%e %e %e %e \n ",Fermi_X[j],Fermi_exl[j],Fermi_Y[j],Fermi_eyh[j]);
       j=j+1;  
       }
  fclose(fp);
  printf("%s close\n",ttrc);
  nombre_lignes_Fermi=j;
  printf("Done\n\n");
  return 0;    
 }

 double energy_Fermi_UL[300],errh_energy_Fermi_UL[300],errl_energy_Fermi_UL[300],flux_Fermi_UL[300],errh_flux_Fermi_UL[300],errl_flux_Fermi_UL[300];
 float style[300];;
 int nombre_lignes_Fermi_UL;
 char ta_Fermi_UL[50];
 double emax_Fermi_UL[300];
 double emin_Fermi_UL[300];
 double Fermi_UL_X[300];
 double Fermi_UL_Y[300];
 double Fermi_UL_exl[300];
 double Fermi_UL_exh[300];
 double Fermi_UL_eyl[300];
 double Fermi_UL_eyh[300];

 int read_SED_Fermi_UL_pointlike()
 {
  printf("************************Fermi_UL***********************************\n");
  char emin_char[20];
  char emax_char[20];
  char errl_emin_char[20];
  char flux_Fermi_UL_char[20];
  char errh_flux_Fermi_UL_char[20];
  char errl_flux_Fermi_UL_char[20];
  char buffer[50000];
  char ttrc[1000];
  nombre_lignes_Fermi_UL=0;
  
  sprintf(ttrc,"GeV_UL.txt");
  FILE *fp;
  
   if((fp = fopen(ttrc,"r"))==NULL)
     {
      printf("Impossible d'ouvrir le fichier %s\n",ttrc);
      exit(0);
     }
  printf("%s open\n",ttrc);
  int j=0;
  while(!feof(fp))
      {
       energy_Fermi_UL[j]=0.;
       errh_energy_Fermi_UL[j]=0.;
       errl_energy_Fermi_UL[j]=0.;
       flux_Fermi_UL[j]=0.;
       errh_flux_Fermi_UL[j]=0.;
       errl_flux_Fermi_UL[j]=0.;
       emax_Fermi_UL[j]=0;
       emin_Fermi_UL[j]=0;
      
       buffer[0]=0;	      
       fgets(buffer,10000,fp);        
       if(!isdigit(buffer[0]))continue;       //lignes vides ou commençant par autre chose qu'un nombre
       
       sscanf(buffer,"%s %s %s %s  ",emin_char,emax_char,flux_Fermi_UL_char,errh_flux_Fermi_UL_char);
       
       emax_Fermi_UL[j]=atof(emax_char);
       emin_Fermi_UL[j]=atof(emin_char);
       energy_Fermi_UL[j]= pow( 10 , ( log10(emin_Fermi_UL[j]) +  log10(emax_Fermi_UL[j]) ) / 2. ) ;
       errh_energy_Fermi_UL[j]=(emax_Fermi_UL[j]) - energy_Fermi_UL[j];
       errl_energy_Fermi_UL[j]=energy_Fermi_UL[j] - (emin_Fermi_UL[j]);
        flux_Fermi_UL[j]=atof(flux_Fermi_UL_char);
        errh_flux_Fermi_UL[j]=0.;
        errl_flux_Fermi_UL[j]=0.4*flux_Fermi_UL[j];

       Fermi_UL_X[j] = energy_Fermi_UL[j];
       Fermi_UL_Y[j] = flux_Fermi_UL[j];
       Fermi_UL_exl[j] = errl_energy_Fermi_UL[j];
       Fermi_UL_exh[j] = errh_energy_Fermi_UL[j];
       Fermi_UL_eyl[j] = errl_flux_Fermi_UL[j];
       Fermi_UL_eyh[j] = errh_flux_Fermi_UL[j];
       printf("%e %e %e %e \n ",Fermi_UL_X[j],Fermi_UL_exl[j],Fermi_UL_Y[j],Fermi_UL_eyh[j]);
       j=j+1;  
       }
  fclose(fp);
  printf("%s close\n",ttrc);
  nombre_lignes_Fermi_UL=j;
  return 0;    
 }

double energy_HESS[300],errh_energy_HESS[300],errl_energy_HESS[300],flux_HESS[300],errh_flux_HESS[300],errl_flux_HESS[300];
 float style[300];;
 int nombre_lignes_HESS;
 char ta_HESS[50];
 double emax_HESS[300];
 double emin_HESS[300];
 double HESS_X[300];
 double HESS_Y[300];
 double HESS_exl[300];
 double HESS_exh[300];
 double HESS_eyl[300];
 double HESS_eyh[300];

 int read_SED_HESS()
 {
  printf("************************HESS***********************************\n");
  char emin_char[20];
  char emax_char[20];
  char errl_emin_char[20];
  char flux_HESS_char[20];
  char errh_flux_HESS_char[20];
  char errl_flux_HESS_char[20];
  char buffer[50000];
  char ttrc[1000];
  nombre_lignes_HESS=0;
  
  sprintf(ttrc,"TeV.txt");
  FILE *fp;
  
   if((fp = fopen(ttrc,"r"))==NULL)
     {
      printf("Impossible d'ouvrir le fichier %s\n",ttrc);
      exit(0);
     }
  printf("%s open\n",ttrc);
  int j=0;
  while(!feof(fp))
      {
       energy_HESS[j]=0.;
       errh_energy_HESS[j]=0.;
       errl_energy_HESS[j]=0.;
       flux_HESS[j]=0.;
       errh_flux_HESS[j]=0.;
       errl_flux_HESS[j]=0.;
       emax_HESS[j]=0;
       emin_HESS[j]=0;
      
       buffer[0]=0;	      
       fgets(buffer,10000,fp);        
       if(!isdigit(buffer[0]))continue;       //lignes vides ou commençant par autre chose qu'un nombre
       
       sscanf(buffer,"%s %s %s %s  ",emin_char,emax_char,flux_HESS_char,errh_flux_HESS_char);
       
       emax_HESS[j]=atof(emax_char);
       emin_HESS[j]=atof(emin_char);
       energy_HESS[j]= pow( 10 , ( log10(emin_HESS[j]) +  log10(emax_HESS[j]) ) / 2. );
       errh_energy_HESS[j]=(emax_HESS[j]) - energy_HESS[j];
       errl_energy_HESS[j]=energy_HESS[j] - (emin_HESS[j]);
        flux_HESS[j]=atof(flux_HESS_char);//*(emax_HESS[j]-emin_HESS[j]));
        errh_flux_HESS[j]=atof(errh_flux_HESS_char);//*(emax_HESS[j]-emin_HESS[j]));
        errl_flux_HESS[j]=atof(errh_flux_HESS_char);//*(emax_HESS[j]-emin_HESS[j]));
 
       HESS_X[j] = energy_HESS[j];
       HESS_Y[j] = flux_HESS[j];
       HESS_exl[j] = errl_energy_HESS[j];
       HESS_exh[j] = errh_energy_HESS[j];
       HESS_eyl[j] = errl_flux_HESS[j];
       HESS_eyh[j] = errh_flux_HESS[j];
       printf("%e %e %e %e \n ",HESS_X[j],HESS_exl[j],HESS_Y[j],HESS_eyh[j]);
       j=j+1;  
       }
  fclose(fp);
  printf("%s close\n",ttrc);
  nombre_lignes_HESS=j;
  return 0;    
 }



// ***************************************************************************************************
// ***************************************************************************************************
// ***************************************************************************************************

void plot(){
 gROOT->SetStyle("Plain");
    gROOT->SetStyle("Plain");
    gStyle->SetPalette(1);

    gStyle->SetFillColor(0);
    gStyle->SetCanvasColor(10);

    // Frame
    gStyle->SetFrameBorderMode(0);
    gStyle->SetFrameFillColor(0);

    // Pad
    gStyle->SetPadBorderMode(0);
    gStyle->SetPadColor(0);
    gStyle->SetPadTopMargin(0.07);
    gStyle->SetPadLeftMargin(0.13);
    gStyle->SetPadRightMargin(0.05);
    gStyle->SetPadBottomMargin(0.1);
    gStyle->SetPadTickX(1);  //make ticks be on all 4 sides.
    gStyle->SetPadTickY(1);

    // histogram
    gStyle->SetHistFillStyle(0);
    gStyle->SetOptTitle(0);

    // histogram title
    gStyle->SetTitleSize(0.22);
    gStyle->SetTitleFontSize(2);
    gStyle->SetTitleFont(42);
    gStyle->SetTitleFont(62,"xyz");
    gStyle->SetTitleYOffset(1.0);
    gStyle->SetTitleXOffset(1.0);
    gStyle->SetTitleXSize(0.04);
    gStyle->SetTitleYSize(0.04);
    gStyle->SetTitleX(.15);
    gStyle->SetTitleY(.98);
    gStyle->SetTitleW(.70);
    gStyle->SetTitleH(.05);

    // statistics box
    gStyle->SetOptStat(0);
    gStyle->SetStatFont(42);
    gStyle->SetStatX(.91);
    gStyle->SetStatY(.90);
    gStyle->SetStatW(.15);
    gStyle->SetStatH(.15);

    // axis labels
    gStyle->SetLabelFont(42,"xyz");
    gStyle->SetLabelSize(0.035,"xyz");
    gStyle->SetGridColor(16);

    gStyle->SetLegendBorderSize(0);

    // Pad
    Float_t small = 1e-5;
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    gStyle->SetPadGridX(1);
    gStyle->SetPadGridY(1);
    gStyle->SetPadBorderMode(0);

 TCanvas *cc = new TCanvas("cc","",900,600);
 cc->cd(1);
 gPad->SetLogy(1);
 gPad->SetLogx(1);
 if (HESS==true) TH2F *frame =new TH2F("frame","",100,50,5.e7,100,8e-14,5e-10);
 if (HESS==false) TH2F *frame =new TH2F("frame","",100,80,1.5e5,100,6e-14,3e-10);
 frame->SetStats(kFALSE);
 frame->GetXaxis()->SetLabelSize(0.04);
 frame->GetXaxis()->SetTitle("Energy [MeV]");
 frame->GetYaxis()->CenterTitle();
 frame->GetXaxis()->CenterTitle();
 frame->GetXaxis()->SetTitleSize(0.045);
 frame->GetYaxis()->SetLabelSize(0.04);
 frame->GetYaxis()->SetTitle("E^{2} dN/dE [erg cm^{-2} s^{-1}]");
 frame->GetYaxis()->SetTitleSize(0.045);
 frame->Draw();


 read_SED_sensibility_Fermi(1);
 int nbin_sensibility=nombre_lignes_sensibility;
 TGraphAsymmErrors *sensibility_graph1 = new TGraphAsymmErrors(nbin_sensibility,sensibility_X,sensibility_Y,sensibility_exl,sensibility_exh,sensibility_eyl,sensibility_eyh);
 sensibility_graph1->SetLineColor(6);
 sensibility_graph1->SetLineStyle(3);
 sensibility_graph1->SetLineWidth(3);
 sensibility_graph1->Draw("Csame");
 
 read_SED_sensibility_Fermi(2);
 int nbin_sensibility=nombre_lignes_sensibility;
 TGraphAsymmErrors *sensibility_graph2 = new TGraphAsymmErrors(nbin_sensibility,sensibility_X,sensibility_Y,sensibility_exl,sensibility_exh,sensibility_eyl,sensibility_eyh);
 sensibility_graph2->SetLineColor(8);
 sensibility_graph2->SetLineStyle(3);
 sensibility_graph2->SetLineWidth(3);
 sensibility_graph2->Draw("Csame");
 
 read_SED_sensibility_Fermi(3);
 int nbin_sensibility=nombre_lignes_sensibility;
 TGraphAsymmErrors *sensibility_graph3 = new TGraphAsymmErrors(nbin_sensibility,sensibility_X,sensibility_Y,sensibility_exl,sensibility_exh,sensibility_eyl,sensibility_eyh);
 sensibility_graph3->SetLineColor(5);
 sensibility_graph3->SetLineStyle(3);
 sensibility_graph3->SetLineWidth(3);
 sensibility_graph3->Draw("Csame");
  
 read_SED_Fermi_pointlike();
 int nbin_Fermi=nombre_lignes_Fermi;
 TGraphAsymmErrors *Fermi_graph1 = new TGraphAsymmErrors(nbin_Fermi,Fermi_X,Fermi_Y,Fermi_exl,Fermi_exh,Fermi_eyl,Fermi_eyh);
 Fermi_graph1->SetMarkerSize(2.);
 Fermi_graph1->SetMarkerStyle(29);
 Fermi_graph1->SetMarkerColor(2);
 Fermi_graph1->SetLineColor(2);
 Fermi_graph1->Draw("psame");
 
 read_SED_Fermi_UL_pointlike();
 int nbin_Fermi_UL=nombre_lignes_Fermi_UL;
 TGraphAsymmErrors *Fermi_UL_graph1 = new TGraphAsymmErrors(nbin_Fermi_UL,Fermi_UL_X,Fermi_UL_Y,0,0,Fermi_UL_eyl,Fermi_UL_eyh);
 Fermi_UL_graph1->SetMarkerSize(2.);
 Fermi_UL_graph1->SetMarkerStyle(30);
 Fermi_UL_graph1->SetMarkerColor(2);
 Fermi_UL_graph1->SetLineColor(2);
 Fermi_UL_graph1->Draw("p>same");
 TGraphAsymmErrors *Fermi_UL_graph2 = new TGraphAsymmErrors(nbin_Fermi_UL,Fermi_UL_X,Fermi_UL_Y,Fermi_UL_exl,Fermi_UL_exh,0,0);
 Fermi_UL_graph2->SetMarkerSize(2.);
 Fermi_UL_graph2->SetMarkerStyle(30);
 Fermi_UL_graph2->SetMarkerColor(2);
 Fermi_UL_graph2->SetLineColor(2);
 Fermi_UL_graph2->Draw("psame");
 
 if (HESS==true) {
 read_SED_HESS();
 int nbin_HESS=nombre_lignes_HESS;
 TGraphAsymmErrors *HESS_graph1 = new TGraphAsymmErrors(nbin_HESS,HESS_X,HESS_Y,HESS_exl,HESS_exh,HESS_eyl,HESS_eyh);
 HESS_graph1->SetMarkerSize(1.5);
 HESS_graph1->SetMarkerStyle(23);
 HESS_graph1->SetMarkerColor(4);
 HESS_graph1->SetLineColor(4);
 HESS_graph1->Draw("psame");

// TF1 *f=new TF1("f","4.50e-12*(x/1e6)**(-2.53)*x*x/624151/1e6",0.380e6,20e6);
 //TF1 *f=new TF1("f","4.2e-12*(x/1e6)**(-2.)*x*x/624151/1e6",0.6e6,30e6);
 //f->SetLineColor(4);
 //f->SetLineWidth(2);
 //f->SetLineStyle(1);
 //f->Draw("same");}
 }
 TLegend* legend = new TLegend(0.7,0.75,0.9,0.9); // (x1,y1,x2,y2)
 legend->AddEntry(Fermi_graph1,"Fermi","p");
 if (HESS==true) legend->AddEntry(HESS_graph1,"HESS","p");
// legend->Draw();
  
  if (HESS==true){
  cc->Print("SED_with_TeV_data_with_legend.png");
  cc->Print("SED_with_TeV_data_with_legend.eps");
  cc->Print("SED_with_TeV_data_with_legend.root");}
  else{
  cc->Print("SED_with_legend.png");
  cc->Print("SED_with_legend.eps");
  cc->Print("SED_with_legend.root");}
  
}

