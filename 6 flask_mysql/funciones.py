from os import environ
def areaConfigDB(app):
    app.config['MYSQL_HOST']=environ.get('MYSQL_HOST')
    app.config['MYSQL_USER']=environ.get('MYSQL_USER')
    app.config['MYSQL_PASSWORD']=environ.get('MYSQL_PASSWORD')
    app.config['MYSQL_DB']=environ.get('MYSQL_DB')
    app.config['MYSQL_PORT']=3306
    return app
