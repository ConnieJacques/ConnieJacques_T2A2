# Connie Jacques - API Webserver Project


### R1) Identification of the problem you are trying to solve by building this particular app

This API Webserver Project will build an application to list published Stephen King books and the movie adaptations made from them. It will detail the books, including when they were first published, whether the author published them under his own name or under a pen name, the publisher, ISBN, and other interesting information. Many movies have been produced from the stories told in these books. This application will give users quick assess to information about which books have been made into movies, when, who directed them and how successful and popular they were. The users of this application will also have the ability to keep a record of the movies and books they themselves have pursued and leave a rating. Ratings are useful way for other fans of this author to prioritise the books and movies they wish to spend their time consuming next, as there is a large number of both available. As such, the problem this application attempts to solve is the need for a convenient way for fans to find out what is available and what other fans have enjoyed the most, to help them choose what to view or read next. 


### R2) Why is it a problem that needs solving?

Our modern society is a busy one. Many people are working to excess, burnt out, stressed out and in need of a way to relax at the end of the day. For many, reading books and watching movies is a great way to do this; however, the volume of reading and viewing material available can be overwhelming and make choosing something to spend time on difficult. Knowing that you are a fan of an author, director or genre already can help to narrow down the choices but sometimes there are still a lot of options available and being able to choose something we are confident we will enjoy can be challenging. 

This API will aid fans of Stephen King’s work, or the horror genre more broadly, to choose a way to spend their time. This author has published 65 novels, and approximately 86 movie adaptations have been made from them. A public API containing information about all of these options does not currently exist; however, it should because this would be a convenient way to access details about these books and movies, and their popularity amongst enthusiasts, would benefit fans. Plus, the additional benefit for an individual to keep track of what they have and have not read and watched previously is undeniably handy.


### R3) Why have you chosen this database system. What are the drawbacks compared to others?

For this project, I will be using the relational database management system PostgreSQL. 

A relational database management system will be used for this application as it will be essential to be able to easily and flexibly query the database to access the required data. By dividing the data into relevant tables, we can ensure that it is simple to perform highly specific queries while also preventing data corruption in duplication. The process of normalisation will ensure that data integrity can be easily maintained and enable scalability for the project to grow in the future. 

As a RDBMS, Postgres uses Primary and Foreign Keys to relate tables to one another. The benefit of  Postgres itself managing the auto-incrementation of Primary Keys reduces the likely of data integrity being lost due to user error when entires are deleted or modified. As PostgreSQL has its own built-in systems to prevent partial data deletion where cascading removal is or is not used, we can be assured that the information contained in the database accurately reflects the raw data. 

Because it is an object relational database system, PostgreSQL allows for the use of multimedia content and complex data types such as such as boolean, temporal (date/time) and universally unique identifiers (UUIDs), in addition to alphanumeric data (IONOS 2023). As an ORDBMS, Postgres expands on the traditional relational model with the inclusion of object relational mapping to enable data to be stored as objects for use with an object orientated programming language such as Python (IONOS 2023).

For this API project, I will be using JavaScript Object Notation (JSON) extensively to format data. As such, a database management system that can handle this is essential. Although additional external python packages, outside the standard Flask library, are required, Postgres is compatible with this. However, the need for adaptation to make this work could be considered a disadvantage.  

Some other benefits of PostgreSQL that have influenced my decision to use this DBMS and not another include:

- Open source, meaning it is free to use.
- SQL compliant, making it easy for me use SQL commands on the command line to check queries directly against the database (IONOS 2023).
- ACID (Atomicity, Consistency, Isolation, and Durability) compliance ensures reliability when transactions are performed on the database (MariaDB 2023).

Drawbacks:

