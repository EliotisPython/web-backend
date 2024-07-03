#render template es el redericcionador de las carpetas extensiones
from flask import Flask, send_from_directory, flash
#redirect y request es para llamar funciones
from flask import Flask, render_template, redirect, request, Response, session, url_for
from flask_mysqldb import MySQL
from flask_session import Session
#importamos las bibliotecas de reconocimiento-fabio
import cv2
import face_recognition
import os
import json
#LIBRERIA PARA SUBIR IMAGENES
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__,template_folder='templates')
app.secret_key = '321'

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
#la base de datos, se llama login
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Configuración para guardar archivos subidos
UPLOAD_FOLDER = 'C:\\Users\\escor\\OneDrive\\Escritorio\\Prototipo\\Images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Configuración para guardar archivos subidos en una nueva carpeta(Publicaciones)
NEW_UPLOAD_FOLDER = 'C:\\Users\\escor\\OneDrive\\Escritorio\\Prototipo\\NewUploadedImages'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['NEW_UPLOAD_FOLDER'] = NEW_UPLOAD_FOLDER
file_descriptions = {}
# Configuración para guardar archivos subidos
CORREO_FOLDER = 'C:\\Users\\escor\\OneDrive\\Escritorio\\Prototipo\\static\\uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['CORREO_FOLDER'] = CORREO_FOLDER
# Configuración para guardar archivos subidos para retiro de curso
RETIRO_FOLDER = 'C:\\Users\\escor\\OneDrive\\Escritorio\\Prototipo\\static\\retiros'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['RETIRO_FOLDER'] = RETIRO_FOLDER
# Configuración para guardar archivos en Horario
HORARIO_FOLDER = 'C:\\Users\\escor\\OneDrive\\Escritorio\\Prototipo\\Horario'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['HORARIO_FOLDER'] = HORARIO_FOLDER
#inicia el mysql
mysql = MySQL(app)
#PARTE DEL CODIGO DE SUBIR ARCHIVO
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

######################################################################################################################
@app.route('/pnotas')
def profesor_notas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, correo, PC1, PC2, PC3, PC4 FROM usuarios WHERE rol = 'alumno'")
    data = cur.fetchall()
    
    for alumno in data:
        promedio = (alumno['PC1'] + alumno['PC2'] + alumno['PC3'] + alumno['PC4']) / 4
        alumno['promedio'] = promedio
        alumno['estado'] = 'Aprobado' if promedio >= 10 else 'Desaprobado'

    return render_template('sitio/pnotas.html', alumnos=data)

