from flask import Flask, request, render_template_string, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Optional: Max upload size, here set to 16MB

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template_string(UPLOAD_SUCCESS_HTML, filename=filename)

    return render_template_string(UPLOAD_FORM_HTML)


UPLOAD_FORM_HTML = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Upload new File</title>
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container mt-5">
  <h1 class="mb-3">Upload a new file</h1>
  <form method="post" enctype="multipart/form-data">
    <div class="mb-3">
      <label for="file" class="form-label">Choose file</label>
      <input type="file" class="form-control" name="file" id="file" required>
    </div>
    <button type="submit" class="btn btn-primary">Upload</button>
  </form>
</div>
</body>
</html>
'''

UPLOAD_SUCCESS_HTML = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>File Uploaded</title>
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container mt-5">
  <h1>File Uploaded Successfully!</h1>
  <p class="alert alert-success">File {{filename}} has been uploaded.</p>
</div>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)