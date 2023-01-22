# flask-template

Minimal Flask template for Tree-Plenish. Generic Tree-Plenish styles are included.

Detailed setup guide for beginners below. Note that the commands are for linux/unix systems, so you may need to google the equivalent command for your machine.

## Setup guide
Make sure you have git, python3.7+, and pip installed.

Click `Use this Template` > `Create a New Repository`, then set the owner to be `tree-plenish` and give it a new name. In your new repository, click `Clone` and copy the HTTP URL. Then run
```
git clone <YOUR_HTTP_URL> --recurse-submodules 
cd <YOUR_REPO_NAME>
```
### Database connectivity? 
If your app does not need to connect to the database, remove the `tech_team_database` submodule, the `.gitmodules` file, and the DatabaseSQLOperations import in `application.py`.
### Set up database credentials
Omit this step if your app does not connect to the database.

Make sure your Tree-Plenish AWS credentials (`~/.aws/credentials` and `~/.aws/config`) are setup and make sure the database library can find your AWS credentials. If you have your tree-plenish credentials as the default credentials in your `~/.aws/credentials` file, everything should be set. However, if you have a separate profile for the tree-plenish credentials (which the setup.sh script assumes), you need to set the AWS_PROFILE environment variable to the name of that profile. For example, if your `~/.aws/credentials` file looks like this:
```
[default]
aws_access_key_id = **********
aws_secret_access_key = **********

[tree-plenish]
aws_access_key_id = <TREE_PLENISH_KEY_ID_HERE>
aws_secret_access_key = <TREE_PLENISH_SECRET_ACCESS_KEY_HERE>
```
You will need to run:
```
setenv AWS_PROFILE=tree-plenish
```

### Create a virtual environment and install dependencies

Install python virtual environments:
```
pip install virtualenv
```
Create a new virtual environment and activate it:
```
python3 -m virtualenv venv
source venv/bin/activate
```
Install required dependencies for the Flask app into the virtual environment:
```
pip3 install -r requirements.txt
```
To deactivate the virtual environment later:
```
deactivate
```
### Run locally
Because Elastic Beanstalk expects the flask app to be named `application`, set the `FLASK_APP` environment variable to `application.py` before running Flask locally. To run in debug mode locally, set the environment variable instead of using the parameter in `application.run()` so that the production app is not in debug mode. For example, on Linux:
```
setenv FLASK_ENV=development
setenv FLASK_APP=application.py
```
You can set an alias for these commands (and activating the virtual environment) for easy setup whenever you are developing.

To run the flask app locally:
```
flask run
```
You should see messages that say that your development server is starting.
```
 * Serving Flask app 'application.py' (lazy loading)
 * Environment: development
 * Debug mode: on
INFO: 2022-10-14 17:59:38: Found credentials in shared credentials file: ~/.aws/credentials
INFO: 2022-10-14 17:59:38: Found credentials in shared credentials file: ~/.aws/credentials
INFO: 2022-10-14 17:59:38: SUCCESS! Boto3 services were initialized.
INFO: 2022-10-14 17:59:38:  * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
INFO: 2022-10-14 17:59:38:  * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 401-392-724
INFO: 2022-10-14 17:59:38: Found credentials in shared credentials file: ~/.aws/credentials
INFO: 2022-10-14 17:59:38: Found credentials in shared credentials file: ~/.aws/credentials
INFO: 2022-10-14 17:59:39: SUCCESS! Boto3 services were initialized.
```

Note the host and port that the app is running on (http://127.0.0.1:5000 above). Put this in your browser to access the landing page.

### Set up auto-deployment
Do this only when you are ready to deploy your app!
- In Github, go to Settings > Developer Settings > Personal Access Tokens > Tokens (classic) > Generate New Token. Give the token a name, select the `repo` scope, and save. Copy the value of your personal access token.
- In your project repository, go to Settings > Secrets and variables > actions. Add the following repository secrets:
    - `PERSONAL_ACCESS_TOKEN`: set the value to your personal access token
    - `ACCESS_KEY_ID`: set the value to your AWS ACCESS_KEY_ID
    - `SECRET_ACCESS_KEY`: set the value to your AWS SECRET_ACCESS_KEY
- Uncomment the workflow trigger in `.github/workflows/main.yml`
- Replace `<ENVIRONMENT_NAME_HERE>` with the name of your elastic beanstalk flask environment
- Replace `<APP_NAME_HERE>` with the name of your flask app
- Push changes to github

App updates will automatically re-deploy to Elastic Beanstalk on every push to the main branch via the Github actions workflow in `.github/workflows/main.yml`. Relevant updates to dependencies (like `tech_team_database`) will require manual re-run of the `deploy` workflow to update the deployed version, since the workflow checks out the latest version for deployment. Any files in the repository that should not be deployed should be added to `.ebignore`.

## Development practices

### Installing packages
Always activate the virtual environment when you are developing on this project so that any additional installations you make are installed in the virtual environment.
If you do include additional installations, make sure to run
```
pip freeze > requirements.txt
```
to update `requirements.txt`. This ensures that the deployed application will have all the required dependencies installed.

### Directory structure
Include Jinja html templates in the `templates` subdirectory, and all other static files (images, attachments, CSS files, JS files, etc.) that are part of the app in `static`. The top level `images` directory is only for images used in this README. When referencing other files from a template, do not use the relative path, as this may cause problems for shared template bases if templates are reorganized into different subfolders. Instead, use `url_for`. For example, use
```
<link rel="stylesheet" href="{{ url_for('static', filename='css/form.css') }}">
```
instead of
```
<link rel="stylesheet" href="../static/css/form.css'">
```

### Dotfiles
- `.gitignore`: any files or directories listed in this file will be ignored by git and not tracked/committed/pushed to the repo.
- `.ebignore`: any files or directories listed in this file will be ignored by elastic beanstalk (will not be included in deployed app)
- `.gitmodules`: contains submodule mapping for tech_team_database

### Helpful tips
It may be convenient to set an alias for the setup commands to use whenever you start developing. For example, in your shell configuration file (e.g. `~/.bashrc`, `~/.zshrc`, etc.):
```
tp-app () {
    cd <put the absolute path to your local copy of the repo here!>
    source venv/bin/activate
    setenv FLASK_ENV=development
    setenv FLASK_APP=application.py
    setenv AWS_PROFILE=tree-plenish
}
```

### Resources
- Flask: https://flask.palletsprojects.com/en/2.2.x/
- Jinja HTML: https://jinja.palletsprojects.com/en/3.1.x/templates/
