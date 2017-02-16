---
services: cloud-services
platforms: python
author: msonecode
---

# Python Contoso Ads Application Cloud Service 

## Introduction

[Flask (Micro-framework for Python)](http://flask.pocoo.org/) version of the Contoso Ads application in [Get started with Azure Cloud Services and ASP.NET](https://azure.microsoft.com/en-us/documentation/articles/cloud-services-dotnet-get-started/).

## Prerequisites

### 1. [Python 3.4 interpreter for Windows](https://www.python.org/downloads/release/python-344/).

Note that only Python 3.4 and 2.7 are natively supported by Azure (Python 3.4 by default). If you prefer 2.7 or other versions, additional configuration for startup task is required.

### 2. Visual Studio 2013 or 2015

### 3. [Python Tools for Visual Studio (PTVS)](https://www.visualstudio.com/vs/python/)

### 4. [Azure SDK Tools for VS 2013](http://go.microsoft.com/fwlink/?LinkId=323510) or [Azure SDK Tools for VS 2015](http://go.microsoft.com/fwlink/?LinkId=518003)

### 5. Azure Storage Account 

Follow [this guide](https://azure.microsoft.com/en-us/documentation/articles/storage-create-storage-account/) to create a storage account and obtain the Access Key.

### 6. Azure Service Bus

Follow [this guide](https://azure.microsoft.com/en-us/documentation/articles/service-bus-python-how-to-use-queues/#create-a-service-namespace) to create a service bus and obtain the SAS key.
### 7. MongoDB 

You may use [MongoDB on Azure Virtual Machine](https://azure.microsoft.com/en-us/documentation/articles/virtual-machines-windows-classic-install-mongodb/) or [mLab](https://mlab.com/azure/).

## Run the sample

### 1\. Right click the project in the solution explorer and then choose Reload Project if it shows “unavailable”. 

![1](https://raw.githubusercontent.com/shaqian/Flask-Azure-Cloud-Service/master/1.png)
a
### 2\. Modify the connection settings in WebRole1 > app > config.py. 

MONGODB\_SETTINGS ={  
   'db': '*your database name*',  
   'host': '*your MongoDB host*',  
   'port': *port number*,  
   'username': '*your user name*',  
   'password': '*your password*'  
}

STORAGE\_ACCOUNT\_NAME = '*your storage account name*'  
STORAGE\_ACCOUNT\_KEY = '*storage access key*'  

SERVICEBUS\_NAMESPACE = '*your servicebus namespace*'  
SERVICEBUS\_ACCESS_KEYNAME = '*access key name*'  
SERVICEBUS\_ACCESS_KEYVALUE = '*access key value*'  

### 3\. Modify the connection settings in WorkerRole1 > config.py. 

STORAGE\_ACCOUNT\_NAME = '*storage account name*'  
STORAGE\_ACCOUNT\_KEY = '*storage access key*'  

SERVICEBUS\_NAMESPACE = '*servicebus namespace*'  
SERVICEBUS\_ACCESS_KEYNAME = '*access key name*'  
SERVICEBUS\_ACCESS_KEYVALUE = '*access key value*'  

MONGODB\_NAME = '*your database name*'  
MONGODB\_HOST = '*your MongoDB host*'  
MONGODB\_PORT =  *port number*  
MONGODB\_USERNAME = '*your user name*'  
MONGODB\_PASSWORD = '*your password*'  

### 4\. Right click the Python Environments section under the solution, remove the old virtual environment setting in WebRole1. 

![4](https://raw.githubusercontent.com/shaqian/Flask-Azure-Cloud-Service/master/2.png)

### 5\. Add a new virtual environment in WebRole1. 

![5](https://raw.githubusercontent.com/shaqian/Flask-Azure-Cloud-Service/master/3.png)

### 6\. Uncheck “Download and install packages” because we need to add some wheel files to local disk. 

![6](https://raw.githubusercontent.com/shaqian/Flask-Azure-Cloud-Service/master/4.png)

### 7\. Repeat step 2 - 6 for WorkerRole1. 

### 8\. Find the .whl files in bin folder under WorkerRole1. 

![8](https://raw.githubusercontent.com/shaqian/Flask-Azure-Cloud-Service/master/7.png)

### 9\. Create a bin folder in WorkerRole1 env folder and copy the .whl files to bin.

![9](https://raw.githubusercontent.com/shaqian/Flask-Azure-Cloud-Service/master/8.png)

### 10\. Repeat step 8 - 9 for WebRole1. 

### 11\. Run Install from requirements.txt for both virtual env. 

![11](https://raw.githubusercontent.com/shaqian/Flask-Azure-Cloud-Service/master/9.png)

### 12\. To debug a particular role, right click on the role name and click "Set as StartUp Project". 

![12](https://raw.githubusercontent.com/shaqian/Flask-Azure-Cloud-Service/master/10.png)

## Publish to Azure

You may follow [this guide](https://azure.microsoft.com/en-us/documentation/articles/cloud-services-python-ptvs/#publish-to-azure) to publish the application to Azure Cloud Service.

## Additional Information

1\. We use [wheels](http://pythonwheels.com/) to install cffi, cryptograpy and Pillow library, because  in Python 3.4 normal pip installation for these libraries may fail and return error **"Unable to find vcvarsall.bat"**. If you can successfully install all references just by defining the name in requirements, you may safely skip above step 8 - 10.

2\. Startup and Runtime task logs are located in the **C:\Resources\Directory{role}\LogFiles** folder in the Cloud Service instance. Check **ConfigureCloudService.txt** if any library in requirements.txt is not successfully installed. Check **LaunchWorker.err.txt** for WorkerRole runtime errors.
