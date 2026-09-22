import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as ani  

def buildfile(file:str) -> pd.DataFrame: 
    data = pd.read_csv(file) 
    data.dropna 
    return data 

load = buildfile("For_Rod.csv")
c1 = load["C1"].to_numpy() 
c2 = load["C2"].to_numpy() 
c3 = load["C3"].to_numpy() 
# print(load)

def dstats(df=load)->pd.DataFrame: 
    descriptive = pd.DataFrame({
        "Cuts": ["C1", "C2", "C3"], 
        "median":[(df["C1"].median()).round(2),(df["C2"].median()).round(2), (df["C3"].median()).round(2)],
        "mean":[(df["C1"].mean()).round(2),(df["C2"].mean()).round(2), (df["C3"].mean()).round(2)],
        "sdev":[(df["C1"].std()),(df["C2"].std()), (df["C3"].std())],
        "min":[(df["C1"].min()),(df["C2"].min()), (df["C3"].min())],
        "max":[(df["C1"].max()),(df["C2"].max()), (df["C3"].max())]
        }) 
    medianAv = (descriptive["median"][0] + descriptive["median"][1] + descriptive["median"][2]) / 3
    meanAv = (descriptive["mean"][0] + descriptive["mean"][1] + descriptive["mean"][2]) / 3 
    stdvAv = (descriptive["sdev"][0] + descriptive["sdev"][1] + descriptive["sdev"][2]) / 3
    minAv = (descriptive["min"][0] + descriptive["min"][1] + descriptive["min"][2]) / 3
    maxAv = ((descriptive["max"][0] + descriptive["max"][1] + descriptive["max"][2])) / 3 

    descriptive = descriptive.transpose() 
    descriptive = descriptive.drop("Cuts")
    descriptive["Avarages"] = [medianAv, meanAv, stdvAv, minAv, maxAv]
    return descriptive  

def boxplots(df=load): 
    plt.boxplot([c1, c2, c3], patch_artist=True)
    plt.grid() 
    plt.show() 

def opp_time (df=load): 
    arr = []
    for i in range(0, len(df["C1"])): 
        arr.append(round((df["C1"][i] + df["C2"][i] + df["C3"][i]) / 3, 2))

    #plt.plot(range(0,len(arr)), arr, color="b", marker = 'o')
    plt.plot(df["Time"], arr, color="b", marker = 'o') 
    plt.show() 

def scat(df=load): 
    fig = plt.figure(figsize=(10, 8)) # layout="constrained")
    plt.title("Batch One cuts", size=25)
    plt.xlabel("Number of Observations", size=15)   # "Observations"
    plt.ylabel("Measured values in mm", size=15)  

    anima = [] 
    arr = []
    for i in range(0, len(df["C1"])): 
        arr.append(round((df["C1"][i] + df["C2"][i] + df["C3"][i]) / 3, 2))
        container = plt.plot(range(0, len(arr)), arr, color="b", marker = 'o')
        anima.append(container)

    animate = ani.ArtistAnimation(fig=fig, artists=anima, interval=150, blit=True)
    #plt.scatter(range(0, len(arr)), arr, color="r")
    #plt.scatter(df["Time"], c1, color="b") 
    #plt.scatter(df["Time"], c2, color="b") # range(0,len(c1))
    #plt.scatter(df["Time"], c3, color="b")
    plt.grid() # the color is not r2 error 
    plt.show() 

#print(scat())

def control(df=load, des = dstats()):
    ucl = des["Avarages"]["mean"]  + (3*des["Avarages"]["sdev"])
    lcl = des["Avarages"]["mean"]  - (3*des["Avarages"]["sdev"])
    #usl = des["Avarages"]["mean"]  + (2*des["Avarages"]["sdev"])
   # lsl = des["Avarages"]["mean"]  - (2*des["Avarages"]["sdev"])

    fig = plt.figure(figsize=(10, 8))# layout="constrained")
    plt.title("Batch One Control Diagram", size=25)
    plt.xlabel("Number of Observations", size=15)   # "Observations"
    plt.ylabel("Measured values in mm", size=15)  
    plt.ylim(bottom=25, top=35) 
    plt.xlim(left=-0.5, right=29.5)
    plt.xticks([0,5,10,15,20,25,29],
        labels=['1', '5', '10', '15','20','25','30']
        )
    
    comb = []
    #an = [] 
    for i in range(0, len(df["C1"])): 
        comb.append(round((df["C1"][i] + df["C2"][i] + df["C3"][i]) / 3, 2))
        #an.append(plt.plot(range(0, len(comb)), comb, marker=".", color="b"))

    plt.plot(range(0, len(comb)), comb, marker=".", color="b")#b
    plt.plot([-0.5,30], [lcl,lcl], ls="dashed", color="r", label="UCL") # +3stdv
    #plt.plot([0,len(comb)], [lsl,lsl], ls="dashed", color="c", alpha=0.5, label="USL") # +2stdv    # thees need to be spesification limits not 2sdevs 
    plt.plot([-0.5,30], [des["Avarages"]["mean"],des["Avarages"]["mean"]], color="k", ls="dotted", label="Center line")  # mean 
    #plt.plot([0,len(comb)], [usl,usl], ls="dashed", color="c", alpha=0.5, label="LSL") # -2sdev
    plt.plot([-0.5,30], [ucl,ucl], ls="dashed", color="r",label="LCL") # -3stdv

    #an = ani.ArtistAnimation(fig=fig, artists=an, interval=200, blit=True)
    #plt.legend(loc="upper right")
    #plt.figlegend(loc="outside lower center")   #"UCL","USL","Mean","LCL","LSL") 
    plt.grid() 
    plt.show()


