# IWS Feature Request App [![Build Status](https://travis-ci.org/arianithetemi/feature-request-app.svg?branch=master)](https://travis-ci.org/arianithetemi/feature-request-app)
IWS Feature Request App is a web application based on Token-based Authentication RESTful API and other cutting-edge technologies. The main objective of this app is to ease the way of managing feature requests. Once client users are approved as official client by admins, they can send their feature requests, admin and client users corresponds with messages to these feature requests, then admin can approve and manage these feature requests, manage clients and other admins too.

**API Documentation will be available soon!**

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment section below for instructions on how to deploy the project on a live system.
## Local Installation
### Prerequisites
 * Ubuntu or macOS
 * Python 2.7
 * Pip
 * Virtualenv
 * Git
 * MySQL server
 
Install Pip on macOS
```
sudo easy_install pip
```
Install Pip on Ubuntu
```
sudo apt-get install python-pip
```
Install Virtualenv in Ubuntu and macOS
```
sudo pip install virtualenv
```
Install Git on macOS:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install git
```
Install Git on Ubuntu:
```
sudo apt-get install git
```
Install MySQL server in macOS: 
[https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)

Install MySQL server in Ubuntu
```
sudo apt-get install mysql-server
```
## Installing App (Ubuntu + macOS)
Please follow carefully step by step instructions below in order to get the app up and running locally.

1. Open terminal

2. First create a folder in your desktop called dev:
```
cd ~/Desktop
mkdir dev
cd dev
```
3. Getting the project in our local machine:
```
git clone https://github.com/arianithetemi/feature-request-app.git
cd feature-request-app
```
4. Install all packages used in app:
```
bash install.sh
```
5. Prepare configurations file:
```
cp config-template.cfg config.cfg
```
6. Open and fill out the config.cfg file *(your SQL username, password, host, DB name and your gmail account with password in Mail section) and then save the file.*
```
vi config.cfg
```
**Note: Remember the DB Name you set on config file, you will create DB with that exact name**

7. Creating the database in MySQL:

    * Open MySQL shell in macOS
    
      ```
      sudo /usr/local/mysql/bin/mysql -u root -p
      ```
    * Open MySQL shell in Ubuntu
    
      ```
      sudo mysql -p -u root
      ```
    * Inside MySQL shell execute this query:
      
      ```
        CREATE DATABASE <your-database-name-same-as-in-config>;
      ```
      **Note:** The **your-database-name-same-as-in-config** above must be the same value with SQL_DB_NAME set in config.cfg!
      
8. Populating database (creating tables and inserting two users):
```
bash populate_db.sh
```
> Admin username: **johny** and password: **johndoe**                              
> Client username: **william** and password: **123456**                             
> (Don't forget that the client must be approved by admin in order to login)

9. Running application
```
bash run-debug.sh
```
