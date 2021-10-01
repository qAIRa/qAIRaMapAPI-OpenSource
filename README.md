[![Build Status](https://travis-ci.org/qAIRa/qairamapAPI-OpenSource.svg?branch=master)](https://travis-ci.org/qAIRa/qairamapAPI-OpenSource)  [![Coverage Status](https://coveralls.io/repos/github/qAIRa/qAIRaMapAPI-OpenSource/badge.svg?branch=master)](https://coveralls.io/github/qAIRa/qAIRaMapAPI-OpenSource?branch=master) [![Maintainability](https://api.codeclimate.com/v1/badges/2e414a349dfeaa89f538/maintainability)](https://codeclimate.com/github/qAIRa/qairamapAPI-OpenSource/maintainability) [![Documentation Status](https://readthedocs.org/projects/qairamapapi-opensource/badge/?version=latest)](https://qairamapapi-opensource.readthedocs.io/en/latest/?badge=latest)


#  qAIRa Map API

qAIRa Map API is an API to connect our [web](https://qairamap.qairadrones.com/), our qHAWAX and our database.
We work with modules, called qHAWAX, that capture data from gases, dust and environmental sensors (temperature, pressure, ultraviolet and noise).

You can look for a more detailed documentation [here.](https://qaira.github.io/)

Feel welcome to join our [forum](https://unicef-if.discourse.group/c/projects/qaira/11) with UNICEF. 
 
## Getting Started with installation

### Ubuntu, Mac & Windows
Clone or download the project to the device where it will be used.

```
git clone https://github.com/qAIRa/qAIRaMapAPI-OpenSource.git
```

### Prerequisites for every OS
1.  Having installed the postgreSQL driver.
   MacOS: 
```
      brew install postgresql 
``` 
   If facing issues with brew installation: https://docs.brew.sh/Installation

   Make sure to add the installed postgreSQL library to your PATH with the following

```
   export PG_HOME=/Library/PostgreSQL/14
   export PATH=$PATH:$PG_HOME/bin
```

   Windows: https://www.postgresql.org/

2. The API library requirement for psycopg2==2.8.5 makes the Python version equal to 3.8.5 a must.

3. For Windows: if you need the Microsoft C++ 14.0 or higher driver, you can download them from the [link](https://visualstudio.microsoft.com/visual-cpp-build-tools/). Just make sure you leave the defaulted selected options (including the optional). Storage: around 7 GB.

### Prerequisites Ubuntu & Mac
Now you have to open terminal
You must have an isolated environment by executing the following command:

```
python3 -m pip install virtualenv

python3 -m virtualenv venv

source venv/bin/activate

```
### Prerequisites Windows
Now you have to open CMD with administrator permissions
You must have an isolated environment by executing the following command: 

```
py -3 -m pip install virtualenv

py -3 -m virtualenv venv

source venv\Scripts\activate

```

### After that (for all Operating Systems)

First things first:

pip install psycopg2-binary

Now you have to run this command to install all the required libraries

```
pip install -r requirements.txt
```

Also, to set environment variables you need to run this command:

Windows PowerShell:
```
$Env:SQLALCHEMY_DATABASE_URI_OPEN='postgres://open_qaira:open_qaira@qairamap-open.c6xdvtbzawt6.us-east-1.rds.amazonaws.com:5432/open-qairamap'
```

Windows Command Prompt:
```
set SQLALCHEMY_DATABASE_URI_OPEN=postgres://open_qaira:open_qaira@qairamap-open.c6xdvtbzawt6.us-east-1.rds.amazonaws.com:5432/open-qairamap
```

MacOS or Ubuntu:
```
export SQLALCHEMY_DATABASE_URI_OPEN='postgres://open_qaira:open_qaira@qairamap-open.c6xdvtbzawt6.us-east-1.rds.amazonaws.com:5432/open-qairamap'
```
As a suggestion to test code faster, you should uncomment the code
```
app.run(debug = True)
```

Now you are ready to run the main code and test the API by yourself!

```
python run.py
```

If everything went well, the following should come out

```
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

Dont hesitate to contact us in [qAIRa Public Slack Channel](https://join.slack.com/t/qaira-publico/shared_invite/zt-e49w6375-9_vVmPdf8nFvXWfIvkagxw)

## FAQs

If you're encountering some oddities in the API, here's a list of resolutions to some of the problems you may be experiencing.

Why am I getting a 404?
The request could not be understood by the server due to malformed syntax. The client should not repeat the request without modifications.
I recommend you to see the response message it could be something like this: {"error":"No target qhawax_name in given json"}

Why am I getting a 405?

Not Allowed - It occurs when web server is configured in a way that does not allow you to perform an action for a particular URL. Maybe when you run an endpoint with GET instead of POST

Why am I not seeing all my results?
Most API calls accessing a list of resources (e.g., users, issues, etc.). If you're making requests and receiving an incomplete set of results, a response is specified in an unsupported content type.

Why am I getting a 500?
Server Mistake - Indicates that something went wrong on the server that prevent the server from fulfilling the request.

## Issues 

If you have found a bug in the project, you can file it here under the [“issues” tab](https://github.com/qAIRa/qAIRaMapAPI-OpenSource/issues). You can also request new features here. A set of templates for reporting issues and requesting features are provided to assist you (and us!).

## Pull Requests 

If you have received a confirmation about your issue, you can file a pull request under the [“pull request” tab](https://github.com/qAIRa/qAIRaMapAPI-OpenSource/pulls), please use the PR [“template”](https://github.com/qAIRa/qAIRaMapAPI-OpenSource/blob/master/.github/PULL_REQUEST_TEMPLATE/pull_request_template.md). 
You can also request new features here. 

## License
[GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt)
