import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/home_search.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Property_Details = Base.classes.property_details
School_Ranking = Base.classes.school_ranking

#Deploy School Ranking Data
def importSchoolRankings():
    test_df = pd.read_sql_query('select * from school_ranking;', con=db.engine)
    if(len(test_df)==0):
        schoolRanking_file = "datasets/schoolRanking_medianPrice.csv"
        schoolRanking_df = pd.read_csv(schoolRanking_file,index_col=False)
        schoolRanking_df = schoolRanking_df.drop(schoolRanking_df.columns[0], axis=1)
        schoolRanking_df.columns = ['Name','Ranking','Address','Zipcode','Median_Price','Latitude','Longitude']
        print(schoolRanking_df)
        #Delete all rows from the table and resets auto increment value for id to 1
        db.engine.execute("delete from school_ranking;")
        schoolRanking_df.to_sql(name='school_ranking', con=db.engine, if_exists='append', index=False)
    else:
        print(f'{len(test_df)} records in database')


#Deploy Property Details Data
def importPropertyDetails():
    test_df = pd.read_sql_query('select * from property_details;', con=db.engine)
    if(len(test_df)==0):
        propertyDetails_file = "datasets/all_comps.csv"
        propertyDetails_df = pd.read_csv(propertyDetails_file,index_col=False)
        #propertyDetails_df = propertyDetails_df.drop(propertyDetails_df.columns[0], axis=1)
        #propertyDetails_df.columns = ['Name','Ranking','Address','Zipcode','Median_Price','Latitude','Longitude']
        #print(propertyDetails_df)
        #Delete all rows from the table and resets auto increment value for id to 1
        db.engine.execute("delete from property_details;")
        propertyDetails_df.to_sql(name='property_details', con=db.engine, if_exists='append', index=False)
    else:
        print(f'{len(test_df)} records in database')


@app.route("/schools")
def getSchoolList():
    # Use Pandas to perform the sql query
    stmt = db.session.query(School_Ranking).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    schoolNames = df['Name']
    return jsonify(list(schoolNames))



importSchoolRankings()
importPropertyDetails()



@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")



# @app.route("/comps/result>")
# def search_results(result):
#     """Return the column for a given result."""
#     sel = [
#         Search_Results.image,
#         Search_Results.city,
#         Search_Results.latitude,
#         Search_Results.longitude,
#         Search_Results.record_date,
#         Search_Results.state,
#         Search_Results.street,
#         Search_Results.zipcode,
#         Search_Results.zestimate
#     ]

#     results = db.session.query(*sel).filter(Search_Results.result == result).all()

#     # Create a dictionary entry for each row of home information
#     home_data = {}
#     for result in results:
#         #home_data["image"] = result[]
#         home_data["city"] = result[0]
#         home_data["latitude"] = result[4]
#         home_data["longitude"] = result[5]
#         home_data["rcord_date"] = result[6]
#         home_data["state"] = result[7]
#         home_data["street"] = result[8]
#         home_data["zipcode"] = result[13]
#         home_data["zestimate"] = result[12]

#     print(home_data)
#     return jsonify(home_data)


@app.route("/school_ranking_by_name/<school>")
def school_ranking_by_name(school):
    """Return school ranking data by name."""
    print(school)
    sel = [
        School_Ranking.Name,
        School_Ranking.Ranking,
        School_Ranking.Latitude,
        School_Ranking.Longitude,
        School_Ranking.Address,
        School_Ranking.Median_Price,
        School_Ranking.Median_Income
    ]

    results = db.session.query(*sel).filter(School_Ranking.Name == school).all()

# Create a dictionary entry for each row of school information
    
    for result in results:
        school_data = {}
        school_data["Name"] = result[0]
        school_data["Ranking"] = result[1]
        school_data["Latitude"] = result[2]
        school_data["Longitude"] = result[3]
        school_data["Address"] = result[4]
        school_data["Median_Price"] = result[5]
        school_data["Median_Income"] = result[6]

        print(school_data)
        return jsonify(school_data)

