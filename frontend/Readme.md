<h1>Library Management Application</h1>
<h3>Frontend - Vue3.js</h3>
<br>
<h5>---------- Assets ----------</h5>
<p>It has LMS application logos and poster images</p>
<br>
<h5>---------- Router ----------</h5>
<p>It has all the necessary and required routes and routing logic for User and Librarian</p>
<br>
<h5>---------- Stores ----------</h5>
<p>Please find below mentioned list of stores which is used to manage alerts, searches, users, sections, ebooks and issuedbooks</p>
<h6>Alert Store</h6>
<p>This store is used to manage the alert throughout the LMS application</p>
<p>It has the following functions</p>
<p>success --> function to handle success alerts</p>
<p>error --> function to handle error alerts</p>
<p>warning --> function to handle warning alerts</p>
<p>info --> function to handle info alerts</p>
<br>
<h6>Search Store</h6>
<p>This store is used to manage the search operation throughout the LMS application</p>
<p>It has the following attributes and fucntions</p>
<p>errorMessage --> holds the error message</p>
<p>searchedUser --> array of resulted searched users</p>
<p>searchedSections --> array of resulted searched sections</p>
<p>searchedEBooks --> array of resulted searched ebooks</p>
<p>getAllSearchedSectionsAndEBooks --> function to retrieve sections and ebooks</p>
<p>getAllSearchedUsers --> function to retrieve users</p>
<br>
<h6>User Store</h6>
<p>This store is used to manage the user activites throughout the LMS application</p>
<p>It has the following attributes and fucntions</p>
<p>userRegistration --> function to register new user</p>
<p>userLogin --> function to initiate user login</p>
<p>retrieveAllUsers --> function to retrieve all the users</p>
<p>currentUser --> function to retrieve current/selected user</p>
<p>userUpdate --> function to update current/selected user</p>
<p>flagUser --> function to flag current/selected user</p>
<p>updateVisitedToday --> function to update visitedToday attribute for current/selected user</p>
<p>user --> Object for new user</p>
<p>errorMessage --> holds the error message</p>
<p>selectedUser --> Object for current/selected user</p>
<p>allUsers --> array of users</p>
<br>
<h6>Section Store</h6>
<p>This store is used to manage the section activites throughout the LMS application</p>
<p>It has the following attributes and fucntions</p>
<p>errorMessage --> holds the error message</p>
<p>section --> Object for new section</p>
<p>allSections --> array of sections</p>
<p>allSectionNames --> array of section names</p>
<p>selectedSection --> Object for current/selected section</p>
<p>sectionRegistration --> function to register new section</p>
<p>retrieveAllSections --> function to retrieve all sections</p>
<p>currentSection --> function to retrieve current/selected section</p>
<p>getAllSectionNames --> function to retrieve all section names</p>
<p>updateSection --> function to update current/selected section</p>
<p>deleteSection --> function to delete current/selected section</p>
<br>
<h6>EBook Store</h6>
<p>This store is used to manage the ebook activites throughout the LMS application</p>
<p>It has the following attributes and fucntions</p>
<p>errorMessage --> holds the error message</p>
<p>eBook --> Object for new ebook</p>
<p>allEBooks --> array of ebooks</p>
<p>selectedEbook --> Object for current/selected ebook</p>
<p>csvMessage --> holds the csv export message</p>
<p>addEBook --> function to register new ebook</p>
<p>retrieveAllEBooks --> function to retrieve ebooks</p>
<p>currentEBook --> function to retrieve current/selected ebook</p>
<p>exportCSVReport --> function to export CSV report</p>
<p>updateEBook --> function to update current/selected ebook</p>
<p>deleteEBook --> function to delete current/selected ebook</p>
<p>updateAssignedBookInfo --> function to assign current/selected ebook</p>
<p>updateRevokedBookInfo --> function to revoke current/selected ebook</p>
<br>
<h6>IssuedBook Store</h6>
<p>This store is used to manage the issuedBook activites throughout the LMS application</p>
<p>It has the following attributes and fucntions</p>
<p>errorMessage --> holds the error message</p>
<p>issuedBook --> Object for new issuedBook record</p>
<p>allIssuedBooks --> array of issuedBook records</p>
<p>requestedBook --> Object for requested issuedbook</p>
<p>registerIssuedBook --> function to add new issuedBook record</p>
<p>retrieveAllIssuedBooks --> function to retrieve issuedBook records</p>
<p>requestBookDetails --> function to retrieve current/selected issuedBook record</p>
<p>acceptBookRequest --> function to accept the status for current/selected issuedBook record</p>
<p>revokeBookRequest --> function to revoke the status for current/selected issuedBook record</p>
<br>
<h5>---------- Components ----------</h5>
<p>Following are the list of different .vue files which as used as components</p>
<p>HeaderNav</p>
<p>FooterNav</p>
<p>AboutUs</p>
<p>AddEBook</p>
<p>AddSection</p>
<p>AdminHome</p>
<p>AssignBook</p>
<p>ContactUs</p>
<p>ForgotPassword</p>
<p>LoginPage</p>
<p>ProfileDetails</p>
<p>SectionBookExplorer</p>
<p>SignUpPage</p>
<p>UserHome</p>
<p>UserStats</p>
<p>ViewEBook</p>
<p>ViewSection</p>