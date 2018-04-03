$("#boton_enviar").click(function(event){
	var datos = { user: document.getElementById("user").value, passwd: document.getElementById("passwd").value };
	console.log("ei");
	axios.post('adduser.php', datos)
	.then(function (response) {
	    console.log(response);
	  })
	.catch(function (error) {
	    console.log(error);
  });

});
