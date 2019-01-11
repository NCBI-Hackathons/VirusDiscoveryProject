# Virz

A simple Node/Express interface to query a Mongo viral contig database.

# To start

```
$ npm install
$ npm start
```

This will start up a server listening on port 8000.

Configure Nginx to proxy whatever port (e.g., 80) to this:

```
	upstream node {
		server 127.0.0.1:8000;
	}

    location / {
        proxy_pass http://node;
        proxy_buffering off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
```

# To use

There are only two routes defined:

* **/**: will give you a list of sample queries/projections.

* **/query**: will execute a Mongo query using the query string to construct a Mongo query/projection.

# Author

Ken Youens-Clark <kyclark@email.arizona.edu>
