import ROOT
import array
import argparse

parser = argparse.ArgumentParser(description='Read a BDT trained using TMVA')
parser.add_argument("infile")
parser.add_argument("outfile")

args = parser.parse_args()
infile = args.infile
outfile = args.outfile



#init the reader object
reader = ROOT.TMVA.Reader()

#init the variables
varx = array.array('f',[0]) ; reader.AddVariable("x",varx)
vary = array.array('f',[0]) ; reader.AddVariable("y",vary)


reader.BookMVA("BDT","dataset1/weights/TMVAClassification_BDT.weights.xml")

fout = ROOT.TFile(infile+".root","READ")
thetree = fout.Get("dataset1/TestTree")
Histo_signal = ROOT.TH1D('Histo_signal','signal',11,-1.,1.)
Histo_background = ROOT.TH1D('Histo_background','background',11,-1.,1.)
thetree.Project("Histo_signal","BDT","classID<0.5")
thetree.Project("Histo_background","BDT","classID>=0.5")

Histo_signal.SetLineColor(2)
Histo_background.SetLineColor(4)
Histo_signal.SetFillColor(2)
Histo_background.SetFillColor(4)
Histo_signal.SetFillStyle(3001)
Histo_background.SetFillStyle(3001)
Histo_signal.GetXaxis().SetTitle("BDT Score")
Histo_background.GetYaxis().SetTitle("Counts/Bin")

c1 = ROOT.TCanvas()

ymax = max([h.GetMaximum() for h in [Histo_signal,Histo_background] ])
ymax *=1.4
Histo_signal.SetMaximum(ymax)
Histo_signal.Draw()
Histo_background.Draw("same")
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
c1.cd(1).BuildLegend(0.6,  0.6,  0.85,  0.85).SetFillColor(0)
l1=ROOT.TLatex()
l1.SetNDC();
l1.DrawLatex(0.26,0.93,"BDT from TMVA (ROOT)")
atlas = ROOT.TLatex(0.62,0.91,"ATLAS")
atlas.SetNDC()
atlas.SetTextFont(72)
atlas.SetTextColor(1)
atlas.SetLineWidth(2)
atlas.Draw()
internal = ROOT.TLatex(0.745,0.91,"Internal")
internal.SetNDC()
internal.SetTextFont(42)
internal.SetTextColor(1)
internal.SetLineWidth(2)
internal.Draw()
c1.SaveAs(outfile+"response.png","RECREATE")


y = array.array('d')
x = array.array('d')
sig = Histo_signal.Integral()
bkg = Histo_background.Integral()
nbins = Histo_signal.GetNbinsX()
for thisbin in range(1,12):
    y.append(Histo_signal.Integral(thisbin, nbins+1)/sig)
    x.append(Histo_background.Integral(thisbin, nbins+1)/bkg)

roc = ROOT.TGraph(nbins,x,y)
c1 = ROOT.TCanvas()
leg = ROOT.TLegend(0.6,0.3,0.85,0.55)
leg.AddEntry(roc,"BDT response","l")
roc.SetTitle( 'Receiver operating characteristic' )
roc.GetYaxis().SetTitle( 'True positive rate' )
roc.GetXaxis().SetTitle( 'False positive rate' )
roc.Draw()
leg.Draw()
c1.SaveAs(outfile+"roc.png")
