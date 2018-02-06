# "Just-Email-It" Email API

This is a simple API built in Flask, designed for I/O using JSON. It takes in a JSON object with key:values for fields commonly associated with email - an array of addresses for "to:", "cc:", and "bcc:", as well as a string value for keys "from:", "subject:", and "content:". The API providers and abstracted interface between two different (and potentially any number of) email providers, switching over to a different provider if the primary fails. 

Current Heroku deployment can be accessed at 'https://nike-email-api.herokuapp.com/api/send'
***

## Requirements
```
-Python3
-Flask
-IPython (for happy debugging)
-Gunicorn (for Heroku deployment)
```
## Getting Started

Once you've cloned the project, create a Python virtual environment (virtualenvwrapper was used here, but isn't required), and then run ```pip install requirements.txt``` to fetch all required packages and their dependencies.

Once you've set up your virtual environment, you'll want to setup your ENV variables - you'll need to procure a API key for the email providers you want to use (SPARK_API_KEY and SENDGRID_API_KEY are the defaults), as well as set a PRODUCTION var for debugging/production, and PORT. Don't store your keys in the files!

At this point, run ```python app.py ```, which will init your server from the provided app package, and your server will be running! Specify the optional PORT env variable to run on a particular port, the app will default to port 5000.


## Docs

```.
.
├── Procfile
├── app.py
├── config.env
├── project
│   ├── __init__.py
│   └── email_providers.py
├── requirements.txt
└── sample_curls.py
```

The API is small, a single ```project``` package that contains the only current routing logic in ```__init__.py```, and imported classes in ```email_providers.py``` (making use of the email provider helper-libraries). You could scale out a complete exhaustive email API to include receive and tracking capability, as well as advanced HTML and file attachment sending, and abstract the functionality into individual class files in the ```project``` directory. Tests would also go here, though time was not on my side to write them. You would want to verify current functionality as well as mock the API responses. 

Since the bulk of the project is a python ```package``` with structure based on OOP, the ```app.py``` file is only responsible for starting the server and a few housekeeping tasks at boot. ```Config.env``` is just a helper file for setting up ENV variables locally (I included the actual keys here, don't spread them around please!), as well as a Procfile and requirements.txt for easy deployment.

Finally, you can find two pre-built CURL requests using my emails (feel free to sub them for your own), with one for local deployment and the other for the Heroku deployment. 

***/api*:** This is a simple root API that responds to GET requests to inform the user whether the API is running or not.

***/api/send*:** This is an abstracted interface to multiple email providers that takes in a JSON object and creates individual instances of emails based on provider. Each instance will attempt to successfully send, returning a 200-level response on success, and falling back to the next backup provider on a 400-level failure. As each provider handles their own API in sometimes dramatically different (errors send a simple JSON response in some, throw Exceptions in others) I decided it would be easier to completely encapsulate the sending and response handling logic for each email provider in its own individual class. The classes would then send a standard success or failure response based on the email provider API, which would then finally get handed back to the user.


```
{
	"from": "string",
	"to": ["array","of","strings"],
	"cc": ["array","of","strings"],
	"bcc": ["array","of","strings"],
	"subject": "string",
	"content": "string"
}
```

##Further Ideas

With more time I would definitely want to include user-testing on individual send events for each email provider, including checking for error-handling and invalid/edge-case inputs. Since we cannot rely on the actual email providers to conduct unit-tests, we would also want to setup a mock repository "API" for tests to check against, so that while we cannot rely on the email provider APIs themselves, we can model a mock repository on the expected responses from each email provider dependent on input (this would be quite time consuming to investigate properly). 

Expanding the API to also include file attachments and HTML support would be a logical next step, which would also include some way of piecing together multiple pieces of data and handling the different email providers' implementations. The API is currently interface agnostic - as long as the JSON is delivered with the expected key:values, it doesn't matter if a user has a client-side system to add up multiple addresses, or simply a form element that makes multiple POST requests. Mobile apps can also likewise access the API without need for special treatment, though here more work could be done to look into implementations for client-side apps/mobile apps that make many emails to handle disconnects/restarts.


Hope you enjoyed this half as much as I did working/writing it! Please let me know if you have any questions, and don't hesitate to reach out at aaron.m.manley@gmail.com.

**The End**