import ROOT
import argparse

parser = argparse.ArgumentParser(description='Generate two dimentional random data and export to a root file')
parser.add_argument("events", help="number of events to generate", type=int)
parser.add_argument("filename")

args = parser.parse_args()
events = args.events
outfile = args.filename

dataset = ROOT.TFile(outfile+".root","RECREATE")

ntuple = ROOT.TNtuple("ntuple","ntuple","x:y:signal")
for i in range(events):
    # throw a signal event centered at (1,1)
    ntuple.Fill(ROOT.gRandom.Gaus(1,1), # x
                ROOT.gRandom.Gaus(1,1), # y
                0)                      # signal
     
    # throw a background event centered at (-1,-1)
    ntuple.Fill(ROOT.gRandom.Gaus(-1,1), # x
                ROOT.gRandom.Gaus(-1,1), # y
                1)                       # background

dataset.Write()
dataset.Close()
