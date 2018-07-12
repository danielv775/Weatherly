# Project 1

Web Programming with Python and JavaScript

<h1>HTML</h1>

<h2>layout.html</h2>
<p>
layout.html defines the layout that is common throughout the website.
It imports bootstrap 4, my custom css file (styles.css), and a couple google fonts each of
which is leveraged extensivley throughout the various web pages. layout.html also makes use
of jinja block syntax to act a place holder for other html pages that will extend its imports, and structure.
</p>

<h2>home.html</h2>
<p>
home.html is the home page of the website. It allows the user to either login or register. On a larger screen(> 992px)
the background is an embeded video from youtube of EPIC landscapes with EPIC music. It takes a few seconds to load the background
video, so be patient--its worth it! Below 992px, the background is an image of a hiker in the mountains.
</p>

<h2>login.html</h2>
<p>
login.html is the login page of the website. It has a simple login form, allowing already existing users to login.
The entered username, along with a sha256 hash of the password are matched against an entry in the DB to log the user in.
There is various error handling for behavior you wouldn't expect at a login page. If login is successful, the user is redirected
to the search page, search.html.
</p>

<h2>register.html</h2>
<p>
register.html is the registration page of the website. It has a form similar to the login page. A new user would create their
account at this page. Assuming their username is unique, their username and a sha256 hash of their password gets inserted into the
DB. Upon successful registration, the user is redirected to the login page, where they can login with their new account.
</p>

<h2>search.html</h2>
<p>
search.html is the search page of the website. The user makes it here once they login. In the top right, they can see their own
username which is displayed via the session dictionary. The center of the page has a search form where the user can enter either
a zip code or a city to query the DB and generate a table of results. The user doesn't have to enter an exact match as I make use
of "LIKE %string%" in my SQL SELECT query to return a list of results that are a close but not exact match to the user's query.
If the user trys to search while they are logged out, this page redirects to the login page.
</p>

<h2>results.html</h2>
<p>
results.html displays the results of the users search as a bootstrap 4 table. They can click on either the zip code or city button
in any row to be directed to a dynamically generated location page. (see location.html)
</p>

<h2>location.html</h2>
<p>
location.html page is a dynamically generated web page of the web site that displays weather data about a unique location
via the Dark Sky API. It also displays information about the location that it pulls from my DB. Lastly, it displays a scrollable
comments section of user comments; each user who has left a comment had to check in, and a count of check ins is displayed as well.
</p>

<h1>SCSS & CSS</h1>

<h2>styles.css & styles.scss</h2>
<p>Similar to project0, these files contain the styling that I use throughout my website. I make use of bootstrap 4 to
make my website responsive and a decent experience on mobile as well as desktop.
</p>

<h1>Python</h1>

<h2>application.py</h2>
<p>
application.py is the FLASK back-end of the web app. It has functions that handle various user GET and POST requests. All the logic
that makes the html pages above functional, handle user interactions, handle bad user input, and query the Database is here.
Functions in this file are trigerred by a user either going to a specified route via a GET request, or by a call from url_for()
that dynamically builds the url based on the specified handler function and the arguments passed in. In addition to the functions
that make the webpages work, application.py also has an API that handles GET requests in the format "/api/zipcode". The handler pulls
location and check_in data from the DB, populates a python dictionary, and turns it into a json object prior to returning it to the user.
</p>

<h2>import.py</h2>
<p>import.py is a python script used to create my DB tables, read data from zips_updated.csv and insert the data
into my locations table. I make use of pandas to read in the csv file, and add leading 0's to the zip code column
prior to inserting into the DB. I wanted to use pandas to_sql function to directly insert all the rows at once into my table, but
this command kept hanging, so I resorted to iterating through the rows of the dataframe and inserting row by row.
</p>

<h1>Data</h1>

<h2>zips_updated.csv</h2>
<p>zips_updated.csv was the newly sent out location file that I used in import.py to populate my locations table in my DB</p>