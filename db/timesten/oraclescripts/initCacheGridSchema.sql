Rem
Rem $Header: timesten/odbc/util/oraCache/scripts/initCacheGridSchema.sql /main/8 2011/08/10 14:24:59 nabandi Exp $
Rem
Rem initCacheGridSchema.sql
Rem
Rem Copyright (c) 2009, 2011, Oracle and/or its affiliates. 
Rem All rights reserved. 
Rem
Rem    NAME
Rem      initCacheGridSchema.sql - <one-line expansion of the name>
Rem
Rem    DESCRIPTION
Rem      <short description of component this file declares/defines>
Rem
Rem    NOTES
Rem      <other useful comments, qualifications, etc.>
Rem
Rem    MODIFIED   (MM/DD/YY)
Rem    jomiller    08/02/11 - change metadata version number from 05 to 06
Rem    nabandi     04/09/09 - Correcting output format
Rem    nabandi     03/02/09 - Fixing comments
Rem    nabandi     02/20/09 - Fixing the command line argument issue
Rem    nabandi     01/30/09 - This is the initialization script to be run to
Rem                           setup a grid for the manual installation path.
Rem    nabandi     01/30/09 - Created
Rem


/**
   This script will be installed for Oracle In-Memory Database Cache installations. 
   This script is used to manually install all the required Oracle In-Memory Database Cache 
   objects on Oracle under the cache admin user. This script
   is designed to be run by the Database administrator or a super user on Oracle who has 
   the privilege to create objects in the admin user schema on Oracle. This script is the third 
   script that should be run before doing any Oracle In-Memory Database Cache operation. The first 
   script is initCacheGlobalSchema.sql and the second one is initCacheAdmin.sql
   
            
   INPUT: This script takes as input, the name of the cache admin user and the name of 
      	  the grid we want to install
   OUTPUT: This script creates a bunch of objects on Oracle which are used for Cache Grid under the
          admin user.
	                
      An example where the super user on an Oracle instance "inst" is "dbadmin" and 
      the cache admin user is "cacheadminuser" and grid name is "gridname" is given below
            	 
	    sqlplus dbadmin@inst @initCacheAdmin.sql "cacheadminuser" "gridname"
   
   Once this script runs to successful completion, it would have already created 
   TT_06_${GRIDNAME}_${GRIDID}_NODEID, TT_06_${GRIDNAME}_${GRIDID}_NODEINFO and 
   TT_06_${GRIDNAME}_${GRIDID}_CGGROUPDEFS tables. Here GRIDNAMEis the name of the grid passed
   to the script. GRIDID is the ID automatically assigned to this grid

   NOTE: Unless absolutely necessary, we recommend the user to use 
      	 grantCacheAdminPrivileges.sql to grant all the required privileges 
	 for cache admin user.
 

**/

SET ECHO OFF
SET FEEDBACK 1
SET NUMWIDTH 10
SET LINESIZE 80
SET TRIMSPOOL OFF
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


PROMPT ;
PROMPT Please enter the name of the grid;
SET TERMOUT OFF;
SET VERIFY OFF;
DEFINE adminIdPr = '&&2';
SET TERMOUT ON;
PROMPT The value chosen for the grid is &2;
PROMPT ;

DECLARE
  ttprefix VARCHAR2(30) := 'TT_06_';
  adminId VARCHAR2(30) := '&1';    
  gridName VARCHAR2(30) := '&2';
  gridId  NUMBER(38) := -1;
  alreadyExists  NUMBER(38) := -1;
  error NUMBER := 0;
  
  CURSOR selGridIdCursor IS SELECT gridIdNum FROM timesten.tt_gridid FOR UPDATE;
  type rc is REF CURSOR;
  checkGridExists rc;
  
  PROCEDURE executeString (str IN VARCHAR2, errToIgnore NUMBER) IS
      err NUMBER;
   BEGIN
   EXECUTE IMMEDIATE str;
   EXCEPTION WHEN OTHERS THEN
      err := SQLCODE;
      IF(err != errToIgnore) THEN DBMS_OUTPUT.PUT_LINE(SQLERRM);
      	 error := err;
      END IF;
   END;
   
BEGIN


DBMS_OUTPUT.NEW_LINE;
DBMS_OUTPUT.PUT_LINE('***************** Creation of cache grid begins ******************');

