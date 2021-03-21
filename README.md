This project was designed to demostrate web scrapping, and then inserting the data into an unstructured database, Mongodb. The data was then inserted into a SQL table, Postgres.  We then setup a Flask webserver to display the data.
Web Site used: http://quotes.toscrape.com/
Total Quotes: 100
Total Authors: 50
Total Tags: 137
Flask Routes:
1. "/Home"
2. "/api/v1.0/quotes": " - Quotes"
3. "/api/v1.0/authors": " - List of Authors"
4. "/api/v1.0/authors/Bob%20Marley": " - Search for an Author, for example: Bob Marley.",
5. "/api/v1.0/tags": " - List of tags associated to quotes",
6. "/api/v1.0/tags/<tag>": " - Search for a tags associated to quotes"
7. "/api/v1.0/top10tags": " - List of top 10 tags for all quotes scraped, for examaple: /api/v1.0/love"