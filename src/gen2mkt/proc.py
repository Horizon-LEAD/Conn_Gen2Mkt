"""Processing module
"""

import json
from os.path import join
from time import time
from logging import getLogger

import pandas as pd
import numpy as np

from .utils import read_shape, read_mtx

logger = getLogger("gen2mkt.proc")

def run_model(cfg):
    start_time = time()

    outdir = cfg['OUTDIR']
    label  = cfg['LABEL']

    logger.info('Importing data...')

    zones = read_shape(cfg['ZONES'])
    zones.index = zones['AREANR']
    nZones = len(zones)
    
    # To be deleted
    skims = {'time': {}, 'dist': {}, }
    skims['time']['path'] = cfg['SKIMTIME']
    skims['dist']['path'] = cfg['SKIMDISTANCE']
    for skim in skims:
        skims[skim] = read_mtx(skims[skim]['path'])
        nSkimZones = int(len(skims[skim])**0.5)
        skims[skim] = skims[skim].reshape((nSkimZones, nSkimZones))
        if skim == 'time': skims[skim][6483] = skims[skim][:,6483] = 5000 # data deficiency
        for i in range(nSkimZones): #add traveltimes to internal zonal trips
            skims[skim][i,i] = 0.7 * np.min(skims[skim][i,skims[skim][i,:]>0])
    skimTravTime = skims['time']; skimDist = skims['dist']
    skimDist_flat = skimDist.flatten()
    del skims, skim, i

    zoneDict  = dict(np.transpose(np.vstack( (np.arange(1,nZones+1), zones['AREANR']) )))
    zoneDict  = {int(a):int(b) for a,b in zoneDict.items()}
    invZoneDict = dict((v, k) for k, v in zoneDict.items()) 

    segs   = pd.read_csv(cfg['SEGS'])
    segs.index = segs['zone']
    segs = segs[segs['zone'].isin(zones['AREANR'])] #Take only segs into account for which zonal data is known as well

    parcelNodes = read_shape(cfg['PARCELNODES'], returnGeometry=False)
    parcelNodes.index = parcelNodes['id'].astype(int)
    parcelNodes = parcelNodes.sort_index()  

    for node in parcelNodes['id']:
        parcelNodes.loc[node,'SKIMNR'] = int(invZoneDict[parcelNodes.at[int(node),'AREANR']])
    parcelNodes['SKIMNR'] = parcelNodes['SKIMNR'].astype(int)

    cepList   = np.unique(parcelNodes['CEP'])
    cepNodes = [np.where(parcelNodes['CEP']==str(cep))[0] for cep in cepList]
    
    # Keep only cepNodeDict and the last for loop
    cepNodeDict = {}; cepZoneDict = {}; cepSkimDict = {}
    for cep in cepList: 
        cepZoneDict[cep] = parcelNodes[parcelNodes['CEP'] == cep]['AREANR'].astype(int).tolist()
        cepSkimDict[cep] = parcelNodes[parcelNodes['CEP'] == cep]['SKIMNR'].astype(int).tolist()
    for cepNo in range(len(cepList)):
        cepNodeDict[cepList[cepNo]] = cepNodes[cepNo]

    parcels = pd.read_csv(cfg['PARCELS'])
    parcels.index = parcels['Parcel_ID']
    parcels['Segment'] = np.where(np.random.uniform(0,1,len(parcels)) < (cfg['PARCELS_PER_HH_C2C']/cfg['PARCELS_PER_HH']), 'C2C', 'B2C')

    parcels['L2L'] = np.random.uniform(0,1,len(parcels)) < cfg['Local2Local'] #make certain percentage L2L
    parcels['CS_eligible'] = np.random.uniform(0,1,len(parcels)) < cfg['CS_cust_willingness'] # make certain percentage CS eligible. This eligibility is A PRIORI, depending on parcel/sender/receiver characteristics. Inside the crowdshipping part we might want to adjust that according to a choice model
    parcels['CS_eligible'] = (parcels['CS_eligible'] & parcels['L2L'] ) # This means that the CS parcels are only L2L and the percentage above is the % of the L2L parcels that can be crowdshipped
    parcels_hyperconnected = parcels[parcels['L2L'] | parcels['CS_eligible']   ]

    Gemeenten = cfg['Gemeenten_studyarea']

    if len(Gemeenten) > 1:
        ParceltobeL2L = pd.DataFrame(columns = parcels_hyperconnected.columns)
    
        for Geemente in Gemeenten:
            if type (Geemente) != list: # If there the cities are NOT connected (that is every geemente is separated from the next)
                ParcelTemp = parcels_hyperconnected[parcels_hyperconnected['D_zone'].isin(zones['AREANR'][zones['GEMEENTEN']==Geemente])]
                origin_distribution = segs['1: woningen']/segs['1: woningen'].sum() #create distribution to number of houses
                ParcelTemp['O_zone'] = np.random.choice(segs['zone'], p=(origin_distribution), size=(len(ParcelTemp))) 
                segs_local = segs[segs['zone'].isin(zones['AREANR'][zones['GEMEENTEN']==Geemente])] #only consider SEGS in study area for L2L
                L2L_distribution = segs_local['1: woningen']/segs_local['1: woningen'].sum() #create distribution to number of houses in area
                ParcelTemp.loc[ParcelTemp['L2L'] == True,'O_zone'] = np.random.choice(segs_local['zone'], p=(L2L_distribution), size=( ParcelTemp['L2L'].value_counts()[True] )) #assign origin based on local distribution if parcel is L2L
                ParceltobeL2L = ParceltobeL2L.append(ParcelTemp)
            else:
                ParcelTemp = parcels_hyperconnected[parcels_hyperconnected['D_zone'].isin(zones['AREANR'][zones['GEMEENTEN'].isin(Geemente)])]
                origin_distribution = segs['1: woningen']/segs['1: woningen'].sum() #create distribution to number of houses
                ParcelTemp['O_zone'] = np.random.choice(segs['zone'], p=(origin_distribution), size=(len(ParcelTemp))) 
                segs_local = segs[segs['zone'].isin(zones['AREANR'][zones['GEMEENTEN'].isin(Geemente)])]#only consider SEGS in study area for L2L
                L2L_distribution = segs_local['1: woningen']/segs_local['1: woningen'].sum() #create distribution to number of houses in area
                ParcelTemp.loc[ParcelTemp['L2L'] == True,'O_zone'] = np.random.choice(segs_local['zone'], p=(L2L_distribution), size=( ParcelTemp['L2L'].value_counts()[True] )) #assign origin based on local distribution if parcel is L2L
                ParceltobeL2L = ParceltobeL2L.append(ParcelTemp) 
        
        parcels_hyperconnected = ParceltobeL2L
    else:
        # Replace if else with the commented out line of code
        if type (Gemeenten[0]) == list:
            Geemente = Gemeenten [0]
        else:
            Geemente = Gemeenten
        # Geemente = Gemeenten [0] if  type (Gemeenten[0]) == list else Gemeenten
        parcels_hyperconnected = parcels_hyperconnected[parcels_hyperconnected['D_zone'].isin(zones['AREANR'][zones['GEMEENTEN'].isin(Geemente)])] #filter the parcels to study area
        origin_distribution = segs['1: woningen']/segs['1: woningen'].sum() #create distribution to number of houses
        parcels_hyperconnected['O_zone'] = np.random.choice(segs['zone'], p=(origin_distribution), size=(len(parcels_hyperconnected))) #assign origin based on distribution  
        segs_local = segs[segs['zone'].isin(zones['AREANR'][zones['GEMEENTEN'].isin(Geemente)])] #only consider SEGS in study area for L2L
        L2L_distribution = segs_local['1: woningen']/segs_local['1: woningen'].sum() #create distribution to number of houses in area
        parcels_hyperconnected.loc[parcels_hyperconnected['L2L'] == True,'O_zone'] = np.random.choice(segs_local['zone'], p=(L2L_distribution), size=( parcels_hyperconnected['L2L'].value_counts()[True] )) #assign origin based on local distribution if parcel is L2L
    
    ParcelLockers =  parcels[(parcels['PL']!=0)]  
    ParcelLockers = ParcelLockers[(parcels['L2L'] == False)]
    ParcelLockers = ParcelLockers[(parcels['CS_eligible'] == False )]
    
    parcels_hyperconnected = parcels_hyperconnected.append(ParcelLockers)                                               
    parcels_hubspoke = parcels[~(parcels['L2L'] | parcels['CS_eligible'] | parcels['PL'])]
   
    parcels_hyperconnected['Fulfilment']='Hyperconnected'
    parcels_hubspoke['Fulfilment']='Hubspoke'

    Parcels = parcels_hubspoke.append(parcels_hyperconnected)
    Parcels.to_csv(f"{cfg['OUTDIR']}Demand_parcels_fulfilment_{cfg['LABEL']}.csv", index=False)