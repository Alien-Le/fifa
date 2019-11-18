# fifa
The FIFA Players Analyzer  
  
To fill mysql database with the data make the following steps:  
1) Install mysql server if it is not installed  
2) Add somewhere the config file named config.py with the next code:  
MYSQL = {  
    'host': {HOST},  
    'port': {PORT},  
    'user': {USER},  
    'passwd': {PASSWORD},  
    'db': 'fifa',  
    'autocommit': True,  
    'charset': 'utf8'  
}  
and replace the values in braces with your database connection details.  
2) ensure that `pandas` and `pymysql` python modules are being installed  
3) run python3 ./fill_database.py --config_path {THE_PATH_WHERE_THE_CONFIG_IS_SAVED}  
  
Working example you can see here: http://alien-cafe.net/fifa/
