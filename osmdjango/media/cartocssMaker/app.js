var grainstore = require('grainstore');
var fs = require('fs')
var path = require('path')
var params = {
	dbname: 'gis_database',
};

var style ;

//style and sql will write by who input in front-end
params["style"] = style;
params["sql"] = sql;

var options = {
  map: {srid: 3857},
  datasource: {
	type: "postgis",
    	geometry_field: "wkb_geometry",
    	// geometry_field: "geom",
	password:"whu",
	host: "localhost",
	port: "5432",
	user: "postgres",
	max_size: 18
  }
};

//username imported by var style ;

var filepath = '../upload/style/' + userXmlFile;
filepath = path.resolve(__dirname, filepath)
var mmls = new grainstore.MMLStore();
var mmlb = mmls.mml_builder(params, options);
mmlb.toXML(function(err, data){
    fs.writeFile(filepath,data, function(err){
    	if(err) console.log(err);
		console.log('Its ok to generate xml!');
    })

});
