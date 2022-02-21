#!/usr/bin/python

# This program is used to calculate the allowable preload for a bolt.
#Copyright (C) 2022 BracketDesigner
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see http://www.gnu.org/licenses/.

print ("""BoltPreload.py Calculator  Copyright (C) 2022  BracketDesigner
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.\n""")

import sys
if ("show" in sys.argv and "w" in sys.argv):
    print("""--- WARRANTY ---
    THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED 
    BY APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS 
    AND/OR OTHER PARTIES PROVIDE THE PROGRAM “AS IS” WITHOUT WARRANTY OF ANY KIND, 
    EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
    OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE 
    QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE 
    DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.\n""")

if ("show" in sys.argv and "c" in sys.argv):
    print("""--- Conditions ---
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/. \n""")

print("""Please provide information:
    If field is left blank related failure modes will be ignored""")

BoltThread = input("Bolt Thread: ")
BoltMaterial = input("Bolt Material: ")
#Reuse = input("Reusable bolt (y/n): ")
BulkThread = input("Bulk Material Thread: ")
BulkMaterial = input("Bulk Material: ")
EngagementLength = input("EngagementLength (in): ")

def IdentifyThread(thread, isExternal=True, EngagementLength=None):
    # Assuming Unified National Thread Series
    threadsplit = thread.replace(" ","-").split("-")
    MajorDiamStr = threadsplit[0]
    if "/" in MajorDiamStr:
        MajorDiam = float(MajorDiamStr.split("/")[0]) / float(MajorDiamStr.split("/")[1])
    else:
        MajorDiam = str(MajorDiamStr)
    TPI = int(threadsplit[1])

    ThreadDensityLookup = {
            # Thread Identifier | Density | Basic Major Diam
            "0-80":    ["UNF" , .0600],
            "1-64":    ["UNC" , .0730],
            "1-72":    ["UNF" , .0730],
            "2-56":    ["UNC" , .0860],
            "2-64":    ["UNF" , .0860],
            "3-48":    ["UNC" , .0990],
            "3-56":    ["UNF" , .0990],
            "4-40":    ["UNC" , .1120],
            "4-48":    ["UNF" , .1120],
            "5-40":    ["UNC" , .1250],
            "5-44":    ["UNF" , .1250],
            "6-32":    ["UNC" , .1280],
            "6-40":    ["UNF" , .1280],
            "8-32":    ["UNC" , .1640],
            "8-36":    ["UNF" , .1640],
            "10-24":   ["UNC" , .1900],
            "10-32":   ["UNF" , .1900],
            "12-24":   ["UNC" , .2160],
            "12-28":   ["UNF" , .2160],
            "12-32":   ["UNEF", .2160],
            "1/4-20":  ["UNC" , .2500],
            "1/4-28":  ["UNF" , .2500],
            "1/4-32":  ["UNEF", .2500],
            "5/16-18": ["UNC" , .3125],
            "5/16-24": ["UNF" , .3125],
            "5/16-32": ["UNEF", .3125],
            "3/8-16":  ["UNC" , .3750],
            "3/8-24":  ["UNF" , .3750],
            "3/8-32":  ["UNEF", .3750],
            "7/16-14": ["UNC" , .4375],
            "7/16-20": ["UNF" , .4375],
            "7/16-28": ["UNEF", .4375],
            "1/2-13":  ["UNC" , .5000],
            "1/2-20":  ["UNF" , .5000],
            "1/2-28":  ["UNEF", .5000],
            "9/16-12": ["UNC" , .5625],
            "9/16-18": ["UNF" , .5625],
            "9/16-24": ["UNEF", .5625],
            "5/8-11":  ["UNC" , .6250],
            "5/8-18":  ["UNF" , .6250],
            "5/8-24":  ["UNEF", .6250],
            "3/4-10":  ["UNC" , .7500],
            "3/4-16":  ["UNF" , .7500],
            "3/4-20":  ["UNEF", .7500],
            "7/8-9":   ["UNC" , .8750],
            "7/8-14":  ["UNF" , .8750],
            "7/8-20":  ["UNEF", .8750],
            "1-8":     ["UNC" , 1.000],
            "1-12":    ["UNF" , 1.000],
            "1-20":    ["UNEF", 1.000]
            }

    DiamTPI = "-".join(threadsplit[0:2])
    #print(DiamTPI)
    if DiamTPI in ThreadDensityLookup.keys():
            ThreadDensity = ThreadDensityLookup[DiamTPI][0]
            MajorDiam = ThreadDensityLookup[DiamTPI][1]
    else:
        ThreadDensity = "UNS"
        MajorDiam = float(MajorDiam)
        TPI = float(TPI)

    if "1a" in thread or "1b" in thread:
        Class = 1
    elif "2a" in thread or "2b" in thread:
        Class = 2
    elif "3a" in thread or "3b" in thread:
        Class = 3
    elif "4a" in thread or "4b" in thread:
        Class = 4
    elif "5a" in thread or "5b" in thread:
        Class = 5
    else:
        Class = 2 # Assume Class 2, standard

    #if "a" in thread.lower(): #External
    #    ThreadSide = "A"
    #elif "b" in thread.lower(): #Internal
    #    ThreadSide = "B"
    #else:
    if isExternal: # Assume from input, default is external
        ThreadSide = "A"
    else:
        ThreadSide = "B"
    

    # Thread Allowance Calc
    BasicPitchDiam = MajorDiam - 0.64952 / TPI
    BasicMajorDiam = MajorDiam

    EngagementLength = BasicMajorDiam # For tolerance calc, applicable up to 1.5 Major diams) 
    Class2APitchDiamTolerance = 0.0015*BasicMajorDiam**(1/3) + 0.0015*EngagementLength**(1/2) + 0.015 * (1/TPI)**(2/3)

    if ThreadSide == "A": # External Thread (bolt)
        BasicMinorDiam = BasicMajorDiam - 3*3**(1/2)/(4*TPI)
        if Class == 1:
            MajorDiamTolerance = 0.090 * (1/TPI)**(2/3)
        elif Class == 2 or Class == 3:
            MajorDiamTolerance = 0.060 * (1/TPI)**(2/3)

        if Class == 1:
            PitchDiamTolerance = 1.5*Class2APitchDiamTolerance
            Allowance = .3 * Class2APitchDiamTolerance
        elif Class == 2:
            PitchDiamTolerance = Class2APitchDiamTolerance
            Allowance = .3 * Class2APitchDiamTolerance
        elif Class == 3:
            PitchDiamTolerance = .75*Class2APitchDiamTolerance
            Allowance = 0

        MinorDiamTolerance = PitchDiamTolerance + .21650635 * (1/TPI) #UN

        MaxMajorDiam = BasicMajorDiam - Allowance
        MinMajorDiam = MaxMajorDiam - MajorDiamTolerance
        MaxPitchDiam = BasicPitchDiam - Allowance
        MinPitchDiam = MaxPitchDiam - PitchDiamTolerance
        MaxMinorDiam = BasicMinorDiam + Allowance #Note the minor diameter are slightly off from refrences
        MinMinorDiam = MaxMinorDiam - MinorDiamTolerance

    elif ThreadSide == "B": # Internal thread (nut)
        BasicMinorDiam = MajorDiam - 1.08253175 * (1/TPI)
        Allowance = 0

        if Class == 1:
            PitchDiamTolerance = 1.95 * Class2APitchDiamTolerance
        elif Class == 2:
            PitchDiamTolerance = 1.3 * Class2APitchDiamTolerance
        elif Class == 3:
            PitchDiamTolerance = .975 * Class2APitchDiamTolerance

        MajorDiamTolerance = .14433757*(1/TPI) + PitchDiamTolerance

        if Class == 1 or Class == 2:
            if MajorDiam-.25 < .001:
                MinorDiamTolerance = .0500*(1/TPI)**(2/3) + .03*1/(TPI * BasicMajorDiam) - .002
                if MinorDiamTolerance > .3940*(1/TPI):
                    MinorDiamTolerance = .3940*(1/TPI)
                elif MinorDiamTolerance < .25*(1/TPI) - .4 * (1/TPI)**2:
                    MinorDiamTolerance = .25*(1/TPI) - .4 * (1/TPI)**2
            elif TPI >= 4:
                MinorDiamTolerance = .25*(1/TPI)-.4*(1/TPI)**2
            else:
                MinorDiamTolerance = .15*(1/TPI)
        elif Class == 3:
            MinorDiamTolerance = .05*(1/TPI)**(2/3) + .03*1/(TPI * MajorDiam) - .002

            if MinorDiamTolerance > .394*(1/TPI):
                MinorDiamTolerance = .394*(1/TPI)
            elif MinorDiamTolerance < .23*(1/TPI) - 1.5*(1/TPI)**2 and TPI >= 13:
                MinorDiamTolerance = .23*(1/TPI) - 1.5*(1/TPI)**2
            elif MinorDiamTolerance < .12*(1/TPI) and TPI < 13:
                MinorDiamTolerance = .12*(1/TPI)

        MinMajorDiam = BasicMajorDiam - Allowance
        MaxMajorDiam = MinMajorDiam + MajorDiamTolerance
        MinPitchDiam = BasicPitchDiam - Allowance
        MaxPitchDiam = MinPitchDiam + PitchDiamTolerance
        MinMinorDiam = BasicMinorDiam + Allowance #Note the minor diameter are slightly off from refrences
        MaxMinorDiam = MinMinorDiam + MinorDiamTolerance


        
    #print("Minor Diam Tol: " + str(MinorDiamTolerance))

    BasicMajorDiam = round(BasicMajorDiam,4)
    MaxMajorDiam = round(MaxMajorDiam,4)
    MinMajorDiam = round(MinMajorDiam,4)
    BasicPitchDiam = round(BasicPitchDiam,4)
    MaxPitchDiam = round(MaxPitchDiam,4)
    MinPitchDiam = round(MinPitchDiam,4)
    BasicMinorDiam = round(BasicMinorDiam,4)
    MaxMinorDiam = round(MaxMinorDiam,4)
    MinMinorDiam = round(MinMinorDiam,4)

    print("\nThread Callout: " + str(MajorDiam) + "-" + str(TPI) + " " + ThreadDensity + " " + str(Class) + ThreadSide) 
    print("Major: " + str(MaxMajorDiam) + "/" + str(MinMajorDiam))
    print("Pitch: " + str(MaxPitchDiam) + "/" + str(MinPitchDiam))
    print("Minor: " + str(MaxMinorDiam) + "/" + str(MinMinorDiam) + "\n")
    #print("Allowance: " + str(Allowance))
            

    pi = 3.14159265
    #if Class == 1 and ThreadSide == "A":

    TensileStressAreaSmall = (pi/4)*(MajorDiam - 0.938194*(1/TPI))**2
    TensileStressAreaLarge = 3.1416*(MinPitchDiam/2 - 0.16238/TPI)**2

    TensileStressArea = min(TensileStressAreaSmall, TensileStressAreaLarge)

    #print(TensileStressAreaSmall)
    #print(TensileStressAreaLarge)
    #print(TensileStressAreaSmall/TensileStressAreaLarge)

    return TensileStressArea, MaxMinorDiam, MinPitchDiam, EngagementLength, TPI, MaxPitchDiam, MinMajorDiam #in2

