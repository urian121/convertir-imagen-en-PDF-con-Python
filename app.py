from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from PIL import Image, UnidentifiedImageError
import os
import uuid

app = Flask(__name__)
app.secret_key = '4324234234h32g4hg32j4f324'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def image_to_pdf(image_path, pdf_path):
    """Convierte una imagen a PDF."""
    try:
        image = Image.open(image_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(pdf_path, "PDF", resolution=100.0)
    except UnidentifiedImageError:
        raise ValueError("El archivo no es una imagen válida.")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(url_for('upload_file'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No se seleccionó ningún archivo', 'danger')
            return redirect(url_for('upload_file'))
        
        try:
            # Guardar la imagen temporalmente
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)

            # Generar un nombre único para el archivo PDF
            pdf_filename = f"{uuid.uuid4().hex}.pdf"
            pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)

            # Convertir la imagen a PDF
            image_to_pdf(image_path, pdf_path)

            # Eliminar la imagen temporal
            os.remove(image_path)

            return send_file(pdf_path, as_attachment=True)
        except ValueError as e:
            flash(str(e), 'danger')
            return redirect(url_for('upload_file'))
        except Exception as e:
            flash(f"Error al procesar el archivo: {str(e)}", 'danger')
            return redirect(url_for('upload_file'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
