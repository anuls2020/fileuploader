import os
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # SET the upload folder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # SET maximum file size as 16MB

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submit an empty file without a file name.
        if file.filename == '':
            return redirect(request.url)
        # If the user selected the file correct
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
