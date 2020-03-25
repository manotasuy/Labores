
  /* <form ... method="POST" onsubmit="return validarReg();">*/

/* Validacion para campos de registro de usuario*/
function validarReg() {
    var nombre, apellido, ci, tel, cumple, domicilio, nacionalidad, email, password, repassword, expresion;

    nombre = document.forms["perfil"]["nombre"].value;
    apellido = document.forms["perfil"]["apellido"].value;
    tel = document.forms["perfil"]["tel"].value;
    cumple = document.forms["perfil"]["cumple"].value;
    domicilio = document.forms["perfil"]["domicilio"].value;
    nacionalidad = document.forms["perfil"]["nacionalidad"].value;
    email = document.forms["perfil"]["email"].value;
    password = document.forms["perfil"]["password"].value;
    repassword = document.forms["perfil"]["repassword"].value;
    
    fecha = new Date();

    expresion = / \w+@\w+\.+[a-z] /;
    
  
    if (nombre.length>30 || nombre.length<3 || !isNaN(nombre)) {
        alert("Nombre debe tener entre 3 a 30 caracteres alfabeticos");
        return false;
    }
    else if (apellido.length>30 || apellido.length<2 || !isNaN(apellido)) {
        alert("Apellido debe tener entre 2 a 30 caracteres alfabeticos");
        return false;
    } 
    else if (ci.length>9 || ci.length<4 || isNaN(ci)){
        alert("La CI ingresada no es válida");
        return false;
    }
    else if (tel.length>30 || tel.length<4 || isNaN(tel)) {
        alert("Teléfono tiene que tener de 4 a 15 números");
        return false;
    }
    else if (direccion.length>80 || direccion.length<4) {
        alert("Dirección debe tener entre 4 a 80 caracteres");
        return false;
    } 
    else if (nacionalidad.length>40 || nacionalidad.length<4) {
        alert("Nacionalidad debe tener de 4 a 40 caracteres");
        return false;
    }
    else if (expresion.test(email) || email === ""){
        alert("El email no es correcto");
        return false;
    }
}

/* Validacion para campo de BPS usuario empleador*/
function validarBps() {
    var empleadorNumRegBPS, bpsSi, bpsNo;
    empleadorNumRegBPS = document.getElementById("empleadorNumRegBPS").value;
    bpsNo = document.getElementsByName("bpsNo");
    bpsSi = document.getElementById("bpsSi");


    if (bpsSi.checked==true) {
        if (empleadorNumRegBPS == "" || isNaN(empleadorNumRegBPS)) {
            alert("Si esta registrado debe ingresar su código correspondiente");
            return false;
        }  
    }
}
/* Validacion para campos de editar perfil empleado NO TERMINADO*/
function validarEdEmpleado(){
    validarReg();
}
/* Validacion para campos de editar perfil de empleadores*/
function validarEdEmpleador(){
    validarReg();
    validarBps();

}
/*Validacion para campos de registro Anuncios*/

function validateForm(){
    var titulo, descripcion, pagoPorHora;

    titulo = document.forms["anuncio"]["titulo"].value;
    descripcion = document.forms["anuncio"]["descripcion"].value;
    pagoPorHora = document.forms["anuncio"]["pagoPorHora"].value;

    if (titulo.length>30 || titulo.length<4){
        alert("El titulo debe contener de 4 a 30 caracteres");
        return false;
    }
    else if (descripcion.length>350 || descripcion.length<20){
        alert("La descripcion debe contener de 20 a 350 caracteres")
        return false;
    }
    else if (isNaN(pagoPorHora) || pagoPorHora.length<2 || pagoPorHora == 0){
        alert("El precio por hora debe de ser correcto");
        return false;
    }
}

/*

Validacion extencion imagen

<form method="POST" onchange="return validarExt()" > 
    <input type="file" id="archivoInput">
    <div id="muestraImg">

    </div>
*/ 


function validarExt() {
    var archivoInput, archivoRuta, extPermitidas;

    archivoInput = document.getElementById("archivoInput");
    archivoRuta = archivoInput.value;
    extPermitidas = /(.IMG|.JPG|.PNG)$/i;

    if(!extPermitidas.exec(archivoRuta)) 
    {
        alert("Asegurate haber seleccionado correctamente una imagen (.img, .jpg o .png)");
        archivoInput.value="";
        return false;
    }
    else {
        if (archivoInput.files && archivoInput.files[0]) 
        {
            var visor = new FileReader();
            visor.onload=function(e)
            {
                document.getElementById('muestraImg').innerHTML='<embed src="'+e.target.result+'" width="120" heigth="120">';
            };
            visor.readAsDataURL(archivoInput.files[0]);
        }
    }

}

    // Example starter JavaScript for disabling form submissions if there are invalid fields
    (function () {
        'use strict';
  
        window.addEventListener('load', function () {
          // Fetch all the forms we want to apply custom Bootstrap validation styles to
          var forms = document.getElementsByClassName('needs-validation');
  
          // Loop over them and prevent submission
          var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
              if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
              }
              form.classList.add('was-validated');
            }, false);
          }
          
          
          
          );
        }, false);
      })();
    