"""
These tcra rep, rep_EPN, recovery_monte_carlo_simulation functions calculate estimated repair times 
and Monte Carlo simulation for recovery process.

"""
def rep(data):
    """ 
    this function estimates repair time (days) given damage level of buildings. params need to adjusted for local building types.
    0: none, 1: slight, 2: moderate, 3: extensive, 4: complete
    
    Parameters
    ----------
    data : 
        building invetory with damage states and occupancy type
        
    dmg : 
        building damage state
       
    Occupancy : 
        building occupancy type based on HAZUS classification

    Returns
    -------
    recovery :
        recovery time
        
    """
    params = {
        'RES1': {4: 720, 3: 360, 2: 120, 1: 5, 0: 0},
        'RES2': {4: 240, 3: 120, 2: 20, 1: 5, 0: 0},
        'RES3': {4: 960, 3: 480, 2: 120, 1: 10, 0: 0},
        'RES4': {4: 480, 3: 360, 2: 90, 1: 10, 0: 0},
        'RES5': {4: 480, 3: 360, 2: 90, 1: 10, 0: 0},
        'RES6': {4: 960, 3: 480, 2: 120, 1: 10, 0: 0},
        'COM1': {4: 360, 3: 270, 2: 90, 1: 10, 0: 0},
        'COM2': {4: 360, 3: 270, 2: 90, 1: 10, 0: 0},
        'COM3': {4: 360, 3: 270, 2: 90, 1: 10, 0: 0},
        'COM4': {4: 480, 3: 360, 2: 90, 1: 20, 0: 0},
        'COM5': {4: 360, 3: 180, 2: 90, 1: 20, 0: 0},
        'COM6': {4: 720, 3: 540, 2: 135, 1: 20, 0: 0},
        'COM7': {4: 540, 3: 270, 2: 135, 1: 20, 0: 0},
        'COM8': {4: 360, 3: 180, 2: 90, 1: 20, 0: 0},
        'COM9': {4: 360, 3: 180, 2: 90, 1: 20, 0: 0},
        'COM10': {4: 360, 3: 180, 2: 60, 1: 5, 0: 0},
        'IND1': {4: 360, 3: 240, 2: 90, 1: 10, 0: 0},
        'IND2': {4: 360, 3: 240, 2: 90, 1: 10, 0: 0},
        'IND3': {4: 360, 3: 240, 2: 90, 1: 10, 0: 0},
        'IND4': {4: 360, 3: 240, 2: 90, 1: 10, 0: 0},
        'IND5': {4: 540, 3: 360, 2: 135, 1: 20, 0: 0},
        'IND6': {4: 320, 3: 160, 2: 60, 1: 10, 0: 0},
        'AGR1': {4: 120, 3: 60, 2: 20, 1: 2, 0: 0},
        'REL1': {4: 960, 3: 480, 2: 120, 1: 5, 0: 0},
        'GOV1': {4: 480, 3: 360, 2: 90, 1: 10, 0: 0},
        'GOV2': {4: 360, 3: 270, 2: 60, 1: 10, 0: 0},
        'EDU1': {4: 480, 3: 360, 2: 90, 1: 10, 0: 0},
        'EDU2': {4: 960, 3: 480, 2: 120, 1: 10, 0: 0},
    }


    recovery = []
    for _, row in data.iterrows():
        mean_val = params.get(row['Occupancy'], {}).get(row['dmg'], 0)
        f1 = np.random.normal(mean_val, 0.3 * mean_val) if mean_val > 0 else 0
        recovery.append(f1)
        
    return recovery

def recovery_monte_carlo_simulation(data, num_simulations):
    """ 
    this function simulate Monte Carlo process of recovery of buildings given damage level.
    
    Parameters
    ----------
    data : 
        building invetory with damage states and occupancy type

    num_simulations : 
        number of simulaitons.
    dmg : 
        building damage state
       
    Occupancy : 
        building occupancy type based on HAZUS classification

    Returns
    -------
    tt :
        recovery time in days
    all_simulations :
        recovery time from all Monte Carlo sampling
    mean_simulation :
        mean recovery time from all sampling
    min_simulation :
        minimum recovery time from all sampling
    max_simulation :
        maximum recovery time from all sampling
    
    """
    
    all_simulations = []

    for _ in range(num_simulations):
        recovery_time = rep(data)
        data['RT_bdg'] = list(recovery_time)

        bb = []
        tt = list(range(0, 1000, 5))
        for T in tt:
            bb.append(data[data.RT_bdg < T].shape[0])

        all_simulations.append(pd.Series(bb)*100/data.shape[0])

    # Convert to numpy array for easy averaging
    all_simulations = np.array(all_simulations)
    mean_simulation = np.mean(all_simulations, axis=0)
    min_simulation = np.min(all_simulations, axis=0)
    max_simulation = np.max(all_simulations, axis=0)

    return tt, all_simulations, mean_simulation, min_simulation, max_simulation


def rep_EPN(data):
    """ this function estimates repair time (days) for damage electrical poles. parameters need to be adjusted as required.
    0: non failure, 1: failure
    
    Parameters
    ----------
    data : 
        epn invetory
    dmg_pole :
        electrical pole damage state
    params :
        a dictionary provides expected recovery time for recovery time for damaged electrical poles.

    Returns
    -------
    recovery : 
        recovery time in days
        
    """

    params = {
        1: 10,
        0: 0,
    }

    recovery = []
    for _, row in data.iterrows():
        mean_val = params.get(row['dmg_pole'])
        f1 = np.random.normal(mean_val, 0.3 * mean_val) if mean_val > 0 else 0
        recovery.append(f1)
    
    return recovery