- Relationships between tables must be correctly identified and Foreign Keys must be accurately  entered. This is not an issue with NoSQL databases. 
- Speed - Postgres can be slower than other RDBMS, including MySQL; however, performance can be influenced by a lot of factors, so this is not always true.
- Learning curve - although PostgreSQL is simple to use it does require some knowledge of object orientated program methodology, querying patterns and a general understanding of relational modelling. 
- Storage - as PostgreSQL stores data in tabular form the amount memory required to hold the data can be significant. 
- Complexity - a normalised relational database model can be complex as the information is split across many tables. Keeping track of the relationships between tables can be tedious. The need for more standalone and joining tables can become necessary if the data stored within the database diversifies over time, which will compound the issue (IONOS 2023).
- Decreased performance as data size increases - over time, it is common for a database to become very large. As Postgres is a relational database, queries are often made across several tables. The ability to do this is a key reason for using a relational database in the first place; however, when the database is large, complex queries can have a slow response time, especially if many users are accessing the database simultaneously (IONOS 2023).


### R4) Identify and discuss the key functionalities and benefits of an ORM

Object Relational Mapping (ORM) connects an object orientated program to a relational database (Abba 2022). Relational databases have functionality to create, read, update and delete (CRUD) information stored in tables. The ability to perform these operations is a key reason for using a relational database. This functionality can be utilised by performing transitions with SQL on the command line, but it can be more convenient to have code written into a program to do this. For this reason, an ORM tool is used to allow for direct interaction between the database and an Object Orientation Programming (OOP) language (Abba 2022). 

OOP languages use objects to represent data. These consist of classes (blueprints outlining what information is needed to define the object) and their instances (objects with this information filled in). A RDBMS represents data in a tabular format (tables made up of rows and columns). The term ‘object-relational independence mismatch’ is used to describe the fundamental differences that exist between these two paradigms, including the use of dissimilar data structures, divergence in the way data is interacted with, and basic conceptual distinctions (Tina 2020). To make these two seperate things work together, we need an ORM tool.

The process of converting data from the database into an object is called hydration. This is done by converting values from columns in a table into object properties (Tina 2020). A table’s column attributes form the base of a class and the individual values contained within the column are transcribed to become the specific properties of a class instantiation. For this reason, ORM tools are language specific. This webserver application will use the ORM tool SQLAlchemy with the database adaptor/driver psycopg2 to enable the use of the OOP language python with a PostgreSQL database.

In addition to performing these key functionaries, some of the benefits of using an ORM include:

- Instead of writing lengthy SQL commands, methods from the ORM are used. An ORM has many built-in methods for performing transitions on the database. These methods are shorter to write thus reducing the volume of code needed to perform an operation and encourage DRY coding practices. Once a developer in familiar with the methods available for a particular ORM, they can reduce development time (Abba 2022). This increase in productive is additionally beneficial as it reduces the cost to develop software. 
- An ORM abstracts away some of the tedious workings of querying the database allowing programmer to focus on performing the tasks without having to think too much about how it happens.
- An ORM tool adds a layer of removal to SQL queries within the code, as explicit SQL commands are not used. Because of this, an application utilising ORM can be more secure against malicious SQL injection attacks by third parties (Admin Globaldots 2021, Abba 2022).
- ORM tools allow for queries to be stated but not executed until they are called i.e. the logic for querying a database can be outlined in the OOP language but is not used until it is needed. This is known as lazy-loading (Imperva 2022).


### R5) Document all endpoints for your API

### R6) An ERD for your app

![Stephen King DB ERD](./docs/stephen_king_db_erd.jpg)

### R7) Detail any third party services that your app will use

Flask: This application will be built on Flask, which is a python web application framework and is imported as a python module. Flask is a Webserver Gateway Interface (WSGI), meaning that it controls communication between servers and our python application (Python Basics 2021). 

Flask-SQLAlchemy: This application will utilise the ORM tool SQLAlchemy to control the relationships between our python objects and the tables in our PostgreSQL database. To use SQLAlchemy in this project, we will be using Flask-SQLAlchemy, which will be imported as a python module. Flask-SQLAlchemy is a specific extension for Flask to enable the use of SQLAlchemy. It provides the full range of functionality offered by SQLAlchemy but simplifies the execution of this specifically for a Flask application by providing handy defaults and helper methods for some common transactions performed on a relational database (Pallets 2010). The Model method from Flask-SQLAlchemy will be used to create models for this project. One benefit of using this method to create our models is that, although a custom name can be specified, it will automatically set the class name converted to camel case as table name in the database if we do not do this. The Column method will be used to define the columns in our tables so we can set a variable name as the column name, declare a primary key as an auto-incrementing integer that Flask-SQLAlchemy will manage for us, and specify a datatype (Integer, String, Text, DataTime, Float, Boolean, PickleType or LargeBinary) for each column to ensure data integrity is maintained (Pallets 2010). The Model method also allows us to outline the relationships between tables and define them as one-to-many by using the relationship() function in conjunction with the ForeignKey method or many-to-many by using the Tables and ForeignKey methods(Pallets 2010). 

