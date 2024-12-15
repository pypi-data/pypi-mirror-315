# -*- coding: utf-8 -*-
"""
@author: Joe Rinehart
@contributors: Bernd Saugel
     Sean Coekelenbergh
     Ishita Srivastava
     Brandon Woo




"""
import numpy as np
import math
from matplotlib import pyplot as plt


def ErrorFieldConcordance(X,Y,IDS=[],
                          plot_TF=False,
                          graph_label="",
                          X_name="ΔX",
                          Y_name="ΔY",
                          min_plot_range=3,
                          decolor_threshold=2):

    if (len(X) != len(Y)):
        print ("ErrorFieldConcordance: Reference and Test values must have" +\
               " the same number of observations.")
        return (0,0)
    if (len(X)<2):
        print ("ErrorFieldConcordance: Must have at least two observations" +\
               " per group")
        return (0,0)

    if (len(IDS) == 0):
        IDS = [1] * len(X)
    elif (len(IDS) != len(Y)):
        print ("ErrorFieldConcordance: Length of subject IDs does not "+\
               "match length of observations")
        return (0,0)


    # Calculate changes
    DX = []
    DY = []
    for i in range(1,len(X)):
        if (IDS[i-1] == IDS[i]):
            DX.append(X[i] - X[i-1])
            DY.append(Y[i] - Y[i-1])

    if (len(DX) == 0):
        print ("ErrorFieldConcordance: No matching subject IDs found;" +\
               "not possible to calculate any changes.  Check to be sure " +\
                "subject observations are grouped together and in temporal " +\
                "order in the lists")
        return (0,0)

    plotcols = []
    TotalWeight = 0
    TotalScore = 0
    ScoreArray = []
    WeightArray = []

    for i in range(len(DX)):
        # Point weight is the distance from the plotted point
        # to the origin (0,0).  This is the hypotenuse of the triangle
        # formed by sides of the lengths DX and DY.
        Hypot = np.hypot(DX[i],DY[i])
        # Minimum weight (and avoid division by zero below)
        if (Hypot <= 0.1):
            Hypot = 0.1
        # Calculate the Angle (a) that a line from the origin makes to
        # this point.  Sin (theta) = opp/hypot
        Angle = np.arctan((DY[i])/DX[i])
        Angle = math.degrees(Angle)
        # 'Score' the Agreement: angle <15 full credit (1 pt)
        #                        angle >75 full negative credit (-1 pt)
        #                        graded between 15 & 75
        # First Correct the angle - perfect is 45 degree line
        Angle -= 45
        if (Angle < -90):
            Angle += 180

        # Now calculate the score based on the angle and prepare graphing
        Score = 0
        # Yellow color is (1.0, 0.84, 0)
        #Score = 1 - (2*(abs(Angle) - 15)/60)  # Total range is (75-15)=60
        Score = abs((90-abs(Angle))/45) - 1
        newcol = []
        # Graph Colors (complex shade gradient - this math leads to
        # appropriate boundary transitions by visual appearance)
        thresh = 0.2
        if(Score > thresh):
            s = (Score-thresh)
            newcol = [1-s,0.84-(0.84*s),s]
        elif(Score < -thresh):
            s = (abs(Score)-thresh)
            newcol = [1, 0.84-(0.84*s),0]
            #print (plotcols[-1])
        else:
            #yellow
            newcol = [1.0, 0.84, 0]

        # Now modify the colors by the weight
        if (decolor_threshold > 0):
            if (Hypot < decolor_threshold):
                desat = 1-pow(1-(decolor_threshold-Hypot)/decolor_threshold,2)
                for i in [0,1,2]:
                    k = newcol[i]
                    diff = 0.85 - k
                    mod = diff * desat
                    newcol[i] += mod

        plotcols.append((newcol[0],newcol[1],newcol[2]))

        # now do the tally
        TotalWeight += Hypot
        TotalScore += Hypot * Score
        ScoreArray.append((Hypot * Score)/Hypot)
        WeightArray.append(Hypot)

    # concordance
    conc = np.round(100*TotalScore/TotalWeight,1)

    # weighted standard deviation
    SD = np.round(100*np.sqrt(np.cov(ScoreArray, aweights=WeightArray)),1)

    # R = stat.pearsonr(DX,DY)
    # print ("Pearson:",R[0])

    # R = stat.spearmanr(DX,DY)
    # print ("Spear:", R[0])


    #  plot
    if (plot_TF):
        plt.rcParams.update({'font.size': 14})

        mX = max([abs(ele) for ele in DX])
        mY = max([abs(ele) for ele in DY])
        LIM = max(mX,mY) * 1.05
        LIM = max(LIM,min_plot_range)

        plt.figure(figsize=(6,6))

        plt.ylim(-LIM,LIM)
        plt.xlim(-LIM,LIM)

        gtitle = "Error Field Trending = "+str(conc)+"±"+str(SD)+"%"
        if (graph_label != ""):
            gtitle = graph_label+"\n"+gtitle;

        plt.plot([-LIM,LIM],[-LIM,LIM],color="lightgray")
        plt.title(gtitle)
        if (X_name != ""):
            plt.xlabel(str(X_name))
        if (Y_name != ""):
            plt.ylabel(str(Y_name))

        for k in range(len(DX)):
            plt.scatter(DX[k],DY[k],alpha=min(1,600/len(DX)),
                        color=plotcols[k])

        #plt.text(-4,4,"Conc: "+str(conc))
        #plt.text(-4,3.5,"B/Y/R: ["+str(_b)+","+str(_y)+","+str(_r)+"]")
        #plt.text(-4,3,"Tot : "+str(len(DX)))

        plt.show()

    return (conc,SD)

if __name__ == "__main__":

    print ("Creating Random Data Sample Plot")

    X = np.random.random_sample(1000)*5+2
    #Y= X + np.random.random_sample(100)*(X*0.35) - (X*0.175)
    Y = np.random.random_sample(1000)*5+2
    IDS = [1] * len(X)

    C = ErrorFieldConcordance(X,Y,IDS,True,"Random Noise Example")
    print ("---------------------------")
    print ("Error Field Concordance (-100% to +100%): "+str(C[0])+" ± "+str(C[1])+"%")
