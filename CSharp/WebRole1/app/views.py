from app import app, db
from flask import request, render_template, url_for, redirect
from datetime import datetime
from werkzeug.utils import secure_filename
from app.models import Ad, CategoryList
from os.path import basename, splitext
import random, string

# Create storage service
from azure.storage import CloudStorageAccount
storage_account = CloudStorageAccount(account_name=app.config['STORAGE_ACCOUNT_NAME'], 
                                      account_key=app.config['STORAGE_ACCOUNT_KEY'])
block_blob_service = storage_account.create_block_blob_service()

# Create container
from azure.storage.blob import PublicAccess
block_blob_service.create_container('images', public_access=PublicAccess.Container)

# Create service bus service
from azure.servicebus import ServiceBusService, Message, Queue
bus_service = ServiceBusService(service_namespace=app.config['SERVICEBUS_NAMESPACE'], 
                                shared_access_key_name=app.config['SERVICEBUS_ACCESS_KEYNAME'], 
                                shared_access_key_value=app.config['SERVICEBUS_ACCESS_KEYVALUE'])

# Create queue
bus_service.create_queue('adqueue', None, False)

def CreateAdBlob(file):
    filename = RandomString(12) + splitext((file.filename))[1]
    block_blob_service.create_blob_from_stream('images', filename, file.stream)
    imageURL = 'https://' + app.config['STORAGE_ACCOUNT_NAME'] + '.blob.core.windows.net/images/' + filename
    return imageURL

def DeleteAdBlob(ad):
    if ad.imageURL:
        block_blob_service.delete_blob('images', basename(ad.imageURL))
    if ad.thumbnailURL:
        block_blob_service.delete_blob('images', basename(ad.thumbnailURL))

def RandomString(size, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

@app.route('/')
@app.route('/index')
def index():
    adslist = Ad.objects.all()
    return render_template(
        'Index.html',
        title='Index',
        adslist=adslist
    )

@app.route('/details/<id>')
def details(id):
    ad = Ad.objects(id=id).first()
    return render_template(
        'Details.html',
        title='Details',
        ad=ad,
    )

@app.route('/delete/<id>')
def delete(id):
    ad = Ad.objects(id=id).first()
    
    if ad:
        app.logger.info(ad.id)

        try:
            DeleteAdBlob(ad)
        except Exception as e:
            app.logger.error(e)

        try:
            ad.delete()
        except Exception as e:
            app.logger.error(e)

    return redirect('index')

@app.route('/create', methods=['post', 'get'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        description = request.form.get('description')
        category = request.form.get('category')
        phone = request.form.get('phone')
        imageURL = ''

        file = request.files['imageFile']
        if file:
            try:
                imageURL = CreateAdBlob(file)
                app.logger.info(imageURL)
            except Exception as e:
                app.logger.error(e)

        ad = Ad(title=title, price=price, description=description, imageURL=imageURL, category=category, phone=phone)

        try:
            ad.save()

            if ad.imageURL:
                msg = Message(str(ad.id).encode("utf-8"))
                bus_service.send_queue_message('adqueue', msg) 

            return redirect(url_for('details', id=ad.id))

        except Exception as e:
            app.logger.error(e)
            return redirect('create')

    return render_template(
        'Create.html',
        title='Create',
        categoryList=CategoryList
    )

@app.route('/edit/<id>', methods=['post', 'get'])
def edit(id):
    ad = Ad.objects(id=id).first()

    if request.method == 'POST':
        ad.title = request.form.get('title')
        ad.price = request.form.get('price')
        ad.description = request.form.get('description')
        ad.category = request.form.get('category')
        ad.phone = request.form.get('phone')

        file = request.files['imageFile']
        if file:
            try:
                DeleteAdBlob(ad)
                ad.imageURL = CreateAdBlob(file)
                app.logger.info(ad.imageURL)
            except Exception as e:
                app.logger.error(e)

        try:
            ad.save()

            if ad.imageURL:
                msg = Message(str(ad.id).encode("utf-8"))
                bus_service.send_queue_message('adqueue', msg) 

        except Exception as e:
            app.logger.error(e)
        
        finally:
            return redirect(url_for('details', id=ad.id))

    return render_template(
        'Edit.html',
        title='Edit',
        ad=ad,
        categoryList=CategoryList
    )

