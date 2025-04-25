def calculate_precipitation_proportion(group):
    # Check if the total precipitation is greater than 0
    total_precip = group.pr_crop.sum()
    if total_precip > 0:
        # Calculate the sum of precipitation exceeding the reference
        exceeding_precip = group.pr_crop[group.pr_crop > group.refer].sum()
        # Return the proportion
        return exceeding_precip / total_precip
    else:
        return 0
def degreedays(data, b):
    # Calculate bins for tasmax and tasmin
    bins1 = np.digitize(data['tasmax'], bins=[b])
    bins2 = np.digitize(data['tasmin'], bins=[b])
    bin = bins1 + bins2

    # Create a new DataFrame for the degree day calculations
    dday_col = 'dday' + str(b)
    result = pd.DataFrame(index=data.index)  # Create an empty DataFrame with the same index as the input data
    result[dday_col] = 0.0  # Initialize with zeros and explicitly set the column dtype to float

    # For rows where bin == 2, calculate degree days as tAvg - b
    result.loc[bin == 2, dday_col] = data.loc[bin == 2, 'tAvg'].copy() - b

    # For rows where bin == 1, calculate using arccos and sin formula
    mask = (bin == 1)
    tasmax = data.loc[mask, 'tasmax'].copy()
    tasmin = data.loc[mask, 'tasmin'].copy()
    tAvg = data.loc[mask, 'tAvg'].copy()
    arccos_input = (2 * b - tasmax - tasmin) / (tasmax - tasmin)
    arccos_clipped = np.clip(arccos_input,-1,1)

    temp= np.arccos(arccos_clipped)

    result.loc[mask, dday_col] = ((tAvg - b) * temp + (tasmax - tasmin) * np.sin(temp) / 2) / math.pi

    return result

def freezedegreedays(data, b):
    # Calculate bins for tMax and tMin
    bins1 = np.digitize(data['tasmax'], bins=[b])
    bins2 = np.digitize(data['tasmin'], bins=[b])
    bin = bins1 + bins2

    # Create a new DataFrame for the freeze degree day calculations
    fdday_col = 'fdday' + str(b)
    result = pd.DataFrame(index=data.index)  # Create an empty DataFrame with the same index as the input data
    result[fdday_col] = 0.0  # Initialize with zeros and explicitly set the column dtype to float

    # For rows where bin == 0, calculate freeze degree days as b - tAvg
    result.loc[bin == 0, fdday_col] = b - data.loc[bin == 0, 'tAvg'].copy()

    # For rows where bin == 2, freeze degree days is 0
    result.loc[bin == 2, fdday_col] = 0

    # For rows where bin == 1, calculate using the arcsin and cos formula
    mask = (bin == 1)
    tMax = data.loc[mask, 'tasmax'].copy()
    tMin = data.loc[mask, 'tasmin'].copy()
    tAvg = data.loc[mask, 'tAvg'].copy()

    temp = np.arcsin((2 * b - tMax - tMin) / (tMax - tMin))
    result.loc[mask, fdday_col] = ((b - tAvg) * (temp + math.pi / 2) + (tMax - tMin) * np.cos(temp) / 2) / math.pi

    return result[fdday_col]

def get_days_in_year(year):
    return 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365

def u(z, ind, tMin, tMax):
    x= ((z[ind]- tMin[ind])/(tMax[ind]-tMin[ind])).round(6)
    return(x)

#t0 t1 is the lower bound and upper bound of bin
def DaysinRange(t0, t1, data):
    tMin = data.tasmin.reset_index(drop=True)
    tMax = data.tasmax.reset_index(drop=True)
    n = len(tMin)

    # Initialize a DataFrame with tMin and tMax values equal to t0 and t1
    tnew = pd.DataFrame({'tMin': [t0] * n, 'tMax': [t1] * n})

    # Adjust tMin where it's smaller than tasmin
    tnew.loc[tnew.tMin < tMin, 'tMin'] = tMin[tnew.tMin < tMin]

    # Adjust tMax where it's larger than tasmax, ensuring conversion to float if necessary
    tMax_filtered = tMax[tnew.tMax > tMax].astype(float)
    tnew.loc[tnew.tMax > tMax, 'tMax'] = tMax_filtered

    # Define outside and inside conditions
    outside = (tnew.tMin > tMax) | (tnew.tMax < tMin)
    inside = ~outside  # The inverse condition of outside

    # Compute the TimeatRange
    TimeatRange = (2 / math.pi) * (
            u(tnew.tMax, inside, tMin, tMax).apply(math.asin) -
            u(tnew.tMin, inside, tMin, tMax).apply(math.asin)
    )

    # Create a result array with NaN values by default, same size as the data
    x = pd.Series(index=data.index, dtype=float)

    inside.reset_index(drop=True, inplace=True)
    x.reset_index(drop=True, inplace=True)

    # Now you can safely assign
    x[inside] = TimeatRange
    # Assign the computed TimeatRange values where 'inside' is True, others remain NaN

    # Rename the series to reflect the mid-point of the range
    x.name = f"BIN_{t0 + 0.5}"

    return x

def getbins(data, nT):
    savebin = pd.DataFrame()
    for k in nT:
        Tvect = DaysinRange(k - 0.5, k + 0.5, data)
        savebin[Tvect.name] = Tvect
    return (savebin)