def IdentifyMaterial(material):
    materialList = {
        # Material | Yield in PSI
        "18-8": 44961,
        "steel sae grade 2": 74000,
        "6061-t6": 39885,
        "abs": 5800
        }

    if material.lower() in materialList.keys():
        return materialList[material.lower()]
    else:
        print("material not found: " + str(material))
        return None

BoltTensileArea, BoltMaxMinorDiam, BoltMinPitchDiam, BoltEngagementLength, BoltTPI, BoltMaxPitchDiam, BoltMinMajorDiam = IdentifyThread(BoltThread, isExternal=True)
if BulkThread is not "":
    BulkTensileArea, BulkMaxMinorDiam, BulkMinPitchDiam, BulkEngagementLength, BulkTPI, BulkMaxPitchDiam, BulkMinMajorDiam = IdentifyThread(BulkThread, isExternal=False)
else:
    BulkTensileArea, BulkMaxMinorDiam, BulkMinPitchDiam, BulkEngagementLength, BulkTPI, BulkMaxPitchDiam, BulkMinMajorDiam = IdentifyThread(BoltThread, isExternal=False)

BoltYieldStrength = IdentifyMaterial(BoltMaterial)
if BulkMaterial is not "":
    BulkYieldStrength = IdentifyMaterial(BulkMaterial)
