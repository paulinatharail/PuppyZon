
//javascript

var findPetButton = d3.select('#FindPet');


//on Button click event
findPetButton.on("click", function(){
    
    //Prevent the page from refreshing
    d3.event.preventDefault();

    //Get the user input data
    var animalType = d3.select('#animalType').property("value");
   
    //BreedName
    var breedName = d3.select('#BreedName').property("value");
    //zipcode
    var zipcode = d3.select('#zipcode').property("value");
    
    console.log("Animal Type is " + animalType);
    console.log("Breed Type is " + breedName);
    console.log("zipcode is " + zipcode);

    //Call the API with these 3 parameters

});


//on Button click event
var browse = d3.select('#browse');
var fileBrowse = d3.select('#file');
var fileUploadDIV = d3.select('#fileUpload');

browse.on("click", function(){
    console.log("Browse button clicked");

    



    var fileSelector = document.createElement('input');
    fileSelector.setAttribute('type', 'file');
    fileSelector.setAttribute('id', 'fileSelector');

    var selectDialogLink = document.createElement('a');
    selectDialogLink.setAttribute('href', '');
    selectDialogLink.setAttribute('id', 'fileSelector');

    selectDialogLink.innerText = 'Select File';

    selectDialogLink.onclick = function() {
        fileSelector.click();
        return false;
    }

    // document.body.appendChild(selectDialogLink);
    fileUploadDIV.append("fileSelector");
});

