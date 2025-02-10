import os 
import oracledb
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

db_user = "ADMIN"
db_password = "Martinisgoat1!"
db_connect = "(description= (retry_count=20)(retry_delay=3)(address=(protocol=tcps)(port=1521)(host=adb.us-ashburn-1.oraclecloud.com))(connect_data=(service_name=g14f988a10ff21c_lmcin003database_tp.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))"

def init_session(connection, requestedTag_ignored):
    cursor = connection.cursor()
    cursor.execute("""
        ALTER SESSION SET
          TIME_ZONE = 'UTC'
          NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI'""")

def start_pool():

    # Generally a fixed-size pool is recommended, i.e. pool_min=pool_max.
    # Here the pool contains 4 connections, which is fine for 4 conncurrent
    # users.
    #
    # The "get mode" is chosen so that if all connections are already in use, any
    # subsequent acquire() will wait for one to become available.

    pool_min = 1
    pool_max = 2
    pool_inc = 0
    pool_gmd = oracledb.SPOOL_ATTRVAL_WAIT

    print("Connecting to", db_connect)

    pool = oracledb.SessionPool(user=db_user,
                                 password=db_password,
                                 dsn=db_connect,
                                 min=pool_min,
                                 max=pool_max,
                                 increment=pool_inc,
                                 threaded=True,
                                 getmode=pool_gmd,
                                 sessionCallback=init_session)

    return pool


app = Flask(__name__)

def output_type_handler(cursor, metadata):

    def out_converter(d):
        print( d )
        if d is None:
            return ""
        else:
            return d

    if metadata.type_code is oracledb.DB_TYPE_NUMBER:
        return cursor.var(oracledb.DB_TYPE_VARCHAR, arraysize=cursor.arraysize, outconverter=out_converter, convert_nulls=True)


###############################################
#Tables#

