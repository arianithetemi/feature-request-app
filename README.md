# IWS Feature Request App [![Build Status](https://travis-ci.org/arianithetemi/feature-request-app.svg?branch=master)](https://travis-ci.org/arianithetemi/feature-request-app)
IWS Feature Request App is a web application built on Token-based Authentication RESTful API and other cutting-edge technologies. The main objective of this app is to ease the way of managing feature requests. Client users can register with their information and by default are inactive, admins will approve as active these clients, clients can send their feature requests, admin and client users corresponds with messages to these feature requests, then admin can approve and manage main feature requests, set them in progress, and mark them as closed, manage clients and other admins too.

## API Documentation
[Check out API Documentation](https://app.swaggerhub.com/apis/arianithetemi/iws-feature-request-api/1.0.0)

## Technologies used:
 * Server-side scripting: **Python 2.7**
 * Backend Framework: **Flask**
 * Database: **MySQL**
 * ORM: **SQLAlchemy**
 * Javascript: **KnockoutJS and jQuery**
 * Responsive Interface: **Bootstrap**
 * Authentication: **JSON Web Token**
 * Web Service API: **REST**
 * Continuous Integration: **Travis CI**
 

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
        CREATE DATABASE <your_database_name_same_as_in_config>;
      ```
      **Note:** The **your_database_name_same_as_in_config** above must be the same value with SQL_DB_NAME set in config.cfg!
      
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
## Running Tests
The unit tests are mainly for testing the token-based RESTful API and database operations of the application.
Follow the instructions below in order to run automated tests.
 
 1. Open the terminal
 2. Change directory to the app folder
 3. Run the command:
 ```
    bash run_tests.sh
 ```
After the tests are completed you will see the result.
 
## Deployment
### Prerequisites
 * Ubuntu Server
 * MySQL Server
 * Apache Virtual Hosts(httpd)
 
### Initial Setup
 1. Install Apache Virtual Host:
  ```
  sudo apt-get update
  sudo apt-get install apache2
  sudo apt-get install libapache2-mod-wsgi
  ```
  2. Installing Python Dev libs:
  ```
  sudo apt-get -y install gcc make build-essential libssl-dev libffi-dev python-dev
  ```
  3. Install MySQL Server:
  ```
  sudo apt-get install mysql-server
  ```
  In the terminal prompt enter the new password for root.
  
  4. Create a database for the application

     * Enter the shell of MySQL:
     ```
     mysql -p -u root
     ```

     * Execute this query below:
     ```
     CREATE DATABASE feature_request_app;
     ```
  
  ### Setting up the app to deploy
   1. Change directory to WWW folder:
   ```
   cd /var/www
   ```
   2. Clone the project app from github:
   ```
   sudo git clone https://github.com/arianithetemi/feature-request-app.git
   cd feature-request-app
   ```
   3. Install project dependencies:
   ```
   sudo bash install.sh
   ```
   4. Populating database (creating tables and inserting two users):
   ```
   bash populate_db.sh
   ```
   > Admin username: **johny** and password: **johndoe**                              
   > Client username: **william** and password: **123456**                             
   > (Don't forget that the client must be approved by admin in order to login)
   
   5. Make a copy of the wsgi template file and edit it with root privileges:
   ```
   sudo cp app-template.wsgi app.wsgi
   sudo vi app.wsgi
   ```
   6. Edit the project's path in the first line of app.wsgi:
   ```
   app_dir_path = '/var/www/feature-request-app'
   ```
   7. Create, navigate and fill out the project config file(database + email):
   ```
   sudo cp config-template.cfg config.cfg
   sudo vi config.cfg
   ```
   **Note: In the SQL_DB_NAME in config.cfg set the name of the database that you just created.**
   
 ### Setting up new virtual host for the app
   1. Copy default virtual host config file to create new file specific to the project:
   ```
   sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/feature-request-app.conf
   ```
   2. Open the new file in your editor with root privileges:
   ```
   sudo vi /etc/apache2/sites-available/feature-request-app.conf
   ```
   3. Configure it to point to the project's app.wsgi file:
   ```
   <VirtualHost *:80>
     ServerAdmin admin@localhost
     ServerName IPADDRESS

     WSGIScriptAlias / /var/www/feature-request-app/app.wsgi
     <Directory /var/www/feature-request-app>
       Order allow,deny
       Allow from all
     </Directory>

     ErrorLog ${APACHE_LOG_DIR}/error.log
     CustomLog ${APACHE_LOG_DIR}/aacess.log combined
   </VirtualHost>
   ```
   4. Disable the default virtual host:
   ```
   sudo a2dissite 000-default.conf
   ```
   5. Enable the new virtual host we just created:
   ```
   sudo a2ensite feature-request-app.conf
   ```
   6. Restart the server for these changes to take effect:
   ```
   sudo service apache2 restart
   ```
   
## Author
 * **Arianit Hetemi**
