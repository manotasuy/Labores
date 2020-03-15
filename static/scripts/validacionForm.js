/* Validacion para campos de registro de usuario*/
function validarReg() {
    var nombre, apellido, ci, tel, cumple, domicilio, nacionalidad, email, password, repassword, expresion;
    
    nombre = document.getElementById("nombre").value;
    apellido = document.getElementById("apellido").value;
    tel = document.getElementById("tel").value;
    cumple = document.getElementById("cumple").value;
    domicilio = document.getElementById("domicilio").value;
    nacionalidad = document.getElementById("nacionalidad").value;
    email = document.getElementById("email").value;
    password = document.getElementById("password").value;
    repassword = document.getElementById("repassword").value;
    
    fecha = new Date();

    expresion = / \w+@\w+\.+[a-z] /;
    
  
    if (nombre.length>30 || nombre.length<2 || !isNaN(nombre)) {
        alert("Nombre debe tener entre 2 a 30 caracteres alfabeticos");
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
/* Validacion para campos de registro Anuncios*/
function validarAnuncio(){
    var titulo, descripcion, pagoPorHora;

    titulo = document.getElementById("titulo").value;
    descripcion = document.getElementById("descripcion").value;
    pagoPorHora = document.getElementById("pagoPorHora").value;

    if (titulo.length>30 || titulo.length<5){
        alert("El titulo debe contener de 5 a 30 caracteres");
        return false;
    }
    else if (descripcion.length>350 || descripcion.length<20){
        alert("La descripcion debe contener de 20 a 350 caracteres")
        return false;
    }
    else if (isNaN(pagoPorHora) || pagoPorHora.length<2 || pagoPorHora == "00"){
        alert("El precio por hora debe de ser correcto");
        return false;
    }
}
