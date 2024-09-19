<h1>Library Management Application</h1>
<h3>Backend - Python/Flask</h3>
<br>
<h5>---------- Librarian Credentials ----------</h5>
<p>Username: admin123</p>
<p>Password: admin123</p>
<br>
<h5>---------- Models ----------</h5>
<h6>User</h6>
<p>Following are the fields/column for user table</p>
<p>id</p> 
<p>userType</p> 
<p>visitedToday</p> 
<p>flagged</p> 
<p>firstName</p> 
<p>lastName</p> 
<p>email</p> 
<p>username</p> 
<p>password</p>
<br> 
<h6>Section</h6>
<p>Following are the fields/column for section table</p>
<p>id</p>
<p>name</p>
<p>dateCreated</p>
<p>description</p>
<p>rating</p>
<br>
<h6>Book</h6>
<p>Following are the fields/column for book table</p>
<p>id</p>
<p>status</p>
<p>flagged</p>
<p>title</p>
<p>author</p>
<p>language</p>
<p>releaseDate</p>
<p>section</p>
<p>contentPath</p>
<p>currentIssuer</p>
<p>issuedDate</p>
<p>returnedDate</p>
<p>rating</p>
<p>totalRater</p>
<br>
<h6>IssuedBook</h6>
<p>Following are the fields/column for issuedBook table</p>
<p>id</p>
<p>status</p>
<p>issuedDate</p>
<p>returnedDate</p>
<p>bookName</p>
<p>issuerName</p>
<p>bookId</p>
<p>userId</p>
<br>
<h5>---------- Resources ----------</h5>
<h6>UserResource</h6>
<p>CRUD: Create, Read, Update, Delete API to manage user resources</p>
<br>
<h6>SectionResource</h6>
<p>CRUD: Create, Read, Update, Delete API to manage section resources</p>
<br>
<h6>BookResource</h6>
<p>CRUD: Create, Read, Update, Delete API to manage book resources</p>
<br>
<h6>IssuedBookResource</h6>
<p>CRUD: Create, Read, Update, Delete API to manage issuedBook resources</p>
<br>
<h5>---------- Main ----------</h5>
<p>It has the initial login route</p>
<br>
<h5>---------- Static ----------</h5>
<p>It has all the .epub files i.e all the uploaded ebooks are being saved in this folder</p>
<br>
<h5>---------- User-Downloads ----------</h5>
<p>This folder has all the .csv files i.e the ebook report which is generated by Librarian</p>
<br>