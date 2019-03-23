// javascript
var animalType = d3.select("#animalType");

var animalType_value = animalType.property("value");

var BreedName = d3.select("#breedName").property("value");
var zip = d3.select("#zipcode").property("value");
console.log("Animal Type: " + animalType_value + " Breed Name: " + BreedName + "Zip code: " +zip );   


function startRead(evt) {
    var file = document.getElementById('file').files[0];
    if (file) {
        alert("Name: " + file.name + "\n" + "Last Modified Date :" + file.lastModifiedDate);
    }
}

function readFormData(evt) {

    alert("Animal Type: " + animalType_value + " Breed Name: " + BreedName + "Zip code: " +zip );  
}


startRead();
readFormData(animalType_value, BreedName, zip);