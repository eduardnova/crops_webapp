import os
import firebase_admin
from flask import Flask, request, redirect, render_template
from google.cloud import firestore, storage
from firebase_admin import credentials, auth




os.environ["GOOGLE_APPLICATION_CREDENTIALES"] = ""
app = Flask(__name__)
  
db = firestore.Client()
storage_client = storage.Client()


@app.route('/')
def index():
    return 'Hello from Flask!'

#AUTH CLIENTES
@app.route("/register_cliente", methods=["GET","POST"])
def register_clientes():
    if request.method == "POST":
       #obtiene los datos del formulario
       email = request.form["email"]
       password = request.form["password"]

       #Crea una nueva cuenta de  correo y contrase 
       user = auth.create_user(email = email, password = password)
      
       return  redirect("/login_clientes")
    return render_template("registercliente.html")

@app.route("/login_cliente", methods=["GET","POST"])
def login_clientes():
    if request.method == "POST":
       #Obtiene la cuenta de correo y contrasena
       email = request.form["email"]
       password = request.form["password"]
       
       #authentica la cuneta de correo y contrasena 
       try:
          user = auth.sign_in_with_email_and_password(email = email, password = password)
       except Exception as e:
           return "Inicio de session fallido"
       # almacena el ID del usuarioi en la session
       session["user_id"] = user.uid
       return redirect("/") 
    return render_template("loginclientes.html")  

@app.route("/reset-passwordcliente",methods=["GET","POST"])
def reset_password_cliente():     
    if request.method == "POST": 
       # obtiene el correo  electronico del formulario
       email = request.form["email"]

       # envia un correo electronicodel restablecimeinto de la contrasena
       auth.send_password_reset_email(email)

       return "se ha enviado un correo electronico para restablecer su Contrasena"
    return render_template("reset_passwordcliente.html")
  
#AUTH PROVEEDOR
@app.route("/register_proveedor", methods=["GET","POST"])
def register_proveedor():
    if request.method == "POST":
       #obtiene los datos del formulario
       email = request.form["email"]
       password = request.form["password"]

       #Crea una nueva cuenta de  correo y contrase 
       user = auth.create_user(email = email, password = password)
       return  redirect("/login_proveedor")
    return render_template("registerproveedor.html")
  
#AUTH TRANSPORTISTA


#AUTH ADMIN
  



@app.route('/create', methods = ['POST'])
def create_document():
    #recupera los datos enviados en el cuerpode la solicitud
    data = request.get_json()

    #crea un documento en la coleecions users con los datos recibidos
    doc_ref = db.collection("users").document()
    doc_ref.set(data)

    #devuelve una respuesta con el ID del documento create_documento
    return {'message' : 'Document created successfully', 'id': doc_ref.id}
  
@app.route('/read/<document_id>', methods = ['GET'])
def read_document(document_id):
    #recupera el documento con el ID  especificado
    doc_ref = db.collection("users").document(document_id)
    doc = doc_ref.get()
                                                             
    #devuelve una respuesta con los documento
    return {'data': doc.to_dict()}

@app.route('/update/<document_id>', methods = ['PUT'])
def update_document(document_id):
    # recupera los datos enviados en el cuerpo de la solicitud
    data = request.get_json()

    #Actualiza el documento con el ID especifico
    doc_ref = db.collection("users").document(document_id)
    doc_ref.update(data)

    #devuelve una respuesta con los documento
    return {'message' : 'Document update successfully'}
  
app.run(host='0.0.0.0', port=81)
