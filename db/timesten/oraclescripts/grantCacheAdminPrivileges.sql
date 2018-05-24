Rem
Rem $Header: timesten/odbc/util/oraCache/scripts/grantCacheAdminPrivileges.sql /main/13 2014/03/17 10:32:10 shnandan Exp $
Rem
Rem grantCacheAdminPrivileges.sql
Rem
Rem Copyright (c) 2009, 2014, Oracle and/or its affiliates. 
Rem All rights reserved.
Rem
Rem    NAME
Rem      grantCacheAdminPrivileges.sql - <one-line expansion of the name>
Rem
Rem    DESCRIPTION
Rem      <short description of component this file declares/defines>
Rem
Rem    NOTES
Rem      <other useful comments, qualifications, etc.>
Rem
Rem    MODIFIED   (MM/DD/YY)
Rem    shnandan    03/17/13 - Bug 16390772: CREATE TYPE privilege is sufficient
Rem			      in place of CREATE ANY TYPE.
Rem    nabandi     06/11/12 - Add more privileges to cache admin user
Rem    nabandi     06/05/12 - Add optional gv privilege to cache admin
Rem    jomiller    08/02/11 - change metadata version number from 05 to 06
Rem    jomiller    08/17/10 - grant select to all_objects and all_synonyms
Rem    nabandi     03/22/10 - Altering the create any procedure to create
Rem                           procedure
Rem    jomiller    12/21/09 - add execute dbms_lob privilege
Rem    nabandi     04/09/09 - Correcting output format
Rem    nabandi     03/04/09 - Adding table space checks to the script
Rem    nabandi     03/02/09 - Fixing comments
Rem    nabandi     02/20/09 - Fixing the command line argument issue
Rem    nabandi     01/30/09 - This is the script to be run for granting all the
Rem                           required privileges to cache admin user. This is
Rem                           to be used after run initCacheGlobalSchema.sql.
Rem    nabandi     01/30/09 - Created
Rem


/**

   This script will be installed for Oracle In-Memory Database Cache installations. This script 
   is used to grant all the privileges required on Oracle for the  cache admin user. This script
   is designed to be run by the Database administrator or a super user on Oracle who has 
   the privileges to create a role, and grant connect, execute on dbms_lock privileges 
   to other users on Oracle. This is in addition to the create resource, trigger, 
   procedure privileges. This script is the second script that should be run before 
   doing any Oracle In-Memory Database Cache operation. The first script is initCacheGlobalSchema.sql.
   
            
   INPUT: This script takes as input, the name of the cache admin user
   OUTPUT: This script grants the list of all privileges and roles to the cache admin user.
	                
      An example where the super user on an Oracle instance "inst" is "dbadmin" and 
      the cache admin user is "cacheadminuser" is given below
            	 
	    sqlplus dbadmin@inst @grantCacheAdminPrivileges.sql cacheadminuser
    
      NOTE :  Any optional privileges (appended with suffix of optional) may be revoked 
              manually or removed from this script. It is however recommended to grant 
              those privileges to the cache admin user.
 
   
**/


SET ECHO OFF
SET FEEDBACK 0
SET NUMWIDTH 10
SET LINESIZE 80
SET TRIMSPOOL ON
SET TAB OFF
SET PAGESIZE 100

SET SERVEROUTPUT ON;
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
  tableSpaceForTimesTenUser VARCHAR2(30);
  timestenuserexists NUMBER := -1;
  timestenroleexists NUMBER := -1;
  tablespaceexists   NUMBER := -1;
  admintablespace    VARCHAR2(30);
  error NUMBER := 0;
  counter NUMBER := 0;
	       
  PROCEDURE executeString (str in VARCHAR2, errToIgnore NUMBER) is
      err NUMBER;
   BEGIN
   EXECUTE IMMEDIATE str;
   EXCEPTION WHEN OTHERS THEN
      err := SQLCODE;
      IF(err != errToIgnore) THEN 
      	 DBMS_OUTPUT.PUT_LINE(SQLERRM );
	 error := 1;
      END IF;
   END;

         
BEGIN

EXECUTE IMMEDIATE 'select count(*) from all_users where username = ''TIMESTEN''' into timestenuserexists;

EXECUTE IMMEDIATE 'select count(*) from dba_roles where role = ''TT_CACHE_ADMIN_ROLE''' into timestenroleexists;

IF (timestenuserexists = 0 OR timestenroleexists = 0) THEN

DBMS_OUTPUT.PUT_LINE(chr(1));
DBMS_OUTPUT.PUT_LINE(chr (5) || '    TIMESTEN schema needs to be created before this script is run');
DBMS_OUTPUT.PUT_LINE(chr (5) || '    Please run initCacheGlobalSchema.sql first');

ELSE

   
DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE('***************** Initialization for cache admin begins ******************');

