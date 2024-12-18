import pytds
from adsToolBox.loadEnv import env
from adsToolBox.dbMssql import dbMssql
from adsToolBox.logger import Logger
from adsToolBox.global_config import set_timer

logger = Logger(Logger.DEBUG, "AdsLogger")
env = env(logger, 'C:/Users/mvann/Desktop/ADS/Projects/adsGenericFunctions/adsToolBox/demo/.env')
set_timer(True)

source_mssql = dbMssql({'database': env.MSSQL_DWH_DB,
                      'user': env.MSSQL_DWH_USER,
                      'password': env.MSSQL_DWH_PWD,
                      'port': env.MSSQL_DWH_PORT,
                      'host': env.MSSQL_DWH_HOST}, logger, batch_size=10)
source_mssql.connect()


source_mssql.sqlExec("""
DROP TABLE D365_CustomersV3_encode;
CREATE TABLE D365_CustomersV3_encode (
    Colonne1 VARCHAR(100),
    Colonne2 INT,
    Colonne3 datetime NULL,
);
""")

rows = [("Adhérent", None, "2023-04-27 00:00:00.000") for _ in range(30)]
cols = ["Colonne1", "Colonne2", "Colonne3"]



'''
2023-04-27 00:00:00.000
2023-03-21 00:00:00.000
'''

res = source_mssql.insertBulk("D365_CustomersV3_encode", cols, rows)
for i in res:
    print(len(i), i)