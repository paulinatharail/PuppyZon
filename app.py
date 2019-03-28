#Flask App
import os
import io
import numpy as np
import pandas as pd

# import keras
# from keras.preprocessing import image
# from keras.preprocessing.image import img_to_array
# from keras.applications.xception import (
#     Xception, preprocess_input, decode_predictions)
# from keras import backend as K

from flask import Flask, request, render_template, redirect, url_for, jsonify

#import PetFinder

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

#model = None

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
def upload_file():

    # Plan A: make the API Calls
    # =====================================================

    # cats = PetFinder.petFinder("cat", "adoptable", 1000)
    # dogs = PetFinder.petFinder("dog", "adoptable", 1000)
    # results = pd.concat([cats, dogs], sort=None)
    # results.to_csv("Resources/allpets.csv")


    # Plan B: use CSV
    #======================================================
    results = pd.read_csv("Resources/allpets.csv")
    #print(f"cats and dogs: {results}")

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
    
    return render_template("index.html")
            
            
@app.route('/listings')
def listings():
    """
    image_size = (224, 224)
    im = keras.preprocessing.image.load_img(filepath,
                                                    target_size=image_size,
                                                    grayscale=False)
    # preprocess the image and prepare it for classification
    image = prepare_image(im)

    #Feed into model
    #Model returns animal type and breed type
    # Make API calls and store results in results 
    """ 
        
    results = pd.read_csv("Resources/allpets.csv")
    #print(results)

    param = "pug" # test param
    breed = param.title() 
    #print(breed)
        
    filtered_results = results[results["primary breed"] == breed]
    filtered_results = filtered_results.fillna("")

    #print(filtered_results["primary breed"])

       
    filtered_results.to_csv('Resources/filtered_results.csv', header=True, index=False) 
        
    columns = list(filtered_results.columns)
    #print(f"Column titles: {columns}")


    listings = []
    for index, row in filtered_results.iterrows():
        dictionary = {}
        for col in columns:
            #print(col)
            #print(type(col))
            #print(results[col][10])
            #print(filtered_results[col])
            #print(row[col])
            dictionary[col] = row[col]
        
        listings.append(dictionary)
    
    print(f"dictionary: {listings}")

    return jsonify(listings)


if __name__ == "__main__":
    app.run(debug=True)







        



