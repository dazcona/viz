# Viz Template

Visualization template that combines several frameworks and allows you to interact with your data on the web using D3 for interactive graphing and NetworkX for networks.

## Technologies

* Python 3
* MongoDB
* Flask
* Bootstrap
* Javascript
* D3
* NVD3
* NetworkX
* JSNetworkX
* (Optional) Docker

## Deployment

You can either use virtual environments or Docker containers:

### a) Virtual Environment using Bash

Creation of a virtual environments done by executing the command venv:
```
$ python3 -m venv env/
```

Command to activate virtual environment:
```
$ source env/bin/activate
```

Install dependencies:
```
(env) $ pip install -r requirements.txt
```

List the libraries installed on your environment:
```
(env) $ pip freeze
```

Run the development server:
```
(env) $ python src/app.py
```

When you are done, the command to deactivate virtual environment:
```
(env) $ deactivate
```

### b) Docker

Build image with Docker Compose using the Makefile's command:
```
$ make build
```

Run the image to start the mongo and web containers:
```
$ make run
```