-- check if a grid with the name exists
open checkGridExists for  'SELECT grididnum FROM timesten.tt_gridinfo tt where tt.gridname = ''' || UPPER (gridName) || ''' and tt.cacheadminid = '''  || UPPER(adminId) || '''';

FETCH checkGridExists into gridId;

IF (gridId < 0) THEN

   -- open the cursor to get the current gridId
   OPEN selGridIdCursor;
   FETCH selGridIdCursor into gridId;

   -- Update the gridId in the timesten grid table--
   executeString('update timesten.tt_gridid set gridIdNum = gridIdNum + 1', -1);
   gridId := gridId + 1;

      executeString('insert into timesten.tt_gridinfo (gridName, gridIdNum, cacheAdminId, comment_t) values (''' || UPPER(gridName) || ''',' || gridId || ',''' || UPPER(adminId) || ''',''' || 'Grid manually created' || ''')' , -1);

ELSE
   DBMS_OUTPUT.NEW_LINE;
   DBMS_OUTPUT.PUT_LINE('***** Grid already exists with the given adminid and gridname ****');      

END IF;


   --------------- creating the CGNODEID table -------


   DBMS_OUTPUT.NEW_LINE;
   DBMS_OUTPUT.PUT_LINE('1. Creating the '|| UPPER(adminId) || '.' || ttprefix || substr(gridName, 1, 7)|| '_' || gridId || 'CGNODEID table');

   executeString( 'CREATE TABLE ' || adminId || '.' || ttprefix || substr(gridName, 1, 7)|| '_' || gridId || 'CGNODEID (ID NUMBER (38) NOT NULL, CVGRIDID NUMBER (38) NOT NULL, VERSIONNUM NUMBER (38) NOT NULL, PLATFORM VARCHAR2 (100) NOT NULL, MAJOR1 NUMBER (38) NOT NULL, MAJOR2 NUMBER (38) NOT NULL, MAJOR3 NUMBER (38) NOT NULL, PATCH NUMBER (38) NOT NULL, PORTPATCH NUMBER (38) NOT NULL, COMMENT_T VARCHAR2 (4000))', -955);

   --------------- creating the CGNODEINFO table -------

   DBMS_OUTPUT.NEW_LINE;
   DBMS_OUTPUT.PUT_LINE('2. Creating the '|| UPPER(adminId) || '.' || ttprefix || substr(gridName, 1, 7)|| '_' || gridId || 'CGNODEINFO table');

   executeString( 'CREATE TABLE ' || adminId || '.' || ttprefix || substr(gridName, 1, 7)|| '_' || gridId || 'CGNODEINFO( ID NUMBER (38) NOT NULL, VERSIONNUM NUMBER (38) NOT NULL, ACTIVEMEMBER NUMBER (38) NOT NULL, ATTACHEDMEMBERS NUMBER (38) NOT NULL, HOSTNAME1  VARCHAR2 (200), MEMBERNAME1  VARCHAR2 (200) NOT NULL, IPADDR1 VARCHAR2 (128) NOT NULL, PORT1 NUMBER (38) NOT NULL, HOSTNAME2  VARCHAR2 (200), MEMBERNAME2 VARCHAR2 (200), IPADDR2 VARCHAR2 (128), PORT2 NUMBER (38), COMMENT_T  VARCHAR2 (4000), unique(IPADDR1, PORT1), unique (IPADDR2, PORT2))', -955);


   --------------- creating the CGGROUPDEFS table -------

   DBMS_OUTPUT.NEW_LINE;
   DBMS_OUTPUT.PUT_LINE('3. Creating the '|| UPPER(adminId) || '.' || ttprefix || substr(gridName, 1, 7)|| '_' || gridId || 'CGGROUPDEFS table');

   executeString( 'CREATE TABLE ' || adminId || '.' || ttprefix || substr(gridName, 1, 7)|| '_' || gridId || 'CGGROUPDEFS (CVGRIDID INT NOT NULL, ORATBLOBJID CHAR(32) NOT NULL, NAME CHAR(31) NOT NULL, OWNER CHAR(31) NOT NULL, REFCOUNT NUMBER(38) NOT NULL, TEXT CLOB NOT NULL, FLAGS NUMBER(38) NOT NULL, COMMENT_T  VARCHAR2(4000))', -955);


  IF (error = 0) THEN
      	 DBMS_OUTPUT.NEW_LINE;
      	 DBMS_OUTPUT.PUT_LINE('********* Creation of cache grid done successfully *********');
      	 DBMS_OUTPUT.NEW_LINE;
  ELSE
      	 DBMS_OUTPUT.NEW_LINE;
      	 DBMS_OUTPUT.PUT_LINE('** Creation of cache grid could not be successfully done  **');
      	 DBMS_OUTPUT.NEW_LINE;
  END IF; 
   
      
END;
.
/

undefine 1;
undefine 2;

