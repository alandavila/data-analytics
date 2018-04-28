
//function that queries dataSet for data based
//on user's input and regrieves the data as a list of objects
function queryData(query){
  //initialize an array
  var data = [];
  for (var i = 0; i < dataSet.length ; i++) {
    //check query to determine which data to add to the list
    if (query.date.length !=0 && query.date != dataSet[i].datetime){
      continue;
    }
    if (query.country.length !=0 && query.country != dataSet[i].country){
      continue;
    }
    if (query.state != "state" && query.state != dataSet[i].state){
      continue;
    }
    if (query.city.length !=0 && query.city != dataSet[i].city){
      continue;
    }
    if (query.shape.length !=0 && query.shape != dataSet[i].shape){
      continue;
    }
    data.push(dataSet[i]);
  }
  return data;
}

//function to render data table based data
function displayDataTable(data){
  // Get a reference to the tbody element
  var $tbody = document.querySelector("tbody");
  // Start the table body with a blank HTML
  $tbody.innerHTML = "";
  //add column names
  //date/time, city, state, country, shape, and comment
  var columnNames = ["date/time", "city", "state", "country", "shape", "comment"];
  var $row = $tbody.insertRow(0);
  for (var j = 0; j < 6; j++){
    var $cell = $row.insertCell(j);
    $cell.innerText = columnNames[j];
    $cell.style.fontWeight = "900";
  }
  //Fill each row in information from data
  for (var i = 1; i < data.length ; i++) {
    // Insert a row into the table at position i
    var $row = $tbody.insertRow(i);
    // Insert five cells into the newly created row
    var $cell = $row.insertCell(0);
    $cell.innerText = data[i].datetime;
    var $cell = $row.insertCell(1);
    $cell.innerText = data[i].city;
    var $cell = $row.insertCell(2);
    $cell.innerText = data[i].state;
    var $cell = $row.insertCell(3);
    $cell.innerText = data[i].country;
    var $cell = $row.insertCell(4);
    $cell.innerText = data[i].shape;
    var $cell = $row.insertCell(5);
    $cell.innerText = data[i].comments;
  }
}
//function to render data table based on user  query and a max num or rows to display
function displayTable(numRows,query){
  // Get a reference to the tbody element
  var $tbody = document.querySelector("tbody");
  // Start the table body with a blank HTML
  $tbody.innerHTML = "";

  //add column names
  //date/time, city, state, country, shape, and comment
  var columnNames = ["date/time", "city", "state", "country", "shape", "comment"];
  var $row = $tbody.insertRow(0);
  for (var j = 0; j < 6; j++){
    var $cell = $row.insertCell(j);
    $cell.innerText = columnNames[j];
    $cell.style.fontWeight = "900";
  }
  //Fill each row in information from dataSet
  currRow = 1;
  for (var i = 0; i < numRows ; i++) {
    //check query to determine which data to display
    if (query.date.length !=0 && query.date != dataSet[i].datetime){
      continue;
    }
    if (query.country.length !=0 && query.country != dataSet[i].country){
      continue;
    }
    if (query.state != "state" && query.state != dataSet[i].state){
      continue;
    }
    if (query.city.length !=0 && query.city != dataSet[i].city){
      continue;
    }
    if (query.shape.length !=0 && query.shape != dataSet[i].shape){
      continue;
    }

    // Insert a row into the table at position i
    var $row = $tbody.insertRow(currRow);
    currRow = currRow + 1;
    // Insert five cells into the newly created row
    var $cell = $row.insertCell(0);
    $cell.innerText = dataSet[i].datetime;
    var $cell = $row.insertCell(1);
    $cell.innerText = dataSet[i].city;
    var $cell = $row.insertCell(2);
    $cell.innerText = dataSet[i].state;
    var $cell = $row.insertCell(3);
    $cell.innerText = dataSet[i].country;
    var $cell = $row.insertCell(4);
    $cell.innerText = dataSet[i].shape;
    var $cell = $row.insertCell(5);
    $cell.innerText = dataSet[i].comments;
  }
  return currRow
}

//User query object
var query = {
  date:"",
  city:"",
  state:"",
  country:"",
  shape:""
}
function addFunctions(items){
  var step = 50;
  console.log(items);
  for(var i = 0; i < items.length; i+=step){
    var $a = d3.select("#a-"+i).on("click", function (event) {
        d3.event.preventDefault();
        displayDataTable(items.slice(i,i + step));
        console.log( parseInt($a.text));
    });
  }
}

d3.select("#getdata-btn").on("click", function (event) {
    // d3.event.preventDefault() can be used to prevent an event's default behavior.
    // Here, it prevents the submit button from trying to submit a form when clicked
    d3.event.preventDefault();

    query.date = d3.select("#querybydate-input").node().value;
    query.city = d3.select("#querybycity-input").node().value;
    query.state = d3.select("#querybystate-input").node().value.toLowerCase();
    query.country = d3.select("#querybycountry-input").node().value;
    query.shape = d3.select("#querybyshape-input").node().value;

    console.log(query);
    var items = queryData(query);
    console.log(items)
    generatePagination(items.length, items);

    addFunctions(items);

    //displayDataTable(items);
});

function generatePagination(numItems, items){
  //
  var step = 50;
  var $navdiv = d3.select("#paginationdiv")
  $navdiv.node().innerHTML = "";
  var $nav = $navdiv.append("nav");
  var $ul = $nav.append("ul").attr("class","pagination");
  for(var i = 0; i < numItems; i+=step){
    var $li = $ul.append("li").attr("class","page-item").attr("id","li-"+i);
    var $a = $li.append("a").attr("class","page-link").attr("id","a-"+i).text(i);

  }
  //displayDataTable(items);
  displayDataTable(items.slice(0,step));
}


d3.select("#previous").on("click", function (event) {
    // d3.event.preventDefault() can be used to prevent an event's default behavior.
    // Here, it prevents the submit button from trying to submit a form when clicked
    d3.event.preventDefault();

    query.date = d3.select("#querybydate-input").node().value;
    query.city = d3.select("#querybycity-input").node().value;
    query.state = d3.select("#querybystate-input").node().value.toLowerCase();
    query.country = d3.select("#querybycountry-input").node().value;
    query.shape = d3.select("#querybyshape-input").node().value;

    console.log(query);
    displayTable(100,query);

});

//states list needed to populate states dropdown
var us_states = [
'AK',
'AL',
'AR',
'AZ',
'CA',
'CO',
'CT',
'DE',
'FL',
'GA',
'HI',
'IA',
'ID',
'IL',
'IN',
'KS',
'KY',
'LA',
'MA',
'MD',
'ME',
'MI',
'MN',
'MO',
'MS',
'MT',
'NC',
'ND',
'NE',
'NH',
'NJ',
'NM',
'NV',
'NY',
'OH',
'OK',
'OR',
'PA',
'RI',
'SC',
'SD',
'TN',
'TX',
'UT',
'VA',
'VT',
'WA',
'WI',
'WV',
'WY'];
//populate state dropdown box
for(var i = 0; i < us_states.length; i++){
    d3.select("#querybystate-input").append("option").attr("value",us_states[i]).text(us_states[i]);
}
