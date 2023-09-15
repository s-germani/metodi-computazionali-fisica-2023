import numpy as np
import pandas as pd



ifiles = ['4FGL_J0428.6-3756_weekly_9_15_2023.csv',
          '4FGL_J0721.9+7120_weekly_9_15_2023.csv',
          '4FGL_J1256.1-0547_weekly_9_15_2023.csv',
          '4FGL_J2202.7+4216_weekly_9_15_2023.csv',
          '4FGL_J2232.6+1143_weekly_9_15_2023.csv',
          '4FGL_J2253.9+1609_weekly_9_15_2023.csv' ]


ofiles = ['4FGL_J0428.6-3756_weekly_9_15_2023_mcf.csv',
          '4FGL_J0721.9+7120_weekly_9_15_2023_mcf.csv',
          '4FGL_J1256.1-0547_weekly_9_15_2023_mcf.csv',
          '4FGL_J2202.7+4216_weekly_9_15_2023_mcf.csv',
          '4FGL_J2232.6+1143_weekly_9_15_2023_mcf.csv',
          '4FGL_J2253.9+1609_weekly_9_15_2023_mcf.csv' ]



#"Date(UTC)","Julian Date","MET","TS","Photon Flux [0.1-100 GeV](photons cm-2 s-1)","Photon Flux Error(photons cm-2 s-1)","Photon Index","Photon Index Error","Sun Distance","Fit Tolerance","MINUIT Return Code","Analysis Log"


for csvi,csvo in zip(ifiles,ofiles):

    df1 = pd.read_csv(csvi)

    #print(df1)
    #print(df1.dtypes)

    df1c = df1.copy()
    df1c.drop( columns=["MET","Photon Index","Photon Index Error","Sun Distance","Fit Tolerance","MINUIT Return Code","Analysis Log"], inplace=True )



    mask = df1c['Photon Flux Error(photons cm-2 s-1)']==0
    cv   = df1c.loc[mask, 'Photon Flux [0.1-100 GeV](photons cm-2 s-1)']/2
    #print(cv)
    #print(mask)

    df1c.loc[mask, 'Photon Flux Error(photons cm-2 s-1)'] = cv

    #print(df1c)
    df1c.to_csv(csvo, index=False)