else:
    BulkYieldStrength = IdentifyMaterial(BoltMaterial)

# Bolt Yield Mode

YieldLoad = BoltYieldStrength * BoltTensileArea
print("YieldLoad: ",YieldLoad)

#ProofLoad = YieldLoad * .85

#if "y" in Reuse.lower():
#    ReuseMultiplier = .75
#else:
#    ReuseMultiplier = .89
#
#PreloadForce = ProofLoad * ReuseMultiplier

# Bolt Thread Shear Mode

EngagementLength = min(BoltEngagementLength, BulkEngagementLength)

pi = 3.1415926535
BoltShearArea = pi * BoltTPI * EngagementLength * BulkMaxMinorDiam * (1/(2*BoltTPI) + .57735 * (BoltMinPitchDiam - BulkMaxPitchDiam))
BoltThreadShearLoad = BoltYieldStrength * BoltShearArea
print("BoltShearLoad: ", BoltThreadShearLoad)

# Bulk Thread Shear Mode
BulkShearArea = pi * BulkTPI * EngagementLength * BoltMinMajorDiam * (1/(2*BulkTPI) + .57735 * (BoltMinMajorDiam - BulkMaxPitchDiam))

BulkThreadedShearLoad = BulkYieldStrength * BulkShearArea
print("BulkShearLoad: ", BulkThreadedShearLoad)




#print("Preload Force: " + str(round(PreloadForce,4)) + " lbf")

