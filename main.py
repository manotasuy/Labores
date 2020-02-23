from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)


@app.route("/")
@app.route("/Inicio")
def despliegue():
    return render_template("Inicio.html")


# @app.route("/suma/<int:num1>/<int:num2>")
# @app.route("/suma/<int:num1>/<float:num2>")
# @app.route("/suma/<float:num1>/<int:num2>")
# @app.route("/suma/<float:num1>/<float:num2>")
# def suma(num1 = 0, num2 = 0):
#    contexto = {'numero1' : num1, 'numero2' : num2}
#    return render_template("suma.html", **contexto)

if __name__ == "__main__":
    app.run(debug=True)
