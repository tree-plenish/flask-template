from flask import Flask, render_template

#########################################################################
# Database SQL Operations import 
# (remove .gitmodules, the tech_team_database subdirectory, and the
# following lines if not connecting app to database.)
#########################################################################
from tech_team_database.dependencies.DatabaseSQLOperations import TpSQL
tpSQL = TpSQL(schema='tp2022')
#########################################################################
# End Database SQL Operations import
#########################################################################

application = Flask(__name__)

# landing page
@application.route('/index')
@application.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    application.run()