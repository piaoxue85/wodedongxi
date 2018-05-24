Rem
Rem $Header: timesten/odbc/util/oraCache/scripts/initCacheAdminSchema.sql /main/15 2013/04/06 19:09:28 nabandi Exp $
Rem
Rem initCacheAdminSchema.sql
Rem
Rem Copyright (c) 2009, 2013, Oracle and/or its affiliates. 
Rem All rights reserved. 
Rem
Rem    NAME
Rem      initCacheAdminSchema.sql - <one-line expansion of the name>
Rem
Rem    DESCRIPTION
Rem      <short description of component this file declares/defines>
Rem
Rem    NOTES
Rem      <other useful comments, qualifications, etc.>
Rem
Rem    MODIFIED   (MM/DD/YY)
Rem    nabandi     04/05/13 - changing unique to primary key
Rem    nabandi     04/04/13 - Add tt_xx_log_space_stats
Rem    jomiller    11/26/12 - add create table for dbtbl_params table
Rem    jomiller    12/02/12 - add sql for new arinterval table
Rem    nabandi     08/20/12 - Fix reppeer table changes
Rem    nabandi     08/19/12 - Fix the primary key for reppeers table
Rem    nabandi     06/11/12 - Add more privileges to cache admin user
Rem    nabandi     06/05/12 - Add optional gv privilege to cache admin
Rem    jomiller    08/22/11 - add dbspecific_params
Rem    jomiller    08/02/11 - change metadata version number from 05 to 06
Rem    jomiller    08/17/10 - grant select on all_objects and all_synonyms
Rem    nabandi     04/09/09 - Correcting output format
Rem    nabandi     03/04/09 - Adding table space checks to the script
Rem    nabandi     03/02/09 - Fixing comments
Rem    nabandi     02/20/09 - Fixing the command line argument issue
Rem    nabandi     01/30/09 - This is the script that is to be run to setup all
Rem                           the required objects for cache admin in a manual
Rem                           installation path./
Rem    nabandi     01/30/09 - Created
Rem


/**
   This script will be installed for Oracle In-Memory Database Cache installations. 
   This script is used to manually install all the required Oracle In-Memory Database 
   Cache objects on Oracle under the cache admin user. This script is designed to be run 
   by the Database administrator or a super user on Oracle who has 
   the privileges to create a role, and grant connect, execute on dbms_lock privileges 
   to other users on Oracle. This script is the second script that should be run before 
   doing any Oracle In-Memory Database Cache operation. The first script is initCacheGlobalSchema.sql
   
            
   INPUT:  This script takes as input, the name of the cache admin user
   OUTPUT: This script creates a bunch of objects on Oracle which are used for
      	   Oracle In-Memory Database Cache.
	                
      An example where the super user on an Oracle instance "inst" is "dbadmin" and 
      the cache admin user is "cacheadminuser" is given below
            	 
	    sqlplus dbadmin@inst @initCacheAdminSchema.sql cacheadminuser
   
   Once this script runs to successful completion, it would have already created 
   TT_06_USER_COUNT, TT_06_AGENT_STATUS, TT_06_DB_PARAMS, TT_06_DBS, 
   TT_06_DDL_TRACKING, TT_06_DB_PARAMS, TT_06_AR_PARAMS, TT_06_CACHE_STATS
   TT_06_REPACTIVESTANDBY, TT_06_REPPEERS tables and the 
   TT_06_REPACTIVESTANDBY_T trigger on Oracle.

   NOTE: Unless absolutely necessary, we recommend the user to use 
      	 grantCacheAdminPrivileges.sql to grant all the required privileges 
	 for cache admin user. Any optional privileges (appended with suffix 
         of optional) may be revoked manually or removed from this script. It 
         is however recommended to grant those privileges to the cache admin user.
 
**/

SET ECHO OFF
SET FEEDBACK 1
SET NUMWIDTH 10
SET LINESIZE 80
SET TRIMSPOOL ON
SET TAB OFF
SET PAGESIZE 100
SET SERVEROUTPUT on;