#function to get 
@app.route("/school_ranking_by_rank/<rank>")
def school_ranking_by_rank(rank):
    """Return school ranking data."""
    print(rank)
    sel = [
        School_Ranking.Name,
        School_Ranking.Ranking,
        School_Ranking.Latitude,
        School_Ranking.Longitude,
        School_Ranking.Address,
        School_Ranking.Median_Price
        ]

    results = db.session.query(*sel).filter(School_Ranking.Ranking == rank).all()

    # Create a dictionary entry for each row of school information
    school_data = {}
    for result in results:
        school_data = {}
        school_data["Name"] = result[0]
        school_data["Ranking"] = result[1]
        school_data["Latitude"] = result[2]
        school_data["Longitude"] = result[3]
        school_data["Address"] = result[4]
        school_data["Median_Price"] = result[5]

        print(school_data)
        return jsonify(school_data)


#function to get all data
@app.route("/school_ranking_all/")
def school_ranking_all():
    """Return school ranking data."""
    
    stmt = db.session.query(School_Ranking).statement
    school_df = pd.read_sql_query(stmt, db.session.bind)

    school_data = school_df.loc[:,["Name", "Ranking", "Address","Median_Price","Median_Income"]]
    # Format the data to send as json
    data = {
        "Name": school_data.Name.tolist(),
        "Ranking": school_data.Ranking.tolist(),
        "Address": school_data.Address.tolist(),
        "Median_Price": school_data.Median_Price.tolist(),
        "Median_Income": school_data.Median_Income.tolist()
    }

    return jsonify(data)

@app.route("/properties_by_school")
def properties_by_school():
    """Return property details by school name."""
    school  = request.args.get('school', None)
    bedrooms  = request.args.get('bedrooms', None)
    bathrooms  = request.args.get('bathrooms', None)
    print(school + " " + bathrooms)
    sel = [
        Property_Details.zpid,
        Property_Details.street,
        Property_Details.zipcode,
        Property_Details.city,
        Property_Details.state,
        Property_Details.latitude,
        Property_Details.longitude,
        Property_Details.image,
        Property_Details.useCode,
        Property_Details.bedrooms,
        Property_Details.bathrooms,
        Property_Details.finishedSqFt,
        Property_Details.lotSizeSqFt,
        Property_Details.yearBuilt,
        Property_Details.numFloors,
        Property_Details.numRooms,
        Property_Details.parkingType,
        Property_Details.school,
        Property_Details.price
    ]

    q = db.session.query(*sel).filter(Property_Details.school == school)
    
    if (bedrooms != 'Any'and bedrooms !='6+'):
        q = q.filter(Property_Details.bedrooms == bedrooms)
    elif (bedrooms =='6+'):
        q = q.filter(Property_Details.bedrooms >= 6)

    if (bathrooms != 'Any' and bathrooms !='5+'):
        q = q.filter(Property_Details.bathrooms == bathrooms)
    elif (bathrooms =='5+'):
        q = q.filter(Property_Details.bathrooms >= 5)



    results = q.all()

# Create a dictionary entry for each row of property
    property_list = []
    for result in results:
        property_data = {}
        property_data["zpid"] = result[0]
        property_data["street"] = result[1]
        property_data["zipcode"] = result[2]
        property_data["city"] = result[3]
        property_data["state"] = result[4]
        property_data["latitude"] = result[5]
        property_data["longitude"] = result[6]
        property_data["image"] = result[7]
        property_data["useCode"] = result[8]
        property_data["bedrooms"] = result[9]
        property_data["bathrooms"] = result[10]
        property_data["finishedSqFt"] = result[11]
        property_data["lotSizeSqFt"] = result[12]
        property_data["yearBuilt"] = result[13]
        property_data["numFloors"] = result[14]
        property_data["numRooms"] = result[15]
        property_data["parkingType"] = result[16]
        property_data["school"] = result[17]
        property_data["price"] = result[18]

        property_list.append(property_data)

    print(property_list)
    return jsonify(property_list)


    # sel = [
    #     School_Ranking.Name,
    #     School_Ranking.Ranking,
    #     School_Ranking.Latitude,
    #     School_Ranking.Longitude,
    #     School_Ranking.Address,
    #     School_Ranking.Median_Price
    #     ]

    # results = db.session.query(*sel).all()

    # # Create a dictionary entry for each row of school information
    # school_list = []
    # school_data = {}
    # for result in results:
    #     school_data = {}
    #     school_data["Name"] = result[0]
    #     school_data["Ranking"] = result[1]
    #     school_data["Latitude"] = result[2]
    #     school_data["Longitude"] = result[3]
    #     school_data["Address"] = result[4]
    #     school_data["Median_Price"] = result[5]

    #     school_list.append(school_data)

    #school_df = pd.DataFrame(school_list)


if __name__ == "__main__":
    app.run(debug=True)
