##################
About this project
##################

qAIRaMap is an air monitoring project based on an API and Web Application.

In this documentation we are going to show you how to set up qAIRaMap API easily and quickly.

************************************
Getting Started with installation
************************************

#. In Ubuntu, Mac & Windows: Clone or download the project to the device where it will be used.

	#. git clone https://github.com/qAIRa/qAIRaMapAPI-OpenSource.git .

#. Set up isolated environment.

	You have to open terminal and run the following command:

	#. Ubuntu & Mac only .

		python3 -m pip install virtualenv

		python3 -m virtualenv venv

		source venv/bin/activate

	#. Windows only .

		py -3 -m pip install virtualenv

		py -3 -m virtualenv venv

		source venv\Scripts\activate

#. Install all require libraries (after enter to virtual env).

	pip install -r requirements.txt

#. Set environment variables (database and keys).

	export SQLALCHEMY_DATABASE_URI='******'

#. Run.

	python run.py

************************************
FAQs
************************************

If you're encountering some oddities in the API, here's a list of resolutions to some of the problems you may be experiencing.

#. Why am I getting a 404?.

	The request could not be understood by the server due to malformed syntax. The client should not repeat the request without modifications

#. Why am I getting a 405?.
	
	Not Allowed - It occurs when web server is configured in a way that does not allow you to perform an action for a particular URL. Maybe when you run an endpoint with GET instead of POST

#. Why am I not seeing all my results? .
	
	Most API calls accessing a list of resources (e.g., users, issues, etc.). If you're making requests and receiving an incomplete set of results, a response is specified in an unsupported content type.

#. Why am I getting a 500?.
	
	Server Mistake - Indicates that something went wrong on the server that prevent the server from fulfilling the request.

