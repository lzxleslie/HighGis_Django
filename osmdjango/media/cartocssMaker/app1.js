var grainstore = require('grainstore');
var fs = require('fs')
var params = {
	dbname: 'traj001',
	sql: 'select * from traj',
};

var style ;
params["style"] = style;

var options = {
  map: {srid: 4326},
  datasource: {
	type: "postgis",
    geometry_field: "geom",
	password:"whu",
	host: "localhost",
	port: "5432",
	user: "postgres",
	max_size: 18
  }   
};

var filepath = 'test.xml';
var mmls = new grainstore.MMLStore();
var mmlb = mmls.mml_builder(params, options);
mmlb.toXML(function(err, data){
	console.log(data);
    fs.writeFile(filepath,data, function(err){
    	if(err) console.log(err);
		console.log('It is OK');
    })
     
});
