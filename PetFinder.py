import requests
from requests.auth import HTTPDigestAuth
import json
import time
import pandas as pd
import time
from pprint import pprint
from config import pet_finder_api_key, pet_finder_secret_key
petfinder_base_url = "https://api.petfinder.com/v2/"


def getAccessToken():
    url = f'{petfinder_base_url}oauth2/token'
    #print(url)
    #format post request body data
    #https://www.geeksforgeeks.org/get-post-requests-using-python/
    # data to be sent to api; data is the POST body
    data = {'grant_type':"client_credentials", 
            'client_id':pet_finder_api_key, 
            'client_secret':pet_finder_secret_key
           }
    #print(data)
    #how to add headers in python POSTS
    #https://stackoverflow.com/questions/8685790/adding-header-to-python-requests-module
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data = data, headers=headers)
    #print(response)
    if(response.ok):
        jData = json.loads(response.content)
        #print(jData)
        return jData["access_token"]
    else:
        # If response code is not ok (200)
        return None


#function to get total pages of results
def totalPages(animal_type,status,limit):
    url = f'{petfinder_base_url}animals?type={animal_type}&status={status}&limit={limit}'
    print(url)
    #format for calls to animal api
    #https://api.petfinder.com/v2/animals?type=dog&page=2
    #headers: Authorization: Bearer eyJ0eXA...
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers )
    if(response.ok):
        jData = json.loads(response.content)
        return jData['pagination']['total_pages']
       
    else:
        print("Not found")
        return None



def fetchPet(animal_type,limit,status,page):

    token = getAccessToken()

    url = f'{petfinder_base_url}animals?type={animal_type}&limit={limit}&status={status}&page={page}'
    print(url)
    #format for calls to animal api
    #https://api.petfinder.com/v2/animals?type=dog&page=2
    #headers: Authorization: Bearer eyJ0eXA...
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers )
    if(response.ok):
        jData = json.loads(response.content)
        return jData

    else:
        print("Not found")
        return None    


def petFinder(animal_type, status, limit):
   
   total_pages = totalPages(animal_type,status,limit)

   pets = []

   for  page in range(1,total_pages +1):
        petData = fetchPet(animal_type,limit,status,page)
        #print(petData)
        #append to a list from another list
        #https://stackabuse.com/append-vs-extend-in-python-lists/
        #pets.extend(petData["animals"])
        
        for row in petData["animals"]:
            
            pet_dict= {
            'pet_id': row['id'],
                'organization_id': row['organization_id'],
            'url': row['url'],
            'type': row['type'],
            'primary breed': row['breeds']['primary'],
            'secondary breed': row['breeds']['secondary'],
            'mixed breed': row['breeds']['mixed'],
            'age': row['age'],
            'gender': row['gender'],
            'size': row['size'],
            'photo1': '',
            'photo2': '',
            'photo3': '',
            'city': '',
            'state': '',
            'postcode': '',
            'email': '',
            'phone': ''
            }
            
            if len(row['photos']) > 0:
                pet_dict['photo1'] = row['photos'][0]['full']
            if len(row['photos']) > 1:
                pet_dict['photo2'] = row['photos'][1]['full']
            if len(row['photos']) > 2:
                pet_dict['photo3'] = row['photos'][2]['full']
                
                
                
            if 'contact' in row:
                contact = row['contact']
                
                if 'email' in contact:
                    pet_dict['email'] = row['contact']['email']
                if 'phone' in row:
                    pet_dict['phone'] = row['contact']['phone']
                
                if 'address' in contact:
                    address = row['contact']['address']
                    if 'city' in address:
                        pet_dict['city'] = row['contact']['address']['city']
                    if 'state' in address:
                        pet_dict['state'] = row['contact']['address']['state']
                    if 'postcode' in address:
                        pet_dict['postcode'] = row['contact']['address']['postcode']
        
                
            pets.append(pet_dict)    
    
    pets_df = pd.DataFrame(pets)
    print(pets_df)
    
    return pets_df
    
