from GameSimulator import *
import numpy as np

gsw = Team('BOS',[90,100,110,120],[85,90,100,110])
cle = Team('CLE',[90,99,108,117],[85,90,100,110])

msim = MatchupSimulator(gsw,cle)

msim.gamesSim(1000)