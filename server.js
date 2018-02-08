var express=require('express');
var bodyParser=require('body-parser');
var app=express()
var port=3000||process.env.PORT

app.set('view engine','ejs');
app.use(express.static('public'));
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({extended:true}));

app.get('/',function(req,res){
	res.render('index');
});

var spawn=require('child_process').spawn;

app.post('/heart',function(req,res){
	res.send(req.body);
	var parsed=req.body;
	var arr=[]; 
	for(var x in parsed){
		arr.push(Number(parsed[x]));
	}
	console.log(arr);
	py=spawn('python',['heart_disease.py']);
	data=arr;			//provide an array here
	dataString='';

	py.stdout.on('data',function(data){
		dataString+=data.toString();
	});

	py.stdout.on('end',function(){
		console.log('Sum of numbers=',dataString);
	});

	py.on('close',function(code){
		console.log('closing code: '+code);
	});

	py.stdin.write(JSON.stringify(data));
	py.stdin.end();

	//console.log('complete');
});


app.listen(port,function(){
	console.log('Server running on port : '+port)
});

