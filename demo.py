import matplotlib.pyplot as plt
import pickle as pkl
from astropy.wcs import WCS
from playsound import playsound
import wave
from matplotlib import pyplot as plt
import numpy as np
import csv
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.io import fits
from matplotlib.widgets import RadioButtons

#FRB DATA
FRB_RA = []
FRB_DEC = []
FRB_DM = []
FRB_heimSNR = []
FRBs= []
FRB_mjd = []
FRB_z = []
FRB_w = []
FRB_BEAM = []
FRB_IDS = []
FRB_RM = []
FRB_RMerr = []
FRB_RMgal = []
FRB_RMgalerr = []
FRB_RMion = []
FRB_RMionerr = []
def update_FRB_params(fname="DSA110-FRBs-PARSEC_TABLE.csv",path="./",nmax=np.inf):
    """
    This function updates the global FRB parameters from the provided file. File is a copy
    of the 'tablecsv' tab in the DSA110 FRB spreadsheet.
    """
    with open(path + fname,"r") as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        idx = 0
        for row in reader:
            if idx >= nmax: break
            idx += 1
            #print(row)
            if row[0] != "name" and row[0] != "": #\ufeff
                FRBs.append(row[0])

                if row[1] != "":
                    FRB_mjd.append(float(row[1]))
                else:
                    FRB_mjd.append(-1)

                if row[2] != "":
                    FRB_heimSNR.append(float(row[2]))
                else:
                    FRB_heimSNR.append(-1)

                if row[4] != "":
                    FRB_DM.append(float(row[4]))
                elif row[3] != "":
                    FRB_DM.append(float(row[3]))
                else:
                    FRB_DM.append(-1)

                if row[6] != "":
                    FRB_w.append(int(row[6]))
                else:
                    FRB_w.append(-1)

                if row[7] != "":
                    FRB_z.append(float(row[7]))
                else:
                    FRB_z.append(-1)

                if row[8] != "":
                    FRB_RA.append(float(row[8]))
                else:
                    FRB_RA.append(-1)

                if row[9] != "":
                    FRB_DEC.append(float(row[9]))
                else:
                    FRB_DEC.append(-1)
                #print(row)
                if row[10] != "":
                    FRB_BEAM.append(float(row[10]))
                else:
                    FRB_BEAM.append(-1)

                if row[11] != "":
                    FRB_IDS.append(str(row[11]))
                else:
                    FRB_IDS.append("")

                if row[12] != "":
                    FRB_RM.append(float(row[12]))
                else:
                    FRB_RM.append(np.nan)

                if row[13] != "":
                    FRB_RMerr.append(float(row[13]))
                else:
                    FRB_RMerr.append(np.nan)

                if row[14] != "":
                    FRB_RMgal.append(float(row[14]))
                else:
                    FRB_RMgal.append(np.nan)

                if row[15] != "":
                    FRB_RMgalerr.append(float(row[15]))
                else:
                    FRB_RMgalerr.append(np.nan)

                if row[16] != "":
                    FRB_RMion.append(float(row[16]))
                else:
                    FRB_RMion.append(np.nan)

                if row[17] != "":
                    FRB_RMionerr.append(float(row[17]))
                else:
                    FRB_RMionerr.append(np.nan)
                #if no directory exists, make one
                #if len(glob.glob(dirs['data']+FRB_IDS[-1] + "_" + FRBs[-1])) == 0:
                #    os.system("mkdir " + dirs['data']+FRB_IDS[-1] + "_" + FRBs[-1])
            
    return
update_FRB_params(fname="DSA110-FRBs-PARSEC_TABLE.csv",path="./data/",nmax=25)


FRB_COORDS = SkyCoord(ra=FRB_RA*u.deg,dec=FRB_DEC*u.deg,frame='icrs')
FRB_LON = FRB_COORDS.galactic.l.value
FRB_LAT = FRB_COORDS.galactic.b.value

vicinity = 3 #deg



#non-DSA FRBs
fname = "./data/FRB_CATALOG_DATA_POSTREFEREE_DEMO.pkl"
f = open(fname,"rb")
data2 = pkl.load(f)
f.close()

