# code from https://github.com/mswerli/zillow_data
#get median price per zipcode
import requests
import pandas as pd
from xml.etree import ElementTree
import xmltodict
from bs4 import BeautifulSoup
import numpy as np
import urllib
import utils
import datetime
import csv
import os.path
from config import Zillow_API_key
#os.path.isfile(fname)

##User specific ID used for IDing requests
zws_id = 'X1-ZWz183nrq3tjwr_a9fju'

def getRegionChildren(state,county,city,childtype):

    search_params = {
        "city": city,
        "state": state,
        "childtype": childtype,
        'county': county,
        "zws_id": Zillow_API_key
    }

    region_tags =  (('id'),
              ('name'),
              ('zindex'),
              ('latitude'),
              ('longitude'))
    
    region_cols = ['id', 'name','zindex','latitude', 'longitude']

    ##Get starting home data##
    r = utils.get_response(api = 'regionChildren', params = search_params)

    home = utils.parse_response(response = r,
                                api = 'regionChildren',
                                tags = region_tags,
                                cols = region_cols)

    #print(home)
    return home




df = getRegionChildren(state="CA",county="San Diego",city="",childtype="zipcode")
#print (df)

df.to_csv("datasets/median_price_SDcounty.csv",header=True, index=False)