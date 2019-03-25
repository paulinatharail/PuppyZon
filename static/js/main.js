
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


// //File Browse Button click event
const browseButton = document.getElementById('browse');
const fileDialogBox = document.getElementById('file');
const spanText = document.getElementById('custom-text');

browseButton.addEventListener("click", function(){
    fileDialogBox.click();
});

fileDialogBox.addEventListener("change", function(){
    if(fileDialogBox.value){
        spanText.innerHTML = fileDialogBox.value.match(/[\/\\]([\w\d\s\.\-(\)]+)$/)[1];
    }
    else{
        spanText.innerHTML="No file chosen"
    }
    
});