def In_tolerance(df=load):
    des = dstats() 
    #ucl = 
    fig = plt.figure(figsize=(10, 8))
    plt.title("Batch One Tolerance", size=25)
    plt.xlabel("Number of Observations", size=15)   # "Observations"
    plt.ylabel("Measured values in mm", size=15)  

    #plt.fill_between(x=[-0.5,30], y1=[29,29],color="1",hatch="/", hatchcolor="k", alpha=0.5)  
    #plt.fill_between(x=[-0.5,30], y1=[31,31], y2=[35,35], color="1", hatch="/",hatchcolor="k",alpha=0.5)
    plt.fill_between(x=[-0.5,30], y1=[31,31], y2=[29,29], color="1", hatch="/",hatchcolor="k",alpha=0.5)
    #plt.plot([4,4], [0,35], color="r")

    plt.ylim(bottom=25, top=35) 
    plt.xlim(left=-0.5, right=29.5)
    plt.xticks([0,5,10,15,20,25,29],
        labels=['1', '5', '10', '15','20','25','30']
        )

    plt.plot([-0.5,30], [29,29], ls="dashed", color="r") # lowerlim
    plt.plot([-0.5,30], [30,30], ls="dashed")  # mean 
    plt.plot([-0.5,30], [31,31], ls="dashed", color="r") # upperlim 
    

    out = [] 
    inn = []
    comb = []
    for i in range( 0, len(df["C1"])): 
        val = round((df["C1"][i] + df["C2"][i] + df["C3"][i]) / 3, 2) 
        comb.append(val)  
        if val > 31 or val < 29: 
            out.append(val)
        else: 
            inn.append(val)
    plt.plot(comb, marker=".", color="b", alpha=0.1) 
    #plt.scatter([0,1,2,3], out[:4:],color="r")
    #plt.scatter([0,1,2,3,9,12,18,21,25], out, color="r")
    #plt.scatter([4,5,6,7,8,10,11,13,14,15,16,17,19,20,22,23,24,26,27,28,29], inn, color="c" )
    #plt.plot(c1, marker="o", color="b", label="Cut 1")
    #plt.plot(c2, marker="o", color="g", label="Cut 2")
    #plt.plot(c3, marker="o", color="k", label="Cut 3")
    plt.grid() 
    plt.legend()
    plt.show()

def distribution(values): 
    des = dstats() 
    val = np.concatenate((c1,c2,c3))
    plt.figure(figsize=(10, 8), layout="constrained") 
    plt.title("Batch One Control Diagram")
    #plt.xlabel("Measured values")
    plt.xlabel("Observations") 
    #plt.plot(range(0,len(val)), val)
    #plt.ecdf(val, range(25,35))
    plt.hist(values, [25.5,26,27,28,29,30,31,32,33,34,35] ,histtype="stepfilled") #cumulative=True, histtype="step")
    #plt.plot(range(0,len(val)), val)
    plt.grid() 
    plt.show() 
 
des = dstats() 
val = np.concatenate((c1,c2,c3))
#print(distribution(val)) 
#print(control())
def idealRod (mean): 
    count = 0 
    zval = 1.96 # this comes from the z tables 
    # assuming s dev averages at 1.4 - 1.6 
    stat = zval * ( 1.5 / (np.sqrt(mean)) )      # zval * ( des["Avarages"]["sdev"] / (np.sqrt(mean)) ) 
    lowerC = mean - stat    # des["Avarages"]["mean"] 
    upperC = mean + stat  # 0.05 
    hight = ((lowerC * 5) + (upperC * 5)) + (31.91)     # 31.91mm 

    return hight, lowerC, upperC  

print(idealRod(27))
print(((26.5 * 5) + (27 * 5)) + (33))

print(control())