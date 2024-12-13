def SkaterScrape(season):
    import pandas as pd

    print("Beginning scrape of Natural Stat Trick skater data for the "+season[:4]+"-"+season[4:]+" NHL season...\n")  

    indvret = "https://www.naturalstattrick.com/playerteams.php?fromseason="+season+"&thruseason="+season+"&stype=2&sit=5v5&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=multi&draftteam=ALL"
    oniceret = "https://www.naturalstattrick.com/playerteams.php?fromseason="+season+"&thruseason="+season+"&stype=2&sit=5v5&score=all&stdoi=oi&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=multi&draftteam=ALL"
    allindvret = "https://www.naturalstattrick.com/playerteams.php?fromseason="+season+"&thruseason="+season+"&stype=2&sit=all&score=all&stdoi=std&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=multi&draftteam=ALL"
    biosret = "https://www.naturalstattrick.com/playerteams.php?fromseason="+season+"&thruseason="+season+"&stype=2&sit=all&score=all&stdoi=bio&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=multi&draftteam=ALL"

    dfindv = pd.read_html(indvret, header=0, index_col = 0, na_values=["-"])[0]
    dfindv.head()

    dfonice = pd.read_html(oniceret, header=0, index_col = 0, na_values=["-"])[0]
    dfonice.head()

    dfallindv = pd.read_html(allindvret, header=0, index_col = 0, na_values=["-"])[0]
    dfallindv.head()

    bios = pd.read_html(biosret, header=0, index_col = 0, na_values=["-"])[0]
    bios.head()

    dfindv.sort_values(by=['Player'],inplace=True)
    dfonice.sort_values(by=['Player'],inplace=True)
    dfallindv.sort_values(by=['Player'],inplace=True)
    bios.sort_values(by=['Player'],inplace=True)

    dfindv['iFsh%'] = (dfindv['Goals'])/((dfindv['iFF'])) 
    dfindv['ixG/iFF'] = (dfindv['ixG'])/((dfindv['iFF']))
    dfindv['G/ixG'] = (dfindv['Goals'])/((dfindv['ixG']))

    dfindv["G"] = dfindv["Goals"]
    dfindv["G 5v5"] = ((dfindv["Goals"]))
    dfindv["A1 5v5"] = ((dfindv["First Assists"]))
    dfindv["A2 5v5"] = ((dfindv["Second Assists"]))

    dfonice['FshF%'] = (dfonice['GF'])/((dfonice['FF'])) 
    dfonice['xGF/FF'] = (dfonice['xGF'])/((dfonice['FF']))
    dfonice['GF/xGF'] = (dfonice['GF'])/((dfonice['xGF']))
    dfonice['FshA%'] = (dfonice['GA'])/((dfonice['FA'])) 
    dfonice['xGA/FA'] = (dfonice['xGA'])/((dfonice['FA']))
    dfonice['GA/xGA'] = (dfonice['GA'])/((dfonice['xGA']))

    dfallindv['G All'] =  ((dfallindv["Goals"]))
    dfallindv['A1 All'] =  ((dfallindv["First Assists"]))
    dfallindv['A2 All'] =  ((dfallindv["Second Assists"]))

    s = []

    for i in range(0,len(dfindv["Player"])):
        s.append(season[2:-4]+"-"+season[6:])

    year = pd.Series(s)
    dfindv["Season"] = year
    dfindv["ID"] = dfindv['Player']+year+dfindv['Team']
    dfindv['Player'] = dfindv['Player'].str.replace('è', 'e', regex=True)

    df = pd.concat([dfindv["Player"],dfindv['Season'],dfindv['Team'],dfindv['Position'],dfindv['ID'],dfindv['GP'],dfindv['TOI'],dfindv['G'],dfindv['iFF'],dfindv['ixG'],dfindv['ixG/iFF'],dfindv['G/ixG'],dfindv['iFsh%'],dfonice['GF'],dfonice['xGF'],dfonice['FF'],dfonice['FshF%'],dfonice['xGF/FF'],dfonice['GF/xGF'],dfonice['GA'],dfonice['xGA'],dfonice['FA'],dfonice['FshA%'],dfonice['xGA/FA'],dfonice['GA/xGA'],dfindv['G 5v5'],dfindv['A1 5v5'],dfindv['A2 5v5'],dfallindv['G All'],dfallindv['A1 All'],dfallindv['A2 All']],axis=1)

    print("Finished scrape of Natural Stat Trick skater data for the "+season[:4]+"-"+season[4:]+" NHL season.\n")

    return df

def BioScrape(season):
    import pandas as pd
    
    biosret = "https://www.naturalstattrick.com/playerteams.php?fromseason="+season+"&thruseason="+season+"&stype=2&sit=all&score=all&stdoi=bio&rate=n&team=ALL&pos=S&loc=B&toi=0&gpfilt=none&fd=&td=&tgp=410&lines=multi&draftteam=ALL"
    bios = pd.read_html(biosret, header=0, index_col = 0, na_values=["-"])[0]
    bios.head()
    bios.sort_values(by=['Player'],inplace=True)

    s = []

    for i in range(0,len(bios["Player"])):
        s.append(season[2:-4]+"-"+season[6:])

    year = pd.Series(s)
    bios["Season"] = year
    bios["ID"] = bios['Player']+year+bios['Team']
    bios['Player'] = bios['Player'].str.replace('è', 'e', regex=True)

    df = pd.concat([bios['Player'],bios['Season'],bios['Team'],bios['Position'],bios['ID'],bios[bios.columns[3:15]]],axis=1)

    return df

def TeamScrape(season):
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup as bs
    import numpy as np
    import statistics
    import os
    print("Beginning scrape of Natural Stat Trick team data for the "+season[:4]+"-"+season[4:]+" NHL season...\n")  

    ret = "https://www.naturalstattrick.com/teamtable.php?fromseason="+season+"&thruseason="+season+"&stype=2&sit=5v5&score=all&rate=n&team=all&loc=B&gpf=410&fd=&td="

    df = pd.read_html(ret, header=0, index_col = 0, na_values=["-"])[0]
    df.head()

    df.sort_values(by=['Team'],inplace=True)

    team = list(df['Team'])
    wins = list(df['W'])
    losses = list(df['L'])
    otl = list(df['OTL'])
    points = list(df['Points'])
    gp = list(df['GP'])
    toi = list(df['TOI'])
    gf = list(df['GF'])
    ga = list(df['GA'])
    ff = list(df['FF'])
    fa = list(df['FA'])
    xgf = list(df['xGF'])
    xga = list(df['xGA'])

    s = []
    record = []

    for i in range (0, len(team)):
        s.append(season[2:-4]+"-"+season[6:])
        record.append(str(wins[i])+"-"+str(losses[i])+"-"+str(otl[i]))
        print("Adding Entry: "+team[i]+" in "+season[2:-4]+"-"+season[6:])

    comp = pd.DataFrame(np.column_stack([team,s,record,points,gp,toi,gf,ga,ff,fa,xgf,xga]),
    columns=["Team","Season","Record","Points","GP","TOI 5v5","GF 5v5","GA 5v5","FF 5v5","FA 5v5","xGF 5v5","xGA 5v5"])

    comp.sort_values(by=['Team'])

    print("Natural Stat Trick team data scraping for the "+season[:4]+"-"+season[4:]+" NHL season has been completed.\n")

    return comp