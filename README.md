#  qAIRa Map API

qAIRa Map API is an API to connect our [web](https://qairamap.qairadrones.com/), our qHAWAX and our database.
We work with modules, called qHAWAX, that capture data from gases, dust and environmental sensors (temperature, pressure, ultraviolet and noise).

## Getting Started with installation

### Ubuntu, Mac & Windows
Clone or download the project to the device where it will be used.

```
git clone https://github.com/qAIRa/qairamapAPI.git
```

### Prerequisites Ubuntu & Mac
Now you have to open terminal
You must have an isolated environment by executing the following command: py -3 -m pip install virtualenv

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

venv\Scripts\activate

```

### After that (for all Operating Systems)

Now you have to run this command to install all require libraries

```
pip install -r requirements.txt
```

Also, to set environment variables you need to run this command:


```
export MAIL_DEFAULT_RECEIVER=********

export SQLALCHEMY_DATABASE_URI='******'

export SECRET_KEY=*******

export MAIL_USERNAME=*******

export MAIL_PASSWORD=*******
```
Now you are ready to run the main code

```
python run.py
```

If everything went well, the following should come out

```
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

Dont hesitate to contact us in [qAIRa Public Slack Channel](https://join.slack.com/t/qaira-publico/shared_invite/zt-e49w6375-9_vVmPdf8nFvXWfIvkagxw)

## Issues 

If you have found a bug in the project, you can file it here under the [“issues” tab](https://github.com/qAIRa/qairamapAPI/issues). You can also request new features here. A set of templates for reporting issues and requesting features are provided to assist you (and us!).

## Pull Requests 

If you have received a confirmation about your issue, you can file a pull request under the [“pull request” tab](https://github.com/qAIRa/qairamapAPI/pulls), please use the PR [“template”](https://github.com/qAIRa/qairamapAPI/blob/master/.github/PULL_REQUEST_TEMPLATE/pull_request_template.md). 
You can also request new features here. 

## License
[GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt)
