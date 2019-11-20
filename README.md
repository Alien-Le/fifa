# Fifa

## The FIFA Players Analyzer  
  
To fill mysql database with the data make the following steps:

1) Install mysql server if it is not installed

2) Add somewhere the config file named `config.py` with the next code:

    ```python
    MYSQL = {  
        'host': {HOST},  
        'port': {PORT},  
        'user': {USER},  
        'passwd': {PASSWORD},  
        'db': 'fifa',  
        'autocommit': True,  
        'charset': 'utf8'  
    }
    ```

and replace the values in braces with your database connection details.

1) Ensure that `pandas` and `pymysql` python modules are being installed

2) Run `python3 ./fill_database.py --config_path {THE_PATH_WHERE_THE_CONFIG_IS_SAVED}`

Working example you can see here: [Fifa](http://alien-cafe.net/fifa/)
