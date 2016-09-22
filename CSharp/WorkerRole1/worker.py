import os
import io
from time import sleep
from datetime import datetime
from config import *
from mongoengine import *
from os.path import basename, splitext
from PIL import Image

# Create storage service
from azure.storage import CloudStorageAccount
storage_account = CloudStorageAccount(STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY)
block_blob_service = storage_account.create_block_blob_service()

# Create container
from azure.storage.blob import PublicAccess
block_blob_service.create_container('images', public_access=PublicAccess.Container)

# Create service bus service
from azure.servicebus import ServiceBusService
bus_service = ServiceBusService(service_namespace=SERVICEBUS_NAMESPACE, 
                                shared_access_key_name=SERVICEBUS_ACCESS_KEYNAME, 
                                shared_access_key_value=SERVICEBUS_ACCESS_KEYVALUE)

# Create queue
bus_service.create_queue('adqueue', None, False)

connect(MONGODB_NAME, host=MONGODB_HOST, port=MONGODB_PORT, username=MONGODB_USERNAME, password=MONGODB_PASSWORD)

class Ad(Document):
    title = StringField(max_length=100)
    price = IntField()
    description = StringField(max_length=1000)
    imageURL = StringField(max_length=2083)
    thumbnailURL = StringField(max_length=2083)
    postedDate = DateTimeField(default=datetime.now)
    category = StringField(max_length=1000)
    phone = StringField(max_length=12)

def ProcessQueueMessage(msg):
    size = (80, 80)
    
    adId = msg.body.decode("UTF-8")

    try:
        ad = Ad.objects.get(id=adId)
    except Exception as e:
        print(e)
    
    output_stream = io.BytesIO()
    input_stream = io.BytesIO()

    try:
        block_blob_service.get_blob_to_stream('images', basename(ad.imageURL), output_stream)
    
        im = Image.open(output_stream)
        im.thumbnail(size)
        im.save(input_stream, 'JPEG')

        filename = splitext(basename(ad.imageURL))[0] + "thumb.jpg"
        block_blob_service.create_blob_from_bytes('images', filename, input_stream.getvalue())

        ad.thumbnailURL = 'https://' + STORAGE_ACCOUNT_NAME + '.blob.core.windows.net/images/' + filename
        print(ad.thumbnailURL)

        ad.save()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    while True:
        try:
            msg = bus_service.receive_queue_message('adqueue', peek_lock=False, timeout=20)
        except Exception as e:
            print(e)

        if msg.body:
            ProcessQueueMessage(msg)
        else:
            sleep(1.0)