otherFRBcondition = np.logical_and(~np.isnan(data2['FRBWIDTHS']),~np.isnan(data2['FRBSNRS']))
otherFRBcoords = SkyCoord(ra=data2['FRBRAS'][otherFRBcondition]*u.deg,dec=data2['FRBDECS'][otherFRBcondition]*u.deg,frame='icrs')
otherFRBLONS = otherFRBcoords.galactic.l.value
otherFRBLATS = otherFRBcoords.galactic.b.value
otherFRBNAMES = data2['FRBNAMES'][otherFRBcondition]


#PSRs
fname = "./data/PSR_CATALOG_DATA.pkl"
f = open(fname,"rb")
data3 = pkl.load(f)
f.close()
PSRnames = np.load("./data/PSRnames.npy")
PSRcoords = []
PSRRAS = []
PSRDECS = []
PSRRAS2 = []
PSRDECS2 = []
PSRFLAGS = []
PSRLONS = []
PSRLATS = []
for n in PSRnames:
    if n in data3['BNAMES']: i = list(data3['BNAMES']).index(n)
    elif n in data3['JNAMES']: i = list(data3['JNAMES']).index(n)

    if ':' in data3['RAS'][i]:
        PSRFLAGS.append(True)
        PSRRAS.append(data3['RAS'][i])
        PSRDECS.append(data3['DECS'][i])
    else:
        PSRFLAGS.append(False)
        PSRRAS.append(float(data3['RAS'][i]))
        PSRDECS.append(float(data3['DECS'][i]))
PSRFLAGS = np.array(PSRFLAGS)
PSRNAMES = (PSRnames[PSRFLAGS],PSRnames[~PSRFLAGS])
PSRcoords = (SkyCoord([PSRRAS[i]+PSRDECS[i] for i in range(len(PSRRAS))],unit=(u.hourangle,u.deg),frame='icrs'),SkyCoord(ra=np.array(PSRRAS2)*u.deg,dec=np.array(PSRDECS2)*u.deg,frame='icrs'))
PSRLONS = (PSRcoords[0].galactic.l.value,PSRcoords[1].galactic.l.value)
PSRLATS = (PSRcoords[0].galactic.b.value,PSRcoords[1].galactic.b.value)


#magnetars
fname = "./data/MAGdata.pkl"
f = open(fname,"rb")
MAGdata = pkl.load(f)
f.close()
MAGNAMES = MAGdata['names']
MAGcoords = SkyCoord(ra=MAGdata['RAS']*u.deg,dec=MAGdata['DECS']*u.deg,frame='icrs')
MAGLONS = MAGcoords.galactic.l.value
MAGLATS = MAGcoords.galactic.b.value


wavtype='_combined'
wavtypes = {'Full':'_combined','Intensity':'','Linear':'_L','Circular':'_V'}
def onclick(event,wcs):
    


    #see if clicked near FRB
    clicked_coord = wcs.pixel_to_world(event.xdata,event.ydata)
    if np.any(np.abs(clicked_coord.separation(FRB_COORDS).to(u.deg).value) < vicinity):
        FRBclicked = np.argmin(np.abs(clicked_coord.separation(FRB_COORDS).to(u.deg).value))
        print(FRBclicked,FRBs[FRBclicked])
        
        playsound("wavs/" + FRB_IDS[FRBclicked] + "_" + FRBs[FRBclicked] + "_sound" + wavtype + ".wav")
    elif np.any(np.abs(clicked_coord.separation(otherFRBcoords).to(u.deg).value) < vicinity):
        FRBclicked = np.argmin(np.abs(clicked_coord.separation(otherFRBcoords).to(u.deg).value))
        print(FRBclicked,otherFRBNAMES[FRBclicked])
        
        playsound("wavs/" + otherFRBNAMES[FRBclicked] + "_sound" + wavtype + ".wav")
    elif np.any(np.abs(clicked_coord.separation(MAGcoords).to(u.deg).value) < vicinity):
        MAGclicked = np.argmin(np.abs(clicked_coord.separation(MAGcoords).to(u.deg).value))
        print(MAGclicked,MAGNAMES[MAGclicked])

        playsound("wavs/" + MAGNAMES[MAGclicked] + "_sound" + wavtype + ".wav")
    elif np.any(np.abs(clicked_coord.separation(PSRcoords[0]).to(u.deg).value) < vicinity):
        PSRclicked = np.argmin(np.abs(clicked_coord.separation(PSRcoords[0]).to(u.deg).value))
        print(PSRclicked,PSRNAMES[0][PSRclicked])

        playsound("wavs/" + PSRNAMES[0][PSRclicked] + "_sound" + wavtype + ".wav")
    elif np.any(np.abs(clicked_coord.separation(PSRcoords[1]).to(u.deg).value) < vicinity):
        PSRclicked = np.argmin(np.abs(clicked_coord.separation(PSRcoords[1]).to(u.deg).value))
        print(PSRclicked,PSRNAMES[1][PSRclicked])

        playsound("wavs/" + PSRNAMES[1][PSRclicked] + "_sound" + wavtype + ".wav")
    print(event.xdata,event.ydata)
    print(wcs.pixel_to_world(event.xdata,event.ydata))	

