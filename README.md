# Item Catalog
## Project of Udacity Fullstack Web Development Nanodegree

### Pre-Requisites and Environment Preparation
#### First (get resources from the web)
- Download Git : https://git-scm.com/downloads
- Download Virtual Box :  https://www.virtualbox.org/wiki/Download_Old_Builds_5_1
- Download Vagrant : https://www.vagrantup.com/downloads.html
- fork this repository : https://github.com/udacity/fullstack-nanodegree-vm

#### Second (set up Environment using Terminal)
- clone the forked repository
- cd into the repository
- cd again into the vagrant file
- clone this repository


#### Third (Running the Virtual machine)
In order to complete these steps you have to be inside vagrant file
- Type the command : vagrant up
- Type the command : vagrant ssh
- Type the command : cd /vagrant/item_catalog

#### Fourth (Run the Actual WebApplication)
- Type the command : python app.py
- open "localhost:5000/categories" on your browser
- Navigate on the web application :)

### About this project
In this project I tried my best to provide a web-app that is feasible to brows categories and the items for each category.
Also in this web-app users can create, edit and delete both categories and items with some restrictions.
The first restriction is the user most be signed in to manipulate the existed data.
The second restriction is the user can only manipulate the categories and items created by them.
