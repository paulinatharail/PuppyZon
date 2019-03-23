# code from https://github.com/mswerli/zillow_data
import requests
import pandas as pd
from xml.etree import ElementTree
import xmltodict
from bs4 import BeautifulSoup
import numpy as np
import urllib


def get_attribute(api,data,tag):

    print(tag)

    if api == 'comp':

        if type(tag) == str:
            value = pd.DataFrame([dict(data[b][tag]) for b in range(len(data))])
            return value

        if len(tag) == 2:
            value = pd.DataFrame([dict(data[b][tag[0]][tag[1]]) for b in range(len(data))])
            return value

        if len(tag) == 3:
            value = pd.DataFrame([dict(data[b][tag[0]][tag[1]][tag[2]]) for b in range(len(data))])
            return value

    if api == 'search':

        if type(tag) == str:
            value = data[tag]
            return pd.DataFrame(value, index = [0])

        if len(tag) == 2:
            value =  pd.DataFrame(data[tag[0]][tag[1]], index = [0])
            return value

        if len(tag) == 3:
            value = pd.DataFrame(data[tag[0]][tag[1]][tag[2]], index = [0])
            return value

    if api == 'regionChildren':
        if type(tag) == str:
            value = pd.DataFrame([dict(data[b][tag]) for b in range(len(data))])
            return value

        if len(tag) == 2:
            value = pd.DataFrame([dict(data[b][tag[0]][tag[1]]) for b in range(len(data))])
            return value

        if len(tag) == 3:
            value = pd.DataFrame([dict(data[b][tag[0]][tag[1]][tag[2]]) for b in range(len(data))])
            return value


def get_response(api, params):

    print('Starting....')

    if api == 'search':
        print('Search API')

        base_url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
        url = base_url + 'zws-id='+params['zws_id']+'&address='+params['address']+'&citystatezip='+params['citystatezip']

    if api == 'comp':
        base_url = 'http://www.zillow.com/webservice/GetComps.htm?'
        url = base_url  + 'zws-id=' + params['zws_id'] + '&zpid=' + params['zpid'] + '&count=' + params['count']

        print(base_url)
        print(url)
        
    if api == 'regionChildren':
        base_url = 'http://www.zillow.com/webservice/GetRegionChildren.htm?'
        url = base_url  +'zws-id='+params['zws_id']+'&state='+params['state']+'&county='+params['county']+'&city='+params['city']+'&childtype='+params['childtype']

    if api == 'propertyDetails':
        base_url = 'http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm?'
        url = base_url  +'zws-id='+params['zws_id']+'&zpid='+params['zpid']

    print(url)
    r = requests.get(url)

    return r



def parse_response(response, tags, cols, api):

    print('Parsing desired data from response.....')
    zpid = ' '
    if api == 'search':

        cont = xmltodict.parse(response.content.decode('utf-8'))
        cont =  dict(cont.get('SearchResults:searchresults', None)['response']['results']['result'])
        search_dfs = [get_attribute(api = 'search', data = cont, tag = vals) for vals in tags]

        zpid = cont['zpid']

    if api == 'comp':

        cont = xmltodict.parse(response.content.decode('utf-8'))
        keys = cont.get('Comps:comps', None)['response']['properties']['comparables']['comp']
        search_dfs = [get_attribute(api = 'comp', data = keys, tag = vals) for vals in tags]

        ##THIS IS BROKEN--FIX
        zpid = [keys[b]['zpid'] for b in range(len(keys))]
        print(f'zpid: {zpid}')
    
    if api == 'regionChildren':

        cont = xmltodict.parse(response.content.decode('utf-8'))
        keys = cont.get('RegionChildren:regionchildren', None)['response']['list']['region']
        regionData = pd.DataFrame([keys[b]["id"] for b in range(len(keys))], columns=['region_id'])
        regionData['zipcode'] = [keys[b]["name"] for b in range(len(keys))]
        regionData['median'] = [keys[b]['zindex']['#text'] if 'zindex' in keys[b] else 0 for b in range(len(keys))]
        regionData['latitude'] = [keys[b]["latitude"] for b in range(len(keys))]
        regionData['longitude'] = [keys[b]["longitude"] for b in range(len(keys))]
        return regionData

    if api == 'propertyDetails':

        cont = xmltodict.parse(response.content.decode('utf-8'))
        keys = cont.get('UpdatedPropertyDetails:updatedPropertyDetails', None)['response']
        details = {"zpid": keys['zpid']}
        
        details["street"] = keys["address"]["street"]
        details["zipcode"] = keys["address"]["zipcode"]
        details["city"] = keys["address"]["city"]
        details["state"] = keys["address"]["state"]
        details["latitude"] = keys["address"]["latitude"]
        details["longitude"] = keys["address"]["longitude"]

        if ('images' in keys) :
            if (keys["images"]["count"] == "1"):
                details["image"] = keys["images"]["image"]["url"]
            else:
                details["image"] = keys["images"]["image"]["url"][0]
        else:
            details["image"] = None

        keys = cont.get('UpdatedPropertyDetails:updatedPropertyDetails', None)['response']['editedFacts']
        

        for col in cols:
            if (col in keys):
                details[col] = keys[col]
            else:
                details[col] = None

        return details

    print('Combining data frames')

    home_data =  pd.concat(search_dfs, axis = 1)

    print('Setting column names')

    home_data['zpid'] = zpid

    home_data.columns = cols


    return home_data