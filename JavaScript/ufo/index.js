function displayTable(numRows,query){
  // Get references to the tbody element, input field and button
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
    if (dataSet[i].datetime != query){
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
}



d3.select("#querybydate-btn").on("click", function (event) {
    // d3.event.preventDefault() can be used to prevent an event's default behavior.
    // Here, it prevents the submit button from trying to submit a form when clicked
    d3.event.preventDefault();

    var date = d3.select("#querybydate-input").node().value;
    console.log(date);
    console.log(dataSet.length);
    displayTable(dataSet.length,date);

  });
