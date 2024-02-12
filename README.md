# Frontend



## Requirements

To install your virtual environment you need :

- Python 3.9.9

After cloning the git, go to the root of the project and run the following commands:  

```
$pip install virtualenv
```
```
$virtualenv venv
```

```
$source venv/bin/activate
```

```
$pip install -r requirements.txt
```

## Run Frontend locally

To run the frontend locally, from projet root/src :
```
$python main.py
```

## Run Frontend with docker

If you want to launch the frontend with docker, you'll need to change the address to which our frontend points. To do this, simply modify the address, in the Requests folder, in the request.py file.