Psycopg2: Psycopg2 is a popular database adapter used to connect Flask with a PostgreSQL database and enable communication between the two to be written in Python (PyPi 2022) and will be imported as a module for use in this project.

Flask-marshmallow: Flask-marshmallow is an integration tool used to enable Flask to work with the python library marshmallow. Python objects cannot be directly converted to json format, for this we need to use marshmallow. Marshmallow is used to convert complex datatypes (such as json formatted data) and objects into datatypes and objects that python can work with directly (Loria 2022). In our application, it will be used to validate data and serialise (convert) python objects into serialised objects which can be formatted in json, and to convert them back again (deserialisation). Flask-marshmallow is will also be used to generate schemas from our models. Schemas control what information from the database tables is displayed to the user. The flask-marshmallow method Schema will be used when defining the schemas for our project as this will allow us to use fields to specify exactly which fields (columns) to expose and the Nested method will be utilised imbed schemas for Foreign Keys within the output (Loria 2022).

Marshmallow-sqlalchemy: Marshmallow-sqlalchemy is used to integrate the python module marshmallow with flask-sqlalchemy (Loria 2023).

Flask-jwt-extended: JSON Web Tokens are used to authenticate a user in secure way. Instead of sending a user’s credentials with a request, a JWT is sent instead and this is verified against a secret key that is stored as an environment variable (Coder Academy 2023). The python package, flask-jwt-extended will be used in this project to enable us to do use JWTs for user authentication. The function create_access_token() will be used to generate a JWT, get_jwt_identity() will be used to verify a user is authenticated, and jwt_required() will be used to specify a route requires a JWT to access it (Loria 2022). These functions will be used with the JWTManager method to secure routes that have imbedded logic to make changes on our database. 

Flask-bcrypt: hashing is a way to encrypt sensitive information, such as passwords. As new technologies continue to be developed, so do malicious programs that can be used to hack applications with the goal of creating damage and/or stealing personal information (Countryman 2011). Because of this, a secure way to make an encryption more difficult to crack is needed. Bcrypt hashing will be used in this application because it is a ‘de-optimised’ hashing method, designed to be more tedious to crack. The python module flask-bcrypt will be imported for this and the function generate_password_hash({password}).decode(‘utf-8’) to secure passwords and assign them to a variable. 

os: The os library provides various operating system dependent functionalities. This project will use the enrivon.get() function from the os package to retrieve a user’s environment variables for the JWT secret key and database url. 

DateTime: The python package DateTime is used to create datetime objects and format them (Python Software Foundation 2023). The timedelta() function from the DateTime  library will be used to set and track expiry times for JSON Web Tokens used in our application. 


### R8) Describe your projects models in terms of the relationships they have with each other

### R9) Discuss the database relations to be implemented in your application

Users:

- User will be required to register and login to access the Read and Watched tables. 
- Users will only be able to create a single account as their email address will need to be unique.
- Users will need to provide their full name and an email address, and set a password that is 8 characters long. 
- Users may be an admin. Only users with admin privileges will be able to modify the Books and Movies tables.
- Once logged in, a user can modify only their own entries in the Read and Watched tables. Users with admin privileges will not be able to modify entries in these tables; only the author of the entry can change it.
- Users has a zero or many relationship with Read. A user may not read any books, but may read a book without watching the movie adaptation.
- Users has a many to many relationship with Books. A user can read many books.
- Users has a zero or many relationship with Watched. A user may not watch any movies, but does not have to have read the original book to have seen the movie adaptation. 
- Users has a many to many relationship with Movies. A user can watch many movies.

