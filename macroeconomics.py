#fetch economic research
from fredapi import Fred

api_key = 'fb88f90f5fc4526e3df86df73873a487'
fred = Fred(api_key)

def calculate_extrapolation2(data):
    sz = data.size
    y3 = data[sz-1]
    y2 = data[sz-2]
    y1 = data[sz-3]
    y0 = data[sz-4]
    c0 = y0
    c3 = (y3-3*y2+3*y1-y0)/6
    c2 = (-y3+4*y2-5*y1+2*y0)/2
    c1 = y1 - c3 - c2 - c0
    #print(data)
    #print(c0)
    #print(c0+c1+c2+c3)
    #print(c0+2*c1+4*c2+8*c3)
    #print(c0+3*c1+9*c2+27*c3)
    result = []
    result.append(c0)
    result.append(c1)
    result.append(c2)
    result.append(c3)
    return c0+4*c1+16*c2+64*c3

def calculate_extrapolation(data):
    sz = data.size
    sz = min(sz, 5)
    last = data[sz-1]
    diff = 0
    r = 1
    sumr = 0
    dist = 1
    for i in range(sz-1):
        sumr += r
        diff += r * (last - data[sz-2-i]) / dist
        r *= 0.5
        dist += 1
    diff = diff / sumr
    return last + diff

def economic_trend():
    result = []
    #test code
    gdp_data=fred.get_series('GDP')
    nonfarm_data = fred.get_series('PAYEMS')
    tbond_data = fred.get_series('GS10')
    #nonfarm data is monthly
    #gdp data is quaterly   
    print("Non-Farm data prediction....")
    #print(nonfarm_data.tail(4))
    nonfarm_data = nonfarm_data.tail(4)
    nonfarm_data = nonfarm_data.to_numpy()
    pred = calculate_extrapolation(nonfarm_data)
    #print(pred)
    #print(nonfarm_data[-1])
    #print((pred-nonfarm_data[-1]))
    #print((pred-nonfarm_data[-1])/nonfarm_data[-1])
    nonfarm_ratio = (pred-nonfarm_data[-1])/nonfarm_data[-1]*100
    result.append(nonfarm_ratio)
    #
    print("GDP data prediction....")
    #print(gdp_data.tail(4))
    gdp_data = gdp_data.tail(4)
    gdp_data = gdp_data.to_numpy()
    pred = calculate_extrapolation(gdp_data)
    #print(pred)
    gdp_ratio = (pred-gdp_data[-1])/gdp_data[-1]*100
    result.append(gdp_ratio)
    #
    print("Treasury Bonds data prediction....")
    #print(tbond_data.tail(4))
    tbond_data = tbond_data.tail()
    tbond_data = tbond_data.to_numpy()
    pred = calculate_extrapolation(tbond_data)
    #print(pred)
    tbond_ratio = (pred-tbond_data[-1])/tbond_data[-1]*100
    result.append(tbond_ratio)
    return result