allobjects = []
alltexts = []
def onmotion(event,wcs,ax):
    #see if clicked near FRB
    if event.inaxes:
        global allobjects

        for obj in allobjects:
            obj.pop(0).remove()
        allobjects = []
        global alltexts
        for i in range(len(alltexts)):
            alltexts[i].remove()#del plt.gca().texts[i]
        alltexts = []
        
        plt.draw()	


        clicked_coord = wcs.pixel_to_world(event.xdata,event.ydata)
        if np.any(np.abs(clicked_coord.separation(FRB_COORDS).to(u.deg).value) < vicinity):
            FRBclicked = np.argmin(np.abs(clicked_coord.separation(FRB_COORDS).to(u.deg).value))
            print(FRBclicked,FRBs[FRBclicked])

            #change color
            allobjects.append(plt.plot(FRB_LON[FRBclicked],FRB_LAT[FRBclicked],'*',markersize=20,color='purple',markeredgecolor='black',transform=ax.get_transform('world'),zorder=1000))
            alltexts.append(plt.text(FRB_LON[FRBclicked]-5,FRB_LAT[FRBclicked],"FRB " + FRBs[FRBclicked],color='purple',weight='bold',transform=ax.get_transform('world'),backgroundcolor='white',zorder=100))
            plt.draw()
        elif np.any(np.abs(clicked_coord.separation(otherFRBcoords).to(u.deg).value) < vicinity):
            FRBclicked = np.argmin(np.abs(clicked_coord.separation(otherFRBcoords).to(u.deg).value))
            print(FRBclicked,otherFRBNAMES[FRBclicked])

            #change color
            allobjects.append(plt.plot(otherFRBLONS[FRBclicked],otherFRBLATS[FRBclicked],'*',markersize=20,color='purple',markeredgecolor='black',transform=ax.get_transform('world'),zorder=1000))
            alltexts.append(plt.text(otherFRBLONS[FRBclicked]-5,otherFRBLATS[FRBclicked],otherFRBNAMES[FRBclicked],color='purple',weight='bold',transform=ax.get_transform('world'),backgroundcolor='white',zorder=100))
            plt.draw()
        elif np.any(np.abs(clicked_coord.separation(MAGcoords).to(u.deg).value) < vicinity):
            MAGclicked = np.argmin(np.abs(clicked_coord.separation(MAGcoords).to(u.deg).value))
            print(MAGclicked,MAGNAMES[MAGclicked])

            #change color
            print(MAGLONS[MAGclicked],MAGLATS[MAGclicked])
            allobjects.append(plt.plot(MAGLONS[MAGclicked],MAGLATS[MAGclicked],'v',markersize=10,color='purple',markeredgecolor='black',transform=ax.get_transform('world'),zorder=1000))
            alltexts.append(plt.text(MAGLONS[MAGclicked]-5,MAGLATS[MAGclicked],MAGNAMES[MAGclicked],color='purple',weight='bold',transform=ax.get_transform('world'),backgroundcolor='white',zorder=100))
            plt.draw()
        elif np.any(np.abs(clicked_coord.separation(PSRcoords[0]).to(u.deg).value) < vicinity):
            PSRclicked = np.argmin(np.abs(clicked_coord.separation(PSRcoords[0]).to(u.deg).value))
            print(PSRclicked,PSRNAMES[0][PSRclicked])

            #change color
            allobjects.append(plt.plot(PSRLONS[0][PSRclicked],PSRLATS[0][PSRclicked],'o',markersize=10,color='purple',markeredgecolor='black',transform=ax.get_transform('world'),zorder=1000))
            alltexts.append(plt.text(PSRLONS[0][PSRclicked]-5,PSRLATS[0][PSRclicked],"PSR " + PSRNAMES[0][PSRclicked],color='purple',weight='bold',transform=ax.get_transform('world'),backgroundcolor='white',zorder=100))
            plt.draw()
        elif np.any(np.abs(clicked_coord.separation(PSRcoords[1]).to(u.deg).value) < vicinity):
            PSRclicked = np.argmin(np.abs(clicked_coord.separation(PSRcoords[1]).to(u.deg).value))
            print(PSRclicked,PSRNAMES[1][PSRclicked])

            #change color
            allobjects.append(plt.plot(PSRLONS[1][PSRclicked],PSRLATS[1][PSRclicked],'o',markersize=10,color='purple',markeredgecolor='black',transform=ax.get_transform('world'),zorder=1000))
            alltexts.append(plt.text(PSRLONS[1][PSRclicked]-5,PSRLATS[1][PSRclicked],"PSR " + PSRNAMES[1][PSRclicked],color='purple',weight='bold',transform=ax.get_transform('world'),backgroundcolor='white',zorder=100))


            plt.draw()



