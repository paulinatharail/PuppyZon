#Flask App
import os
import io
import numpy as np

import keras
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from keras.applications.xception import (
    Xception, preprocess_input, decode_predictions)
from keras import backend as K

from flask import Flask, request, redirect, url_for, jsonify

import PetFinder

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

model = None

# # Load trained model
# def load_model():
#     global model
#     model = " "

# load_model()

# # Resize image for model using keras
# def prepare_image(img):
#     img = img_to_array(img)
#     img = np.expand_dims(img, axis=0)
#     img = preprocess_input(img)
#     # return the processed image
#     return img



@app.route('/', methods=['GET', 'POST'])
def api_call():
    cats = PetFinder.petFinder("cat", "adoptable", 1000)
    dogs = PetFinder.petFinder("dog", "adoptable", 1000)
    results = pd.concat([cats, dogs], sort=None)
    print(results)
    results.to_csv("Resources/pets.csv")
    
    return render_template("index.html", mars=mars)

def upload_file():
    if request.method == 'POST':
        print(request)

        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Save the file to the uploads folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "Image Saved!"
            
            
@app.route('/listings')
    def listings():

        image_size = (224, 224)
        im = keras.preprocessing.image.load_img(filepath,
                                                    target_size=image_size,
                                                    grayscale=False)
        # preprocess the image and prepare it for classification
        image = prepare_image(im)

        #Feed into model
        #Model returns animal type and breed type
        # Make API calls and store results in results   
        
        results = pd.read_csv("Resources/pets.csv")
        
        filtered_results = results.loc[results["primary breed"] == breed]
        filtered_results.to_csv('Resources/filtered_pets.csv',header=True, index=False) 
        columns = filtered_results.columns


        listings = {}
        for col in cols:
            listings[col] = filtered_results[col] 
        
        print(listings)

        return jsonify(listings)







        