--------------- Granting the CREATE SESSION to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the CREATE SESSION privilege to ' || UPPER(adminId));
executeString('GRANT CREATE SESSION TO ' || adminId, -1919);
counter := counter + 1;

--------------- Granting the tt_cache_admin_role to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the TT_CACHE_ADMIN_ROLE to ' || UPPER(adminId));
executeString('GRANT tt_cache_admin_role TO ' || adminId, -1919);
counter := counter + 1;

--------------- Granting execute privilege on DBMS_LOCK package to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the DBMS_LOCK package privilege to ' || UPPER(adminId));
executeString('GRANT EXECUTE ON SYS.DBMS_LOCK TO ' || adminId, -1919);
counter := counter + 1;

--------------- Granting the CREATE SEQUENCE to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the CREATE SEQUENCE privilege to ' || UPPER(adminId));
executeString('GRANT CREATE SEQUENCE TO ' || adminId, -1919);
counter := counter + 1;

----------------- Granting the CREATE CLUSTER to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the CREATE CLUSTER privilege to ' ||
UPPER(adminId));
executeString('GRANT CREATE CLUSTER TO ' || adminId, -1919);
counter := counter + 1;

---------------- Granting the CREATE OPERATOR to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the CREATE OPERATOR privilege to ' ||
UPPER(adminId));
executeString('GRANT CREATE OPERATOR TO ' || adminId, -1919);
counter := counter + 1;

---------------- Granting the CREATE INDEXTYPE to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the CREATE INDEXTYPE privilege to ' ||
UPPER(adminId));
executeString('GRANT CREATE INDEXTYPE TO ' || adminId, -1919);
counter := counter + 1;

---------------- Granting the CREATE TABLE to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the CREATE TABLE privilege to ' ||
UPPER(adminId));
executeString('GRANT CREATE TABLE TO ' || adminId, -1919);
counter := counter + 1;


--------------- Granting the CREATE PROCEDURE to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the CREATE PROCEDURE  privilege to ' || UPPER(adminId));
executeString('GRANT CREATE PROCEDURE TO ' || adminId, -1919);
counter := counter + 1;


--------------- Granting the CREATE ANY TRIGGER to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the CREATE ANY TRIGGER  privilege to ' || UPPER(adminId));
executeString('GRANT CREATE ANY TRIGGER TO ' || adminId, -1919);
counter := counter + 1;

--------------- Granting the UNLIMITED TABLESPACE to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the GRANT UNLIMITED TABLESPACE privilege to ' || UPPER(adminId));
executeString('GRANT UNLIMITED TABLESPACE TO ' || adminId, -1919);
counter := counter + 1;

--------------- Granting the EXECUTE DBMS_LOB to the admin -------

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Granting the DBMS_LOB package privilege to ' || UPPER(adminId));
executeString('GRANT EXECUTE ON SYS.DBMS_LOB TO ' || adminId, -1919);
counter := counter + 1;

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


DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter||'. Checking if the cache administrator user has permissions on the default tablespace ');
counter := counter + 1;

EXECUTE IMMEDIATE 'SELECT count(*) FROM dba_ts_quotas ts, dba_users users WHERE ts.tablespace_name = users.default_tablespace and users.username= ''' || UPPER(adminId) || '''and ts.username=users.username' INTO tablespaceexists;

EXECUTE IMMEDIATE 'SELECT default_tablespace FROM dba_users users WHERE username= ''' || UPPER(adminId) || ''' ' INTO admintablespace;

IF (tablespaceexists = 0)  THEN
   DBMS_OUTPUT.PUT_LINE(chr (7) || '     No existing permission.');
   DBMS_OUTPUT.NEW_LINE;   
   DBMS_OUTPUT.PUT_LINE(counter||'. Altering the cache administrator to grant unlimited tablespace on ' || admintablespace);
   executeString('ALTER USER ' || UPPER (adminID) || ' QUOTA UNLIMITED ON ' || admintablespace, 1031);  
ELSE
   DBMS_OUTPUT.PUT_LINE(chr (7) || '     Permission exists');
END iF;
counter := counter + 1;
  

DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE(counter || '. Granting the CREATE TYPE privilege to ' || UPPER(adminId));
executeString('GRANT CREATE TYPE TO ' || adminId, -1919);
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



IF (error = 0) THEN
   DBMS_OUTPUT.NEW_LINE;
   DBMS_OUTPUT.PUT_LINE('********* Initialization for cache admin user done successfully *********');
   DBMS_OUTPUT.NEW_LINE;
ELSE
   DBMS_OUTPUT.NEW_LINE;
   DBMS_OUTPUT.PUT_LINE('** Initialization for cache admin user could not be successfully done  **');
   DBMS_OUTPUT.NEW_LINE;
END IF;

END IF;


END;
/

undefine 1;