fig=plt.figure(figsize=(12,6))

#overlay with fits sky image
f = fits.open("./data/cutout-CDS_P_2MASS_J.fits")
wcs = WCS(f[0].header)
plt.subplot(projection=wcs)
plt.imshow(np.log10(f[0].data - np.nanmin(f[0].data) + 1),aspect='auto',cmap='bone',vmin=0.3,vmax=1)
ax = plt.gca()
plt.plot(FRB_LON,FRB_LAT,'*',markersize=20,color='pink',markeredgecolor='black',transform=ax.get_transform('world'),label='DSA-110 FRBs',zorder=0)
plt.plot(otherFRBcoords.galactic.l.value,otherFRBcoords.galactic.b.value,'*',markersize=20,color='palegreen',markeredgecolor='black',transform=ax.get_transform('world'),label='Other FRBs',zorder=0)
plt.plot(np.concatenate([PSRLONS[0],PSRLONS[1]]),np.concatenate([PSRLATS[0],PSRLATS[1]]),'o',markersize=10,color='gold',markeredgecolor='black',transform=ax.get_transform('world'),label='Pulsars',zorder=0)
plt.plot(MAGLONS,MAGLATS,'v',markersize=10,color='cornflowerblue',markeredgecolor='black',transform=ax.get_transform('world'),label='Magnetars',zorder=0)
plt.xticks([])
plt.yticks([])
plt.ylabel("")
plt.xlabel("")
plt.legend(loc='upper right',frameon=True)
fig.canvas.mpl_connect('button_press_event',lambda event: onclick(event,wcs))
fig.canvas.mpl_connect('motion_notify_event',lambda event: onmotion(event,wcs,ax))

#buttons for just linear/circular pol
rax = plt.axes([0.05, 0.05, 0.1, 0.2])
radio = RadioButtons(rax, ['Full', 'Intensity', 'Linear', 'Circular'],0)
radio_labels =  ['Full', 'Intensity', 'Linear', 'Circular']
def pick(labels):
    global wavtype
    wavtype=wavtypes[labels]
    print(labels,wavtype)
    plt.draw()
radio.on_clicked(pick)

plt.show()