Books:

- Books table will be public. A user does not need to be registered or logged in to view the content in this table. Only a user with admin privilege can modify this table.
- Books has a many to many relationship with Users. Many books can be read by many users.
- Books has a zero to many relationship with Read. A book may not be read.
- Books has a zero to many relationship with Movies. One book can be made into many movies, but may not be adapted into a movie at all.
- Books has a one to one relationship with Authors. One book must have one author. 
- Books has a one to one relationship with Publishers. One book must have one publisher.

Movies:

- Movies table will be public. A user does not need to be registered or logged in to view the content in this table. Only a user with admin privilege can modify this table.
- Movies has a many to many relationship with Users. Many movies can be watched by many users.
- Movies has a zero to many relationship with Watched. A movie may not be watched.
- Movies has a one to one relationship with Books. One movie must be based on one book.
- Movies has a one to one relationship with Directors. One movie must have one director.
- Movies has a one to one relationship with ProductionCompanies. One movie is produced by one production company.

Read:

- Once logged in, a user can review leave a rating between 1 - 10 for a book. 
- The Read table can only be viewed by logged in Users. Users can only modify their own entries.
- Read is a joining table for the many to many relationship between Users and Books.
- Read has a one to one relationship with Users. An entry in the Read table must belong to one user.
- Read has a one to one relationship with Books. An entry in the Read table must be about one book.

Watched:

- Once logged in, a user can review leave a rating between 1 - 10 for a movie.
- The Watched table can only be viewed by logged in Users. Users can only modify their own entries.
- Watched is a joining table for the many to many relationship between Users and Movies.
- Watched has a one to one relationship with Users. An entry in the Watched table must belong to one user.
- Watched has a one to one relationship with Movies. An entry in the Watched table must be about one movie.

Authors:

- Authors has a one to many relationship with Books. One author can write many books.
- A book can be collaborative work.
- An author can use a pen name.

Publishers:

- Publishers has a one to many relationship with Books. One publisher can publish many books.

Directors:

- Directors has a one to many relationship with Movies. One director can direct many movies.

ProductionCompanies:

- ProductionCompanies has a one to many relationship with Movies. One production company can produce many movies.

### R10) Describe the way tasks are allocated and tracked in your project

To structure the implementation of each step in undertaking this assessment, I have used a Trello board in the kanban project management style to help me visualise the steps I need to complete and manage my time in doing so.

**My Trello board is available here:** 

All tasks are allocated to myself, as this is an individual project.There are four categories: To Do, In Progress, Completed and Nice to Have. Each card contains a step to undertake, details of the actions to be completed, and a timeframe. The timeframe for completing each step is represented with a coloured label. The key for the labels is as follows:

- Green: can be completed in under 30 minutes
- Yellow: can be completed in under 2 hours
- Orange: can be completed in 2 - 4 hours.

I have broken the steps down into enough detail that no card should take longer than 4 hours to complete. All cards held equal weight in terms of their priority. The To Do tasks were placed from the top of the category down in the anticipated order of competition, so that tasks that needed to be done before another could be started were undertaken first. When a task was started in was moved to the In Progress tab, and moved again to the Completed tab once it was finished. As I was utilising a kanban project management style, tasks that were moved to the Completed category could be moved back to the In Progress tab, if a review of the completed work was needed. Many tasks could be In Progress at the same time.

The Nice to Have category contained only cards to add in entries for all published Stephen Books and all the movie adaptations that have been made from these. The plan was to include only the five oldest novels and movies in the minimal viable product (MVP) so as to ensure enough time to focus on getting the body of the assessment completed, and add the whole lot only if there was enough time to do so before the submission date. 

This planning method was highly successful in allowing me visualise the remaining workload, allocate appropriate time for each task and complete the project without forgetting to do any particular task.
The following screenshots were taken as I worked my through the project. Some show what is contain on an individual card, while others show overall progress. All of the cards can be accessed on Trello via the link provided above.

Start of the project

