# G-Flight

G-Flight is a web service compromised to give it's users the best flight prices for the world most wanted destinations. 


## Usage    

To use the application, simply access it on [gflight.ga](https://gflight.ga)
___
![website landing page][landing-page]

## What does it do?

Uppon subscribing, we are going to evaluate several times a week all the flight prices departuring from your town. 

Every time we see that a flight price is lower than usual, we notify you by e-mail of the good deal!

This way you can be aware of all the good deals and plan out your vaccation

If you are interested in what the usual prices are, jump into the [Search Flights](https://gflight.ga/view-flights.html) page.


## Why did I built this?

This project started as an exercise on http requests on python. But then I saw the possibility of making this into a useful and usable application that can make peoples lifes easier a provide a good service to everyone!

As a consequence, I had to learn a large set of skills that later allowed my project to come to life. More on that later.


## Project Status
Pull requests and issues are always welcome! I am no longer actively developing new features for the project but it is still open to change. So if you see any issues or need new features, please contact me!

___
# Software architecture

This web aplication uses a MVC (Model, View, Controller) architecture with some additional services included, such as messagers (to contact users), additional databases and API's.

Here are some of the technologies used in this project

<img style="padding:5px 20px;" width="26px" src="https://raw.githubusercontent.com/devicons/devicon/00f02ef57fb7601fd1ddcc2fe6fe670fef3ae3e4/icons/python/python-original.svg"/>
<img style="padding:5px 20px;" width="26px" src="https://raw.githubusercontent.com/devicons/devicon/00f02ef57fb7601fd1ddcc2fe6fe670fef3ae3e4/icons/html5/html5-original.svg"/>
<img style="padding:5px 20px;" width="26px" src="https://raw.githubusercontent.com/devicons/devicon/00f02ef57fb7601fd1ddcc2fe6fe670fef3ae3e4/icons/css3/css3-original.svg"/>
<img style="padding:5px 20px;" width="26px" src="https://raw.githubusercontent.com/devicons/devicon/00f02ef57fb7601fd1ddcc2fe6fe670fef3ae3e4/icons/javascript/javascript-original.svg"/>
<img style="padding:5px 20px;" width="26px" src="https://raw.githubusercontent.com/devicons/devicon/00f02ef57fb7601fd1ddcc2fe6fe670fef3ae3e4/icons/heroku/heroku-original.svg"/>
<img style="padding:5px 20px;" width="26px" src="https://raw.githubusercontent.com/devicons/devicon/00f02ef57fb7601fd1ddcc2fe6fe670fef3ae3e4/icons/amazonwebservices/amazonwebservices-original.svg"/>
<img style="padding:5px 20px;" width="26px" src="https://raw.githubusercontent.com/devicons/devicon/00f02ef57fb7601fd1ddcc2fe6fe670fef3ae3e4/icons/github/github-original.svg"/>
<img style="padding:5px 20px;" width="26px" src="https://raw.githubusercontent.com/devicons/devicon/00f02ef57fb7601fd1ddcc2fe6fe670fef3ae3e4/icons/postgresql/postgresql-original.svg"/>
<img style="padding:5px 20px;" width="26px" src="https://raw.githubusercontent.com/devicons/devicon/00f02ef57fb7601fd1ddcc2fe6fe670fef3ae3e4/icons/figma/figma-original.svg"/>
<img style="padding:5px 20px;" width="26px" src="https://raw.githubusercontent.com/devicons/devicon/00f02ef57fb7601fd1ddcc2fe6fe670fef3ae3e4/icons/flask/flask-original.svg"/>


![software architecture][architecture]

## **Technologies and frameworks used**
On each part/layer of the program a set of different software and programming languages had to be used. On this secction we will break down each component, from user to database.


### **Design**
All the website elements were designed by me, except the social media icons, which are credited on the page.
- [Figma][figma] : Design tool

### **Webpage**
All the pages were build from scratch using the Big3 of FrontEnd Development.
- HTML5
- CSS
- Vanilla JavaScript

### **Page Hosting**
The page is currently beeing hosted by the Github Pages service, using a domain name I own.
- Github Pages

### **Backend API**
The project backend is served as an REST API for communication with the frontend. This API was built using some simple Python frameworks.
- Python Flask
- Flask RESTfull

### **Backend API Hosting**
The API is hosted on [Heroku][heroku] under this [endpoint][backend-endpoint]. The service is running 24/7 garanteeing the best user experience of the website
- Heroku

### **Backend services Hosting**
Many of the controller functionalities, such as sending flights to the users and updating flight prices reside on API endpoints through GET requests. 
This requests are made using Amazon AWS Lambda functions and are activated through weekly triggers.
- AWS Lambda 

### **Messager**
All the user app notifications are sent via e-mail. This is done from inside the backend though a SMTP service called Mailgo
- Mailgo

### **Flight model**
The flight model is responsible for doing every action related with flights: destinations, city codes, prices, ...
It was implemented on Python but makes uses of the [Tequila Flight Api][tequila] through a helper class. This API fetches the flight data for a single departure and arrival.
It can access the apps database to update, retrieve and create tables with flight prices and destinations.
- Tequila API requests

### **User model**
The user model was also build using Python. Implemented with a `User` dataclass for dependency injection on the software controller.
This model also has a conneciton with the programs DataBase.
- Python

### **DataBase**
The active DB for the project is served in an Amazon AWS RDS Postgresql database. During the development of the project, another implementation of the database class was created using CSV files and the Pandas library.
- Postgresql
- AWS RDS
- Pandas


[architecture]: https://raw.githubusercontent.com/guilevieiram/g_flight/8e1a7d1c0ff2c7b884d327e739e96558fe8d5757/g-flight-architecture.svg
[landing-page]: https://raw.githubusercontent.com/guilevieiram/g_flight/main/src/view/static/media/front-page.png 
[figma]: https://www.figma.com/
[heroku]:   https://www.heroku.com
[backend-endpoint]: https://g-flight-backend.heroku.com
[tequila]: tequila.kiwi.com/