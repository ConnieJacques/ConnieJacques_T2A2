# Connie Jacques - API Webserver Project

## R1) Identification of the problem you are trying to solve by building this particular app

## R2) Why is it a problem that needs solving?

## R3) Why have you chosen this database system. What are the drawbacks compared to others?

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


## R4) Identify and discuss the key functionalities and benefits of an ORM

Object Relational Mapping (ORM) connects an object orientated program to a relational database (Abba 2022). Relational databases have functionality to create, read, update and delete (CRUD) information stored in tables. The ability to perform these operations is a key reason for using a relational database. This functionality can be utilised by performing transitions with SQL on the command line, but it can be more convenient to have code written into a program to do this. For this reason, an ORM tool is used to allow for direct interaction between the database and an Object Orientation Programming (OOP) language (Abba 2022). 

OOP languages use objects to represent data. These consist of classes (blueprints outlining what information is needed to define the object) and their instances (objects with this information filled in). A RDBMS represents data in a tabular format (tables made up of rows and columns). The term ‘object-relational independence mismatch’ is used to describe the fundamental differences that exist between these two paradigms, including the use of dissimilar data structures, divergence in the way data is interacted with, and basic conceptual distinctions (Tina 2020). To make these two seperate things work together, we need an ORM tool.

The process of converting data from the database into an object is called hydration. This is done by converting values from columns in a table into object properties (Tina 2020). A table’s column attributes form the base of a class and the individual values contained within the column are transcribed to become the specific properties of a class instantiation. For this reason, ORM tools are language specific. This webserver application will use the ORM tool SQLAlchemy with the database adaptor/driver psycopg2 to enable the use of the OOP language python with a PostgreSQL database.

In addition to performing these key functionaries, some of the benefits of using an ORM include:

- Instead of writing lengthy SQL commands, methods from the ORM are used. An ORM has many built-in methods for performing transitions on the database. These methods are shorter to write thus reducing the volume of code needed to perform an operation and encourage DRY coding practices. Once a developer in familiar with the methods available for a particular ORM, they can reduce development time (Abba 2022). This increase in productive is additionally beneficial as it reduces the cost to develop software. 
- An ORM abstracts away some of the tedious workings of querying the database allowing programmer to focus on performing the tasks without having to think too much about how it happens.
- An ORM tool adds a layer of removal to SQL queries within the code, as explicit SQL commands are not used. Because of this, an application utilising ORM can be more secure against malicious SQL injection attacks by third parties (Admin Globaldots 2021, Abba 2022).
- ORM tools allow for queries to be stated but not executed until they are called i.e. the logic for querying a database can be outlined in the OOP language but is not used until it is needed. This is known as lazy-loading (Imperva 2022).


## R5) Document all endpoints for your API

## R6) An ERD for your app

## R7) Detail any third party services that your app will use

## R8) Describe your projects models in terms of the relationships they have with each other

## R9) Discuss the database relations to be implemented in your application

## R10) Describe the way tasks are allocated and tracked in your project


## References 

Abba, Ihechikara Vincent (2022) *What is an ORM – The Meaning of Object Relational Mapping Database Tools
*, Free Code Camp. Accessed at: https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/ (Accessed on 26 February 2023)

Admin Globaldots (2021) *8 best practices to prevent SQL injection attacks*, GlobalDots. Accessed at: https://www.globaldots.com/resources/blog/8-best-practices-to-prevent-sql-injection-attacks/ (Accessed on 27 February 2023)

Imperva (2022) *Lazy Loading*, Imperva Learning Center. Accessed at: https://www.imperva.com/learn/performance/lazy-loading/ (Accessed on 27 February 2023)

IONOS (2023) *PostgreSQL: a closer look at the object-relational database management system*, IONOS Digital Guide. Accessed at: https://www.ionos.com/digitalguide/server/know-how/postgresql/ (Accessed on 25 February 2023)

MariaDB (2023) *What is ACID Compliance in a Database? What It Means and Why You Should Care*, MariaDB. Accessed at: https://mariadb.com/resources/blog/acid-compliance-what-it-means-and-why-you-should-care/ (Accessed on 25 February 2023)

Tina (2020) *Introduction to Object-relational mapping: the what, why, when and how of ORM*, .dev. Accessed at: https://dev.to/tinazhouhui/introduction-to-object-relational-mapping-the-what-why-when-and-how-of-orm-nb2 (Accessed on 26 February 2023)