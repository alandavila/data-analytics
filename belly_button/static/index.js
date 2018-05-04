function load_samples_dropdown(){
  Plotly.d3.json('/names', function(error, response){
    if (error) return console.warn(error);
    for(var i = 0; i < response.length; i++){
        Plotly.d3.select("#selDataset").append("option").attr("value",response[i]).text(response[i]);
    }
  })
}

function load_sample_table(sample){
  //sample: string of sample to show: "BB_940"
  //plots the table in the #sample_table node form the html document
  var url = '/metadata/' + sample;
  //Generate table with data from initial selected value
  Plotly.d3.json(url, function(error, response){
    if (error) return console.warn(error);
    var table = Plotly.d3.select('#sample_table');
    //refresh table by deleting all rows, data if present
    table.selectAll('tr').remove();
    table.selectAll('td').remove();
    table.selectAll('thead').remove();
    table.append('thead').text('Sample Metadata')
      .style('font-weight','bold');
    for (var key in response) {
      var val = response[key];
      var row = table.append('tr');
      row.append('td').text(key);
      row.append('td').text(val);
    }
  })
}
/*
function get_otu_data(value){
  //use flask roude '/samples/value' to retreive
  //two arrays: otu_values and otu_ids
  var otu_values = new Array();
  var otu_ids = new Array();
  //use flask route to get otu values and id data
  var url = '/samples/'  + value;
  Plotly.d3.json(url, function(error, response){
    if (error) console.warn(error);
    for(var i = 0; i < 10; i++){
      otu_values.push(response[value][i]);
      otu_ids.push(response['otu_id'][i]);
      }
    })
    return [otu_values, otu_ids];
}
*/
/*
function get_otu_descriptions(value, otu_ids){
  //use flask roude '/otu_descriptions' to retreive
  //a dictionary {otu_id:description}
  //use the values of array otu_ids to return
  //the array with the descriptions of those otu_ids
  var otu_descriptions = new Array();
  //use flask route to get otu values and id data
  var url = '/otu_descriptions';
  Plotly.d3.json(url, function(error, response){
    if (error) console.warn(error);
    for(var i = 0; i < 10; i++){
      var descr = response[otu_ids[i]];
      otu_descriptions.push(descr);
    }
  })
  return otu_descriptions;

}
*/
function initialize_page(){

  load_samples_dropdown()

  var initial_value = 'BB_940';
  load_sample_table(initial_value);

  var otu_values=[];
  var otu_ids = [];
  var otu_descriptions = [];
  //use flask route to get otu values and id data
  var url = '/samples/'  + initial_value;
  Plotly.d3.json(url, function(error, response){
    if (error) console.warn(error);
    for(var i = 0; i < 10; i++){
      otu_values.push(response[initial_value][i]);
      otu_ids.push(response['otu_id'][i]);
    }
    //use flask route to get otu values and id data
    url = '/otu_descriptions'
    Plotly.d3.json(url, function(error, response){
      if (error) console.warn(error);
      for(var i = 0; i < 10; i++){
        otu_descriptions.push(response[otu_ids[i]]);
      }
      //**********all data is available, let;s plot********//
      var data = [{
        values:otu_values,
        labels:otu_ids,
        text:otu_descriptions,
        hoverinfo:'text',
        hole: .4,
        type: 'pie'
      }];
      var layout = {
        height: 400,
        width: 500
      };

      Plotly.plot('thepie', data, layout);
    })
  })
}//initialize_page()

function optionChanged(value){

  load_sample_table(value);

  var otu_values=[];
  var otu_ids = [];
  var otu_descriptions = [];
  //use Flask route to get otu values and ids
  var url = '/samples/' + value;
  Plotly.d3.json(url, function(error, response){
    if (error) console.warn(error);
    for(var i = 0;i<10;i++){
      otu_values.push(response[value][i]);
      otu_ids.push(response['otu_id'][i]);
    }
    //use Flask route to get otu descriptions
    url = '/otu_descriptions'
    Plotly.d3.json(url, function(error, response){
      if (error) console.warn(error);
      //console.log(response);
      for(var i = 0;i<10;i++){
        otu_descriptions.push(response[otu_ids[i]]);
      }
      //**********all data is available, let;s plot********//
      var data = [{
        values:otu_values,
        labels:otu_ids,
        text:otu_descriptions,
        hoverinfo:'text',
        hole: .4,
        type: 'pie'
      }];
      var layout = {
        height: 400,
        width: 500
      };
      Plotly.newPlot('thepie', data, layout);
    })
  })
}//optionChanged(value)
