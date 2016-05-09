var grainstore = require('grainstore');

var params = {
  dbname: 'my_database',
  sql:'select * from my_table',
  style: '#my_table { polygon-fill: #fff; }'
}

// fully default.
var mmls = new grainstore.MMLStore();
var mmlb = mmls.mml_builder(params);
mmlb.toXML(function(err, data){
    console.log(data); // => Mapnik XML for your database with default styles
});


// custom pg settings.
var mmls = new GrainStore.MMLStore();

// see mml_store.js for more customisation detail 
var options = {
  Map: {srid: 4326},
  Datasource: {
    user: "postgres",
    geometry_field: "my_geom"
  }   
}

mmlb = mmls.mml_builder(params, options);
mmlb.toXML(function(err, data){
    console.log(data); // => Mapnik XML of custom database with default style
});


// custom styles.
var mmls = new GrainStore.MMLStore();
var mmlb = mmls.mml_builder(params);
mmlb.toMML(function(err, data){
    console.log(data) // => Carto ready MML
});

mmlb.toXML(function(err, data){
    console.log(data); // => Mapnik XML of database with custom style
});
