import ROOT
import argparse

parser = argparse.ArgumentParser(description='Train a BDT using TMVA')
parser.add_argument("infile")
parser.add_argument("datasetname")
parser.add_argument("jobname")
parser.add_argument("outfile")

args = parser.parse_args()
infile = args.infile
datasetname = args.datasetname
jobname = args.jobname
outfile = args.outfile


infile = ROOT.TFile.Open(infile+".root")
ntuple = infile.Get("ntuple")

ROOT.TMVA.Tools.Instance()
fout = ROOT.TFile(outfile+".root","RECREATE")
factory = ROOT.TMVA.Factory(jobname, fout,
                            ":".join([
                                "!V",
                                "!Silent",
                                "Color",
                                "DrawProgressBar",
                                "Transformations=I;D;P;G,D",
                                "AnalysisType=Classification"]
                                     ))

loader = ROOT.TMVA.DataLoader(datasetname)
loader.AddVariable("x","F")
loader.AddVariable("y","F")
loader.AddSignalTree(ntuple)
loader.AddBackgroundTree(ntuple)
sigCut = ROOT.TCut("signal < 0.5")
bgCut = ROOT.TCut("signal >= 0.5")
 
loader.PrepareTrainingAndTestTree(sigCut,   # signal events
                                   bgCut,    # background events
                                   ":".join([
                                        "nTrain_Signal=0",
                                        "nTrain_Background=0",
                                        "SplitMode=Random",
                                        "NormMode=NumEvents",
                                        "!V"
                                       ]))

method = factory.BookMethod(loader,ROOT.TMVA.Types.kBDT, "BDT",
                   ":".join([
                       "!H",
                       "!V",
                       "NTrees=200",
                       "nEventsMin=150",
                       "MaxDepth=1",
                       "BoostType=AdaBoost",
                       "AdaBoostBeta=0.5",
                       "SeparationType=GiniIndex",
                       "nCuts=20",
                       "PruneMethod=NoPruning",
                       ]))
 
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
