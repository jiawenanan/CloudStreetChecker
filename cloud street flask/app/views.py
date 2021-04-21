# Important imports
from app import app
from flask import request, render_template, url_for
import numpy as np
from PIL import Image
import string
import random
import os
import sys
from tensorflow.keras import layers, models, optimizers
import matplotlib.image as mpimg


# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'
classes = ['False', 'True', 'Invalid Image']

model = models.load_model('app/static/model/kevin_md.h5')
# Route to home page
@app.route("/", methods=["GET", "POST"])


def index():
  if request.method == "GET":
    full_filename =  'images/white_bg.jpg'
    return render_template("index.html", full_filename = full_filename)
  if request.method == "POST":
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for i in range(10)) + '.png'
    full_filename =  'uploads/' + name
    image_upload = request.files['image_upload']
    imagename = image_upload.filename
    # file_path = image_upload.temporary_file_path
    img = Image.open(image_upload)
    # img = mpimg.imread(imagename)
    # img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))
    img_width, img_height = img.size
    img_depth = len(set(img.getdata()))
    # or img_depth !=3
    if (img_width < 375 or img_height < 375 or img_depth < 3):
      return render_template('index.html', full_filename = full_filename, pred = classes[2])
    # img = img.resize((375, 375))
    dim = 375
    w_begin = (img_width-dim)//2
    w_end = w_begin + dim
    h_begin = (img_height-dim)//2
    h_end = h_begin + dim
    img = img.crop((w_begin, h_begin, w_end, h_end))
    # pred_arr = np.array(img.convert('RGB'))
    img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))
    pred_arr = np.array(img.convert('RGB'))
    pred_arr.shape = (1,375,375,3)
    confidence = model.predict(pred_arr)[0][0]
    res = 0
    if (confidence > 0.5):
        res = 1
  # Returning template, filename, extracted text
    return render_template('index.html', full_filename = full_filename, pred = classes[res])

  # Main function
if __name__ == '__main__':
  app.run(debug=True)