PROMPT ;
PROMPT Please enter the administrator user id;
SET TERMOUT OFF;
SET VERIFY OFF;
DEFINE adminIdPr = '&&1';
SET TERMOUT ON;
PROMPT The value chosen for administrator user id is &1;
PROMPT ;


DECLARE

  adminId VARCHAR2(30) := '&1';
  ttprefix VARCHAR2(30) := 'TT_06_';
  tablespaceexists   NUMBER := -1;
  admintablespace    VARCHAR2(30); 
  counter NUMBER := 0;
  error NUMBER := 0;
  
  PROCEDURE executeString (str in VARCHAR2, errToIgnore NUMBER) is
      err NUMBER;
   BEGIN
   EXECUTE IMMEDIATE str;
   EXCEPTION WHEN OTHERS THEN
      err := SQLCODE;
      IF(err != errToIgnore) THEN DBMS_OUTPUT.PUT_LINE(SQLERRM );
      END IF;
   END;
   
BEGIN


DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE('***************** Initialization for cache admin begins ******************');

--------------- Granting the CREATE SESSION to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter || '. Granting the CREATE SESSION privilege to ' || UPPER(adminId));
counter := counter + 1;
executeString('GRANT CREATE SESSION TO ' || adminId, -1919);


DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter || '. Granting the CREATE ANY TYPE privilege to ' || UPPER(adminId));
counter := counter + 1;
executeString('GRANT CREATE ANY TYPE TO ' || adminId, -1919);


--------------- Granting the tt_cache_admin_role to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Granting the TT_CACHE_ADMIN_ROLE to ' || UPPER(adminId));
counter := counter + 1;
executeString('GRANT tt_cache_admin_role TO ' || adminId, -1919);


--------------- Granting execute privilege on DBMS_LOCK package to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Granting the DBMS_LOCK package privilege to ' || UPPER(adminId));
counter := counter + 1;
executeString('GRANT EXECUTE ON SYS.DBMS_LOCK TO ' || adminId, -1919);
--------------- Granting the SELECT ON ALL_OBJECTS to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the SELECT on SYS.ALL_OBJECTS privilege to ' || UPPER(adminId));
executeString('GRANT SELECT ON SYS.ALL_OBJECTS TO ' || adminId, -1919);
counter := counter + 1;

--------------- Granting the SELECT ON ALL_SYNONYMS to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the SELECT on SYS.ALL_SYNONYMS privilege to ' || UPPER(adminId));
executeString('GRANT SELECT ON SYS.ALL_SYNONYMS TO ' || adminId, -1919);
counter := counter + 1;

--------------- Granting the SELECT ON GV$LOCK to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the SELECT on SYS.GV$LOCK privilege to ' || UPPER(adminId) || ' (optional) ');
executeString('GRANT SELECT ON SYS.GV_$LOCK TO ' || adminId, -1919);
counter := counter + 1;

--------------- Granting the SELECT ON GV$SESSION to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the SELECT on SYS.GV$SESSION privilege  to ' || UPPER(adminId) || ' (optional) ');
executeString('GRANT SELECT ON SYS.GV_$SESSION TO ' || adminId, -1919);
counter := counter + 1;

--------------- Granting the SELECT ON SYS.DBA_DATA_FILES to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the SELECT on SYS.DBA_DATA_FILES privilege  to ' || UPPER(adminId) || ' (optional) ');
executeString('GRANT SELECT ON SYS.DBA_DATA_FILES TO ' || adminId, -1919);
counter := counter + 1;


--------------- Granting the SELECT ON SYS.USER_USERS to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the SELECT on SYS.USER_USERS privilege  to ' || UPPER(adminId) || ' (optional) ');
executeString('GRANT SELECT ON SYS.USER_USERS TO ' || adminId, -1919);
counter := counter + 1;

--------------- Granting the SELECT ON SYS.USER_FREE_SPACE to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the SELECT on SYS.USER_FREE_SPACE privilege  to ' || UPPER(adminId) || ' (optional) ');
executeString('GRANT SELECT ON SYS.USER_FREE_SPACE TO ' || adminId, -1919);
counter := counter + 1;


