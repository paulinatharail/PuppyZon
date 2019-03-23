

function addPropertyDataToTable(data, table) {

	var t = d3.select(table);
	var tbody = t.select('tbody');
	//Remove the existing rows to make room for new data
	tbody.selectAll('*').remove();

	for (i = 0; i < data.length; i++) {
		//item=row of data
		var item = data[i];
		console.log(item);
		var tr = tbody.append('tr');
		var td = tr.append('td').attr('rowspan', '5');
		var img = td.append('img').attr('src', item.image).attr('width', '200');
		td = tr.append('td').attr('class', 'heading').text("Address");
		td = tr.append('td').attr('class', 'data').text(item.street);
		td = tr.append('td').attr('class', 'heading').text("Bedrooms");
		td = tr.append('td').attr('class', 'data').text(item.bedrooms);
		td = tr.append('td').attr('rowspan', '5');
		var div = td.append('td').attr('class', 'map');
		var span = div.append('span').text("Map Here.");

		tr = tbody.append('tr');
		td = tr.append('td').html("&nbsp;");
		td = tr.append('td').attr('class', 'data').text(item.city + ", " + item.state + " " + item.zipcode);
		td = tr.append('td').attr('class', 'heading').text("Bathrooms");
		td = tr.append('td').attr('class', 'data').text(item.bathrooms);

		tr = tbody.append('tr');
		td = tr.append('td').attr('class', 'heading').text("Square Feet");
		td = tr.append('td').attr('class', 'data').text(item.finishedSqFt);
		td = tr.append('td').attr('class', 'heading').text("Year Built");
		td = tr.append('td').attr('class', 'data').text(item.yearBuilt);

		tr = tbody.append('tr');
		td = tr.append('td').attr('class', 'heading').text("Lot Sqft");
		td = tr.append('td').attr('class', 'data').text(item.lotSizeSqFt);
		td = tr.append('td').attr('class', 'heading').text("Floors");
		td = tr.append('td').attr('class', 'data').text(item.numFloors);

		tr = tbody.append('tr');
		td = tr.append('td').attr('class', 'heading').text("Price");
		td = tr.append('td').attr('class', 'data').text(item.price);
		td = tr.append('td').attr('class', 'heading').html("&nbsp;");
		td = tr.append('td').attr('class', 'data').html("&nbsp;");
	}
}


function addAffordabilityDataToTable(data, table) {

	var t = d3.select(table);
	var tbody = t.select('tbody');
	//Remove the existing rows to make room for new data
	tbody.selectAll('*').remove();
	var tr = tbody.append('tr');
	var th = tr.append('th').text("Rank");
	th = tr.append('th').text("Name");
	th = tr.append('th').text("Median Home Price");
	th = tr.append('th').text("Median Household Income");
	th = tr.append('th').text("Affordability Ratio");

	for (i = 0; i < data.Name.length; i++) {
		tr = tbody.append('tr');
		var td = tr.append('td').text(data.Ranking[i]);
		td = tr.append('td').text(data.Name[i]);
		td = tr.append('td').text(data.Median_Price[i]);
		td = tr.append('td').text(data.Median_Income[i]);
		td = tr.append('td').text(data.Median_Price[i] / data.Median_Income[i]);
	}
}

function buildPropertyTable(school, bedrooms, bathrooms) {
	url = '/properties_by_school?school=' + school + '&bedrooms=' + bedrooms + '&bathrooms=' + bathrooms
	console.log(url)
	d3.json(url).then((data) => {
		addPropertyDataToTable(data, "#listings");
	});
}

function buildAffordabilityTable() {
	d3.json('/school_ranking_all/').then((data) => {
		addAffordabilityDataToTable(data, "#affordability");
	});
}


function init() {
	// Grab a reference to the dropdown select element
	var selector = d3.select("#selSchools");
	// Use the list of sample names to populate the select options
	d3.json("/schools").then((schoolNames) => {

		schoolNames.forEach((school) => {
			selector
				.append("option")
				.text(school)
				.property("value", school);
		});

		// Use the first sample from the list to build the initial plots
		const firstSchool = schoolNames[0];
		buildPropertyTable(firstSchool,'Any','Any');
		buildAffordabilityTable();
	});
}

function optionChanged(newSchool) {
	// Fetch new data each time a new school is selected
	console.log('school selected: ' + newSchool);
	//buildPropertyTable(newSchool);

}

var filter_button = d3.select("#filter-btn");

//event handler for filter button click event
filter_button.on("click", function () {
	console.log("filter_button.click");
	d3.event.preventDefault();

	var schoolElement = d3.select('#selSchools');
	var schoolValue = schoolElement.property('value');
	
	var bedroomElement = d3.select('#selBedrooms');
	var bedroomValue = bedroomElement.property('value');
	
	var bathroomElement = d3.select('#selBathrooms');
	var bathroomValue = bathroomElement.property('value');

	buildPropertyTable(schoolValue, bedroomValue, bathroomValue);
});


init();