![Trello Board Start of Project](./docs/Trello-start1.png)
![Trello Board Start of Project](./docs/Trello-start2.png)
![Trello Board Start of Project](./docs/Trello-start3.png)
![Trello Board Start of Project](./docs/Trello-start4.png)
![Trello Board Start of Project](./docs/Trello-start5.png)
![Trello Board Start of Project](./docs/Trello-start6.png)

Questions for the readme.md file were answered, where possible, prior to beginning to code out the API

![Trello Board Readme in Progress](./docs/Trello-readme-qs.png)
![Trello Board Readme in Progress](./docs/Trello-readme-qs2.png)

Cards were made for each section of the API to reflect the required MVC structure

![Trello Board Update - Start of Coding](./docs/Trello-coding1.png)
![Trello Board Update - Start of Coding - Working on Models](./docs/Trello-coding2-models.png)

## References 

Abba, Ihechikara Vincent (2022) *What is an ORM – The Meaning of Object Relational Mapping Database Tools
*, Free Code Camp. Accessed at: https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/ (Accessed on 26 February 2023)

Admin Globaldots (2021) *8 best practices to prevent SQL injection attacks*, GlobalDots. Accessed at: https://www.globaldots.com/resources/blog/8-best-practices-to-prevent-sql-injection-attacks/ (Accessed on 27 February 2023)

Coder Academy (2023) *JWT Authentication*, Flask Authentication, Coder Academy, Ed Lessons. Accessed at: https://edstem.org/au/courses/10081/lessons/27620/slides/195163 (Accessed on 1 March 2023)

Countryman, Max (2011) *Flask-Bcrypt*, Read the Docs. Accessed at: https://flask-bcrypt.readthedocs.io/en/1.0.1/ (Accessed on 1 March 2023)

Imperva (2022) *Lazy Loading*, Imperva Learning Center. Accessed at: https://www.imperva.com/learn/performance/lazy-loading/ (Accessed on 27 February 2023)

IONOS (2023) *PostgreSQL: a closer look at the object-relational database management system*, IONOS Digital Guide. Accessed at: https://www.ionos.com/digitalguide/server/know-how/postgresql/ (Accessed on 25 February 2023)

Loria, Steven (2022) *Basic Usage*, Read the Docs. Accessed at: https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/ (Accessed on 1 March 2023)

Loria, Steven (2022) *flask-marshmallow*, Read the Docs. Accessed at: https://flask-marshmallow.readthedocs.io/en/latest/ (Accessed on 1 March 2023)

Loria, Steven (2022) *marshmallow: simplified object serialization*, Read the Docs. Accessed at: https://marshmallow.readthedocs.io/en/stable/ (Accessed on 28 February 2023)

Loria, Steven (2023) *marshmallow-sqlalchemy*, Read the Docs. Accessed at: https://marshmallow-sqlalchemy.readthedocs.io/en/latest/ (Accessed on 28 February 2023)

MariaDB (2023) *What is ACID Compliance in a Database? What It Means and Why You Should Care*, MariaDB. Accessed at: https://mariadb.com/resources/blog/acid-compliance-what-it-means-and-why-you-should-care/ (Accessed on 25 February 2023)

Pallets (2010) *Declaring Models*, Pallets Projects. Accessed at: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/ (Accessed on 1 March 2023)

Pallets (2010) *Flask-SQLAlchemy*, Pallets Projects. Accessed at: https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/ (Accessed on 28 February 2023)

PyPi (2022) *psycopg2 - Python-PostgreSQL Database Adapter*, Python Software Foundation. Accessed at: https://pypi.org/project/psycopg2/ (Accessed on 28 February 2023)

Python Basics (2021) *What is Flask Python*, Python Basics. Accessed at: https://pythonbasics.org/what-is-flask-python/ (Accessed on 28 February 2023)

Python Software Foundation (2023) *datetime — Basic date and time types*, Python Docs. Accessed at: https://docs.python.org/3/library/datetime.html (Accessed on 1 March 2023)

Tina (2020) *Introduction to Object-relational mapping: the what, why, when and how of ORM*, .dev. Accessed at: https://dev.to/tinazhouhui/introduction-to-object-relational-mapping-the-what-why-when-and-how-of-orm-nb2 (Accessed on 26 February 2023)