@app.route('/actualizar_notas/<int:id>', methods=['POST'])
def actualizar_notas(id):
    if request.method == 'POST':
        pc1 = request.form['PC1']
        pc2 = request.form['PC2']
        pc3 = request.form['PC3']
        pc4 = request.form['PC4']
        
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE usuarios
            SET PC1 = %s, PC2 = %s, PC3 = %s, PC4 = %s
            WHERE id = %s
        """, (pc1, pc2, pc3, pc4, id))
        mysql.connection.commit()
        flash('Notas actualizadas correctamente')
        return redirect(url_for('profesor_notas'))

@app.route('/eliminar_nota/<int:id>/<string:pc>', methods=['POST'])
def eliminar_nota(id, pc):
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE usuarios SET {pc} = NULL WHERE id = %s", (id,))
    mysql.connection.commit()
    flash(f'Nota {pc} eliminada correctamente')
    return redirect(url_for('profesor_notas'))

@app.route('/eliminar_alumno/<int:id>', methods=['GET', 'POST'])
def eliminar_alumno(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = %s", [id])
    mysql.connection.commit()
    flash('Alumno eliminado correctamente')
    return redirect(url_for('profesor_notas'))

@app.route('/notasalumnos')
def mostrar_nota():
    return render_template('sitio/unotas.html')

@app.route('/mostrar_aprobados')
def mostrar_aprobados():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, correo, PC1, PC2, PC3, PC4 FROM usuarios WHERE rol = 'alumno'")
    data = cur.fetchall()
    
    aprobados = []
    for alumno in data:
        pc1 = alumno['PC1'] if alumno['PC1'] is not None else 0
        pc2 = alumno['PC2'] if alumno['PC2'] is not None else 0
        pc3 = alumno['PC3'] if alumno['PC3'] is not None else 0
        pc4 = alumno['PC4'] if alumno['PC4'] is not None else 0
        promedio = (pc1 + pc2 + pc3 + pc4) / 4
        
        if promedio >= 10:
            aprobado = {
                'id': alumno['id'],
                'nombre': alumno['nombre'],
                'correo': alumno['correo'],
                'PC1': alumno['PC1'],
                'PC2': alumno['PC2'],
                'PC3': alumno['PC3'],
                'PC4': alumno['PC4'],
                'promedio': promedio,
                'estado': 'Aprobado'
            }
            aprobados.append(aprobado)
    
    return render_template('sitio/pnotas.html', alumnos=aprobados)


@app.route('/mostrar_desaprobados')
def mostrar_desaprobados():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, correo, PC1, PC2, PC3, PC4 FROM usuarios WHERE rol = 'alumno'")
    data = cur.fetchall()
    
    desaprobados = []
    for alumno in data:
        pc1 = alumno['PC1'] if alumno['PC1'] is not None else 0
        pc2 = alumno['PC2'] if alumno['PC2'] is not None else 0
        pc3 = alumno['PC3'] if alumno['PC3'] is not None else 0
        pc4 = alumno['PC4'] if alumno['PC4'] is not None else 0
        promedio = (pc1 + pc2 + pc3 + pc4) / 4
        
        if promedio < 10:
            desaprobado = {
                'id': alumno['id'],
                'nombre': alumno['nombre'],
                'correo': alumno['correo'],
                'PC1': alumno['PC1'],
                'PC2': alumno['PC2'],
                'PC3': alumno['PC3'],
                'PC4': alumno['PC4'],
                'promedio': promedio,
                'estado': 'Desaprobado'
            }
            desaprobados.append(desaprobado)
    
    return render_template('sitio/pnotas.html', alumnos=desaprobados)

#####################################################################################################################
#Ver lista de alumnos

@app.route('/editar')
def editar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT `id`, `dni`, `nombre`, `correo`, `contraseña`, `rol`, `asistencias`, `curso` FROM `usuarios` WHERE `rol` = 'alumno'")
    usuarios = cur.fetchall()
    cur.close()
    return render_template('sitio/editar.html', usuarios=usuarios)

@app.route('/cambiar_contrasena/<int:id>', methods=['POST'])
def cambiar_contrasena(id):
    nueva_contrasena = request.form['nueva_contrasena']
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuarios SET contraseña=%s WHERE id=%s", (nueva_contrasena, id))
    mysql.connection.commit()
    cur.close()
    
    flash('Contraseña actualizada correctamente')
    return redirect(url_for('editar'))

@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    
    flash('Usuario eliminado correctamente')
    return redirect(url_for('editar'))


##############################################################################################
#Libros

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return redirect(request.url)

    file = request.files['pdf_file']

    if file.filename == '':
        return redirect(request.url)

    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect(url_for('libros_profesor'))

@app.route('/delete_pdf/<filename>', methods=['POST'])
def delete_pdf(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('PDF successfully deleted')
    else:
        flash('PDF not found')
    return redirect(url_for('libros_profesor'))

@app.route('/libros')
def libros_profesor():
    # Filtrar solo archivos PDF en el directorio de uploads
    pdf_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.pdf')]
    return render_template('sitio/plibros.html', pdf_files=pdf_files)

@app.route('/ulibros')
def libros():
    # Filtrar solo archivos PDF en el directorio de uploads
    pdf_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.pdf')]
    return render_template('sitio/ulibros.html', pdf_files=pdf_files)



##################################################################################################h
@app.route('/phorario')
def horario_profesor():
    return render_template('sitio/phorario.html')

@app.route('/sitio/phorario', methods=["POST"])
def acceso_phorario():
    if request.method == 'POST':
        _texto = request.form['txtTextoProfesor']
        session['logueado'] = True
        session['textoProfesor'] = _texto

        if 'archivo' in request.files:
            archivo = request.files['archivo']
            if archivo.filename != '' and allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                filepath = os.path.join(app.config['HORARIO_FOLDER'], filename)
                archivo.save(filepath)
                session['archivo_horario'] = filename

        return redirect(url_for('horario_usuario'))

@app.route('/uhorario')
def horario_usuario():
    archivos = os.listdir(app.config['HORARIO_FOLDER'])
    archivos = [f for f in archivos if allowed_file(f)]
    archivo_subido = session.get('archivo_horario', None)
    return render_template('sitio/uhorario.html', archivos=archivos, textoProfesor=session.get('textoProfesor'), archivo_subido=archivo_subido)

@app.route('/eliminar_horario/<filename>')
def eliminar_horario(filename):
    filepath = os.path.join(app.config['HORARIO_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('horario_usuario'))

@app.route('/horario/uploads/<filename>')
def uploaded_horario_file(filename):
    return send_from_directory(app.config['HORARIO_FOLDER'], filename)

######################################################################################333
#Correo del profesor
@app.route('/pcorreo')
def correo_profesor():
    pretexto_justificacion = session.get('pretexto_justificacion', 'No se ingresó un pretexto.')
    correo_justificacion = session.get('correo_justificacion', 'No se ingresó un correo.')
    curso_justificacion = session.get('curso_justificacion', 'No se seleccionó un curso.')
    archivo_justificacion = session.get('archivo_justificacion', None)

    motivo_retiro = session.get('motivo_retiro', 'No se ingresó un motivo.')
    correo_retiro = session.get('correo_retiro', 'No se ingresó un correo.')
    curso_retiro = session.get('curso_retiro', 'No se seleccionó un curso.')
    archivo_retiro = session.get('archivo_retiro', None)

    return render_template('sitio/pcorreo.html',
                           pretexto_justificacion=pretexto_justificacion,
                           correo_justificacion=correo_justificacion,
                           curso_justificacion=curso_justificacion,
                           archivo_justificacion=archivo_justificacion,
                           motivo_retiro=motivo_retiro,
                           correo_retiro=correo_retiro,
                           curso_retiro=curso_retiro,
                           archivo_retiro=archivo_retiro)

@app.route('/justificacion')
def justificacion_usuario():
    mensaje = session.pop('mensaje', None)
    return render_template('sitio/justificacion.html', mensaje=mensaje)
@app.route('/sitio/justificacion', methods=["POST"])
def acceso_justificacion():
    if request.method == 'POST':
        _correo = request.form['txtCorreo']
        _pretexto = request.form['txtPretexto']
        _curso = request.form['curso']

        # Validar si el correo existe en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE correo = %s", (_correo,))
        usuario = cur.fetchone()
        cur.close()

        if usuario is None:
            session['mensaje'] = 'Usuario no encontrado.'
            return redirect(url_for('justificacion_usuario'))

        if 'archivo' in request.files:
            archivo = request.files['archivo']
            if archivo and allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                archivo.save(os.path.join(app.config['CORREO_FOLDER'], filename))
                session['archivo_justificacion'] = filename

        session['correo_justificacion'] = _correo
        session['pretexto_justificacion'] = _pretexto
        session['curso_justificacion'] = _curso

        return redirect(url_for('correo_profesor'))
    
@app.route('/uploads/<filename>')
def uploaded_justificacion_file(filename):
    return send_from_directory(app.config['CORREO_FOLDER'], filename)

@app.route('/eliminar_justificacion', methods=["POST"])
def eliminar_justificacion():
    filename = session.get('archivo_justificacion')
    if filename:
        filepath = os.path.join(app.config['CORREO_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        session.pop('archivo_justificacion', None)
        session.pop('correo_justificacion', None)
        session.pop('pretexto_justificacion', None)
        session.pop('curso_justificacion', None)
    return redirect(url_for('correo_profesor'))

@app.route('/uretiro')
def retiro_usuario():
    mensaje = session.pop('mensaje_retiro', None)
    return render_template('sitio/uretiro.html', mensaje=mensaje)

@app.route('/sitio/uretiro', methods=["POST"])
def acceso_retiro():
    if request.method == 'POST':
        _correo = request.form['txtCorreo']
        _motivo = request.form['txtMotivo']
        _curso = request.form['txtCurso']

        # Validar si el correo existe en la base de datos
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE correo = %s", (_correo,))
        usuario = cur.fetchone()
        cur.close()

        if usuario is None:
            session['mensaje_retiro'] = 'Usuario no encontrado.'
            return redirect(url_for('retiro_usuario'))

        if 'archivo' in request.files:
            archivo = request.files['archivo']
            if archivo and allowed_file(archivo.filename):
                filename = secure_filename(archivo.filename)
                archivo.save(os.path.join(app.config['RETIRO_FOLDER'], filename))
                session['archivo_retiro'] = filename

        session['correo_retiro'] = _correo
        session['motivo_retiro'] = _motivo
        session['curso_retiro'] = _curso

        return redirect(url_for('correo_profesor'))

@app.route('/uploads/retiro/<filename>')
def uploaded_retiro_file(filename):
    return send_from_directory(app.config['RETIRO_FOLDER'], filename)

@app.route('/eliminar_retiro', methods=["POST"])
def eliminar_retiro():
    filename = session.get('archivo_retiro')
    if filename:
        filepath = os.path.join(app.config['RETIRO_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        session.pop('archivo_retiro', None)
        session.pop('correo_retiro', None)
        session.pop('motivo_retiro', None)
        session.pop('curso_retiro', None)
    return redirect(url_for('correo_profesor'))
#####################################################################################publicaciones
@app.route('/publicaciones', methods=['GET', 'POST'])
def publi():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        description = request.form.get('description', '')
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['NEW_UPLOAD_FOLDER'], filename))
            file_descriptions[filename] = description
            # Guardar descripciones en un archivo
            with open('new_descriptions.json', 'w') as f:
                json.dump(file_descriptions, f)
            return redirect(url_for('publi'))
    # Cargar descripciones del archivo
    if os.path.exists('new_descriptions.json'):
        with open('new_descriptions.json', 'r') as f:
            file_descriptions.update(json.load(f))
    files = [(file, file_descriptions.get(file, '')) for file in os.listdir(app.config['NEW_UPLOAD_FOLDER'])]
    return render_template('sitio/pusuarios.html', files=files)

@app.route('/new_uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['NEW_UPLOAD_FOLDER'], filename)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['NEW_UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    file_descriptions.pop(filename, None)
    # Guardar descripciones actualizadas en el archivo
    with open('new_descriptions.json', 'w') as f:
        json.dump(file_descriptions, f)
    return redirect(url_for('publi'))

@app.route('/usuariosinicio')
def usuarios_inicio():
    files = os.listdir(app.config['NEW_UPLOAD_FOLDER'])
    files_with_descriptions = [(file, file_descriptions.get(file, '')) for file in files]
    return render_template('sitio/usuarios.html', files=files_with_descriptions)
#################################################################################################publicaciones
#Inicio
@app.route('/')
def index():
    #dentro del parentesis se pone la direccion del template
    return render_template('sitio/index.html')

#esta parte funcionara como admin
@app.route('/profesor')
def admin_profesor():
    return render_template('sitio/profesor.html')

#LOGIN
@app.route('/acceso-login', methods=["GET","POST"])
def login():
    
    #comprueba que lo que recibe es el correo y contraseña
    if(request.method == 'POST' and 'txtCorreo' in request.form and 'txtContraseña'):
        
        #se asignan variables
        _correo=request.form['txtCorreo']
        _contraseña=request.form['txtContraseña']

        #se conecta con mysql
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s', (_correo, _contraseña))
        account = cur.fetchone()

        #si se comprueba el ingreso entonces:
        if(account):
            session['logueando'] = True
            session['id'] = account['id']
            
            #verificar elro rol del que logueo
            if(account['rol']=='profesor'):
                #si es profesor entonces lo redirecciona al html profesor
                return render_template('sitio/pusuarios.html')
            elif(account['rol']=='alumno'):
                #si es alumno lo redirecciona al html alumno
                return render_template('sitio/alumno.html')
        
        
        else:
            return render_template("sitio/index.html")
    
    
    return render_template('sitio/index.html')


@app.route('/registrate')
def registrate():
    return render_template('sitio/registrate.html')

@app.route('/recuperarcontra')
def recuperarcontra():
    return render_template('sitio/recuperarcontra.html')

@app.route('/registrobiometrico')
def registrobiometrico():
    return render_template('sitio/registrobiometrico.html')

@app.route('/registrobiometrico2')
def registrobiometrico2():
    return render_template('sitio/registrobiometrico2.html')


#REGISTRO DE USUARIOS

@app.route('/sitio/registrate/guardar', methods=['POST'])
def sitio_registrate_guardar():
    _nombre = request.form['txtRegistroNombre']
    _correo = request.form['txtRegistroCorreo']
    _contraseña = request.form['txtRegistroContraseña']
    _dni = request.form['txtRegistroDNI']
    _curso = request.form['curso']
    
    if 'archivo' not in request.files:
        return 'No se ha subido ningún archivo'
    
    archivo = request.files['archivo']
    
    if archivo.filename == '':
        return 'No se ha seleccionado ningún archivo'
    
    if archivo and allowed_file(archivo.filename):
        filename = secure_filename(_dni) + os.path.splitext(archivo.filename)[1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        archivo.save(filepath)
        
        cur = mysql.connection.cursor()
        try:
            asistencias = 0
            cur.execute("INSERT INTO usuarios (nombre, dni, correo, contraseña, curso) VALUES (%s, %s, %s, %s, %s)", (_nombre, _dni, _correo, _contraseña, _curso))
            mysql.connection.commit()  # Asegúrate de hacer commit para guardar los cambios
            return redirect('/acceso-login')
        except Exception as e:
            mysql.connection.rollback()  # Revertir los cambios en caso de error
            return f'Ocurrió un error: {str(e)}'
        finally:
            cur.close()
    else:
        return 'Tipo de archivo no permitido'
    
    
#RECONOCIMIENTO BOTON

@app.route('/registrar', methods=['POST'])
def registrar_reconocimiento():
    def detect_and_draw_faces(frame, face_image_encodings):
        face_locations = face_recognition.face_locations(frame, model="hog")
        if face_locations:
            for face_location in face_locations:
                face_frame_encodings = face_recognition.face_encodings(frame, known_face_locations=[face_location])[0]
                for name, encoding in face_image_encodings.items():
                    result = face_recognition.compare_faces([encoding], face_frame_encodings)
                    if result[0]:
                        dni = name.split('.')[0]  # Obtener el dni del archivo jpg
                        print(f"Persona detectada con dni: {dni}.")
                        cur = mysql.connection.cursor()
                        cur.execute("SELECT asistencias FROM usuarios WHERE dni = %s", (dni,))
                        asistencias_result = cur.fetchone()
                        
                        if asistencias_result:
                            asistencias = asistencias_result['asistencias']
                            asistencias += 1 
                            cur.execute("UPDATE usuarios SET asistencias = %s WHERE dni = %s", (asistencias, dni))
                            mysql.connection.commit()
                        else:
                            print(f"No se encontró usuario con dni {dni}.")
                        
                        cur.close()
                        # Cerrar la cámara después de detectar a alguien
                        cap.release()
                        cv2.destroyAllWindows()
                        return redirect('/acceso-login')
                
    folder_path = r"C:\Users\escor\OneDrive\Escritorio\Prototipo\Images"
    face_images = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            name = os.path.splitext(filename)[0]
            image = cv2.imread(image_path)
            face_locations = face_recognition.face_locations(image)
            if face_locations:
                face_loc = face_locations[0]
                face_image_encodings = face_recognition.face_encodings(image, known_face_locations=[face_loc])[0]
                face_images[name] = face_image_encodings
            else:
                print(f"No se detectaron rostros en la imagen {filename}")

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar el frame de la cámara.")
            break
        frame = cv2.flip(frame, 1)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        detect_and_draw_faces(small_frame, face_images)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return redirect('/acceso-login')


if __name__ == '__main__':
    app.run(debug=True)