--------------- Granting the SELECT ON SYS.USER_TS_QUOTAS to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the SELECT on SYS.USER_TS_QUOTAS privilege  to ' || UPPER(adminId) || ' (optional) ');
executeString('GRANT SELECT ON SYS.USER_TS_QUOTAS TO ' || adminId, -1919);
counter := counter + 1;


--------------- Granting the SELECT ON SYS.USER_SYS_PRIVS to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the SELECT on SYS.USER_SYS_PRIVS privilege  to ' || UPPER(adminId) || ' (optional) ');
executeString('GRANT SELECT ON SYS.USER_SYS_PRIVS TO ' || adminId, -1919);
counter := counter + 1;



DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Checking if the cache administrator user has permissions on the default tablespace ');
counter := counter + 1;

EXECUTE IMMEDIATE 'SELECT count(*) FROM dba_ts_quotas ts, dba_users users WHERE ts.tablespace_name = users.default_tablespace and users.username= ''' || UPPER(adminId) || '''and ts.username=users.username' INTO tablespaceexists;

EXECUTE IMMEDIATE 'SELECT default_tablespace FROM dba_users users WHERE username= ''' || UPPER(adminId) || ''' ' INTO admintablespace;

IF (tablespaceexists = 0)  THEN
   DBMS_OUTPUT.PUT_LINE(chr (7) || '     No existing permission.');   
   DBMS_OUTPUT.NEW_LINE;
   DBMS_OUTPUT.PUT_LINE(counter ||'. Altering the cache administrator to grant unlimited tablespace on ' || admintablespace);   
   counter := counter + 1;   
   executeString('ALTER USER ' || UPPER (adminID) || ' QUOTA UNLIMITED ON ' || admintablespace, 1031);  
ELSE
   DBMS_OUTPUT.PUT_LINE(chr (7) || '     Permission exists');
END iF;
  

-- Create USER_COUNT table and assign permissions to the regular use role ---


DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Creating the '|| UPPER(adminId) || '.' || ttprefix || 'USER_COUNT table');
counter := counter + 1;
executeString('CREATE TABLE ' || adminId || '.' || ttprefix || 'user_count( schema varchar(32), tableName VARCHAR(32), object_id INT, userCount INT, createdOO NUMBER(1), logseq NUMBER, cacheGroup NUMBER, newTblFlag NUMBER(1), autorefreshType NUMBER(2), logLimit INT, needsRecoveryFlag NUMBER(1), markTS timestamp, constraint_name varchar(32), ddlTrkObjId int, ddlTrkObjOwner varchar2(30), ddlTrkObjName varchar2(30), ddlTrkProxyType int, hasDMLTrig char(1), oraBaseId int, oraBaseOwner varchar2(30), oraBaseName varchar2(30), oraBaseType int, oraTopId int, oraTopOwner varchar2(30), oraTopName varchar2(30), oraTopType int, UNIQUE(schema, tableName, cacheGroup, ddlTrkObjId, hasDMLTrig))', -955);



-- Create AGENT_STATUS table and assign permissions to the regular use role --

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Creating the '|| UPPER(adminId) || '.' || ttprefix || 'AGENT_STATUS table');
counter := counter + 1;

executeString( 'CREATE TABLE ' || adminId || '.' || ttprefix || 'agent_status(object_id INT, hash INT, bookmark NUMBER, reportTS TIMESTAMP, host varchar(200), datastore varchar(257), autoRefInterval interval day to second, owner varchar(32), cgname varchar(32), disabled INT, status VARCHAR2(20), ddsrecoverypt NUMBER, isDynamic CHAR(1) DEFAULT ''N'' NOT NULL, aliasOwner VARCHAR2(30), aliasName VARCHAR2(30), hasDMLTrig CHAR(1), cgType INT, UNIQUE(object_id, hash, aliasOwner, aliasName, hasDMLTrig))', -955);


-- Create SYNC_OBJS table and assign permissions to the regular use role ---

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Creating the '|| UPPER(adminId) || '.' || ttprefix || 'SYNC_OBJS table');
counter := counter + 1;

executeString( 'create table ' || adminId ||'.' || ttprefix || 'sync_objs(objectName varchar(100) unique not null)', -955);

-- Create SYNC_OBJS table index -------
DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Initialize '|| UPPER(adminId) || '.' || ttprefix || 'SYNC_OBJS table');
counter := counter + 1;

executeString ('insert into ' || adminId || '.' || ttprefix || 'sync_objs(objectName) values (''CacheDDLLock;'')',  -1);
executeString ('insert into ' || adminId || '.' || ttprefix || 'sync_objs(objectName) values (''LockTruncator'')',  -1);
executeString ('insert into ' || adminId || '.' || ttprefix || 'sync_objs(objectName) values (''OneTruncator'')',   -1);
executeString ('insert into ' || adminId || '.' || ttprefix || 'sync_objs(objectName) values (''OneMarker'')',      -1);
executeString ('insert into ' || adminId || '.' || ttprefix || 'sync_objs(objectName) values (''DDSMonitor1'')',    -1);
executeString ('insert into ' || adminId || '.' || ttprefix || 'sync_objs(objectName) values (''OneAlertWriter'')', -1);

-- Create DB_PARAMS table and assign permissions to the regular use role --
DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Creating the '|| UPPER(adminId) || '.' || ttprefix || 'DB_PARAMS table');
counter := counter + 1;

executeString( 'create table ' || adminId ||'.' || ttprefix || 'db_params(param VARCHAR2(50) NOT NULL UNIQUE, value VARCHAR2(200) NOT NULL)', -955);

executeString( 'INSERT INTO '|| UPPER(adminId)||'.' || ttprefix || 'db_params(param, value) VALUES (''AgentTimeout'',''0'')', -1);

executeString( 'INSERT INTO '|| adminId ||'.' || ttprefix || 'db_params(param, value) VALUES (''DeadDbRecovery'',''normal'')', -1);

executeString( 'INSERT INTO '|| adminId ||'.' || ttprefix || 'db_params(param, value) VALUES (''NearTblspaceFullThreshold'',''0'')', -1);

EXECUTE IMMEDIATE 'COMMIT';


-- Create DATABASES table and assign permissions to the regular use role --

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Creating the '|| UPPER(adminId) || '.' || ttprefix || 'DATA_BASES table');
executeString( 'create table ' || adminId ||'.' || ttprefix || 'databases(hash INT NOT NULL,host VARCHAR2(200) NOT NULL,datastore VARCHAR2(257) NOT NULL,heartbeat TIMESTAMP(0) WITH TIME ZONE,status VARCHAR2(20) NOT NULL,status_changed TIMESTAMP(0) WITH TIME ZONE,tsCheck TIMESTAMP(0) WITH TIME ZONE,UNIQUE(host,datastore),UNIQUE(hash))', -955);
counter := counter + 1;

-- Create DDL_L log table and assign permissions to the regular use role --

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Creating the '|| UPPER(adminId) || '.' || ttprefix || 'DDL_L table');
executeString( 'create table ' || adminId ||'.' || ttprefix || 'DDL_L(ddlTS timestamp, schema varchar2(30), sqltext varchar2(2000))', -955);
counter := counter + 1;


--------------- Create DDL_TRACKING table ---------------------------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Creating the '|| UPPER(adminId) || '.' || ttprefix || 'DDL_TRACKING table');
counter := counter + 1;

executeString( 'create table '||adminId||'.' || ttprefix || 'DDL_TRACKING (trackingstatus NUMBER(1))', -955);

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter || '. Enabling DDL tracking');
counter := counter + 1;

executeString( 'INSERT INTO '|| adminId ||'.' || ttprefix || 'DDL_TRACKING (trackingstatus) VALUES (0)', -1);

--------------- Create REPPEERS table ---------------------------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Creating the '|| UPPER(adminId) ||'.' || ttprefix || 'REPPEERS table');
counter := counter + 1;

executeString( 'CREATE TABLE ' || adminId ||'.' || ttprefix || 'RepPeers(replication_name char(31) not null,replication_owner char(31) not null,tt_store_id number(19,0) not null,subscriber_id number(19,0) not null,commit_timestamp number(19,0),commit_seqnum number(19,0),timerecv number(10,0),protocol number(10,0),track_id number(3,0) default 0 not null, grstate number(1) default 0, PRIMARY KEY(tt_store_id, track_id))', -955);
executeString( 'ALTER TABLE ' || adminId ||'.' || ttprefix || 'RepPeers modify track_id number(3,0) default 0 not null', -1442);
executeString( 'ALTER TABLE ' || adminId ||'.' || ttprefix || 'RepPeers add grstate number(1) default 0', -1430);
executeString( 'ALTER TABLE ' || adminId ||'.' || ttprefix || 'RepPeers drop primary key', 0);
executeString( 'ALTER TABLE ' || adminId ||'.' || ttprefix || 'RepPeers add primary key(tt_store_id, track_id)', 0);

   

--------------- Create REPACTIVESTANDBY table ---------------------------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Creating the '|| UPPER(adminId) ||'.' || ttprefix || 'REPACTIVESTANDBY table');
counter := counter + 1;
executeString( 'CREATE TABLE ' || adminId ||'.' || ttprefix || 'RepActiveStandby(tt_store_id1 number(19,0) not null,tt_store_id2 number(19,0) not null,ts1 number(19,0),ts2 number(19,0),role1 char(1),role2 char(1),state number(10,0),rep_checksum number(19,0),tt_store_pair_key varchar2(50),track_id number(3,0) default 0 not null, grstate number(1) default 0, constraint ' || ttprefix || 'RepActiveStandby_spk_u unique(tt_store_pair_key,track_id) deferrable)', -955);
executeString( 'CREATE INDEX ' || adminId ||'.' || ttprefix || 'RepActiveStandby_ix ON '|| adminId || '.' || ttprefix || 'REPACTIVESTANDBY (tt_store_id1 ,tt_store_id2)', -955);
executeString( 'ALTER TABLE ' || adminId ||'.' || ttprefix || 'RepActiveStandby modify track_id number(3,0) default 0 not null', -1442);
executeString( 'ALTER TABLE ' || adminId ||'.' || ttprefix || 'RepActiveStandby add grstate number(1) default 0', -1430);
executeString( 'ALTER TABLE ' || adminId ||'.' || ttprefix || 'RepActiveStandby drop constraint ' || ttprefix || 'RepActiveStandby_spk_u', -2261);
executeString( 'ALTER TABLE ' || adminId ||'.' || ttprefix || 'RepActiveStandby add constraint ' || ttprefix || 'RepActiveStandby_spk_u unique (tt_store_pair_key, track_id)', -2261);


--------------- Create REPACTIVESTANDBY_T trigger ---------------------------


DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Creating the '|| UPPER(adminId) ||'.' || ttprefix || 'REPACTIVESTANDBY_T trigger');
counter := counter + 1;

executeString( 'CREATE TRIGGER '|| adminId || '.' || ttprefix || 'RepActiveStandby_t BEFORE INSERT OR UPDATE OF TT_STORE_ID1, TT_STORE_ID2 ON ' || adminId ||'.' || ttprefix || 'RepActiveStandby FOR EACH ROW DECLARE tmp int; tmp_c char(1); BEGIN IF (:new.TT_STORE_ID1 > :new.TT_STORE_ID2) THEN tmp := :new.TT_STORE_ID1; :new.TT_STORE_ID1 := :new.TT_STORE_ID2; :new.TT_STORE_ID2 := tmp; tmp := :new.TS1; :new.TS1 := :new.TS2; :new.TS2 := tmp; tmp_c := :new.role1; :new.role1 := :new.role2; :new.role2 := tmp_c; END IF; :new.TT_STORE_PAIR_KEY := :new.TT_STORE_ID1 ||''' || ':' || '''|| :new.TT_STORE_ID2; END;', -4081);

--------------- Create CACHE_STATS table ---------------------------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Creating the '|| UPPER(adminId) ||'.' || ttprefix || 'CACHE_STATS table');
counter := counter + 1;
executeString( 'CREATE TABLE ' || adminId ||
'.' || ttprefix || 'CACHE_STATS(statistic VARCHAR2(30) NOT NULL, value NUMBER, updated TIMESTAMP(0) WITH TIME ZONE, constraint ' || ttprefix || 'Cache_Stats_S_U unique(statistic) deferrable)', -955);

-- Create AR_PARAMS table and assign permissions to the regular use role --

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter || '. Creating the '|| UPPER(adminId) || '.' || ttprefix || 'AR_PARAMS table');
counter := counter + 1;

executeString( 'create table ' || adminId ||'.' || ttprefix || 'ar_params(param VARCHAR2(50) NOT NULL,tblowner VARCHAR2(30) NOT NULL,tblname VARCHAR2(30) NOT NULL,value VARCHAR2(200) NOT NULL,UNIQUE(param,tblowner,tblname))', -955);

-- Create DBSPECIFIC_PARAMS table and assign permissions to the regular use role --

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter || '. Creating the '|| UPPER(adminId) || '.' || ttprefix || 'DB_SPECIFIC_PARAMS table');
counter := counter + 1;

executeString( 'create table ' || adminId ||'.' || ttprefix || 'dbspecific_params(host VARCHAR2(200) NOT NULL, datastore VARCHAR2(257) NOT NULL, param VARCHAR2(50) NOT NULL,value VARCHAR2(200) NOT NULL,UNIQUE(host,datastore,param))', -955);

-- Create ARINTERVAL_PARAMS table and assign permissions to the regular use role --

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter || '. Creating the '|| UPPER(adminId) || '.' || ttprefix || 'ARInterval_Params table');
counter := counter + 1;

executeString( 'create table ' || adminId ||'.' || ttprefix || 'arinterval_params(host VARCHAR2(200) NOT NULL, database VARCHAR2(257) NOT NULL, arinterval INTEGER NOT NULL, param VARCHAR2(50) NOT NULL, value VARCHAR2(200), PRIMARY KEY(host, database, arinterval, param))', -955);

-- Create DBTBL_PARAMS table and assign permissions to the regular use role --

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter || '. Creating the '|| UPPER(adminId) || '.' || ttprefix || 'DBTBL_PARAMS table');
counter := counter + 1;

executeString( 'create table ' || adminId ||'.' || ttprefix || 'dbtbl_params(param VARCHAR2(50) NOT NULL, host VARCHAR2(200) NOT NULL, datastore VARCHAR2(257) NOT NULL, tblowner VARCHAR2(30) NOT NULL, tblname VARCHAR2(30) NOT NULL, value VARCHAR2(200) NOT NULL, PRIMARY KEY(param,host,datastore,tblowner,tblname))', -955);


-- Create LOG_SPACE_STATS table and assign permissions to the regular use role ---


DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter ||'. Creating the '|| UPPER(adminId) || '.' || ttprefix || 'LOG_SPACE_STATS table');
counter := counter + 1;
executeString('CREATE TABLE ' || adminId || '.' || ttprefix || 'log_space_stats ( object_id INT, logSpaceFragmentationPCT NUMBER(3) default 0, logSpaceFragmentationTS TIMESTAMP, logSpaceDeFragCnt NUMBER(3) default 0, logSpaceDeFragTS TIMESTAMP, PRIMARY KEY (object_id))', -955);




IF (error = 0) THEN
   DBMS_OUTPUT.NEW_LINE;
   DBMS_OUTPUT.PUT_LINE('********* Initialization for cache admin user done successfully *********');
   DBMS_OUTPUT.NEW_LINE;
ELSE
   DBMS_OUTPUT.NEW_LINE;
   DBMS_OUTPUT.PUT_LINE('** Initialization for cache admin user could not be successfully done  **');
   DBMS_OUTPUT.NEW_LINE;
END IF;

END;
/

undefine 1;
