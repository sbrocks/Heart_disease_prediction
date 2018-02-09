var express=require('express');
var bodyParser=require('body-parser');
var app=express()
var port=3000||process.env.PORT
var result='';
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
	py.stderr.on('data',function(data){
		console.log('error:'+data);
	});
	py.stdout.on('end',function(){
		if(parseInt(dataString)==0){
			result=false;
		} else {
			result=true;
		}
		console.log('Patient has high chances of suffering from heart disease: ',result);
	});

	py.on('close',function(code){
		console.log('closing code: '+code);
	});

	py.stdin.write(JSON.stringify(data));
	py.stdin.end();

	//console.log('complete');
});

app.get('/heart',function(req,res){
	res.render('results',{result:result});   // To be displayed on webpage
});

app.listen(port,function(){
	console.log('Server running on port : '+port)
});

