/**
This script will be installed for Cache Connect to Oracle installations. 
It is designed to run on Oracle using sqlplus to clean all autorefresh objects 
related to a TimesTen data store when that data store is no longer available. 
The script requires that the user is connected to the Oracle database as a 
cache admin user. 

INPUT
Script requires host and TimesTen data store name as input. 
Its important to use the same name for host and data store name as its 
registered on oracle. Use full path name for the data store. If the target 
Timesten data store is on windows platform, use all lowercase value for host 
and data store name. Output from <installdir>/bin/autorefreshChangeLogInfo.sql 
script shows the host and datastore name as registered on oracle. 

Parameters can be passed to SQL*Plus script. For example, from the command line:

sqlplus <cacheadminuid>/<cacheadminpwd>@<oracleid> 
@ <installdir>/bin/autorefreshCleanUp.sql "<host_name>" "<datastore_name>"

You can also pass parameters when calling script from within a SQL*Plus session, 
for example:

SQL> @ <installdir>/bin/autorefreshCleanUp.sql "<host_name>" "<datastore_name>"

If parameters are not specified on the command line, script will prompt for 
parameters. Parameter 1 is host name. Parameter 2 is data store name.

OUTPUT
Script prints the cleanup sql that it executes on Oracle. 

Example output 1: (when trigger and log table is in use by other data stores)
*****************************OUTPUT**************************************
Performing cleanup for object_id: 91771 which belongs to table : SCOTT.FOO
Executing: delete from tt_06_agent_status where host = my-pc 
and datastore = c:\data\rep2 and object_id = 91771
Executing: update tt_06_user_count set usercount = :usecount,usecount = 1
**************************************************************************

Example output 2: (when no other data stores using trigger and log table)
*****************************OUTPUT**************************************
Performing cleanup for object_id: 83560 which belongs to table : SCOTT.FOO
Executing: delete from tt_06_agent_status where host = my-pc 
and datastore = c:\data\tt60 and object_id = 83560
Executing: drop table tt_06_83560_L
Executing: drop trigger tt_06_83560_T
Executing: delete from tt_06_user_count where object_id = object_id1
**************************************************************************

Example output 3: (When no autorefresh objects are found)
*****************************OUTPUT**************************************
No autorefresh objects are found for datastore c:\data\tt70 on host my-pc
(If the target Timesten data store is on windows platform, please try all
lowercase value for host and data store name)
**************************************************************************
*
**/


set echo off;
SET SERVEROUTPUT ON;
PROMPT ;
PROMPT Please enter the hostname;
SET TERMOUT OFF;
SET VERIFY OFF;
DEFINE hostnamePr = '&&1';
SET TERMOUT ON;
PROMPT The value chosen for the hostname is &1;
PROMPT ;

PROMPT Please enter the datastore;
SET TERMOUT OFF;
SET VERIFY OFF;
DEFINE datastorePr = '&&2';
SET TERMOUT ON;
PROMPT The value chosen for the datastore is &2;
PROMPT ;


declare 
sqlString varchar(256);
object_id number;
object_id1 number;
cgType number;
tablename varchar(65);
usecount NUMBER;
usecount1 NUMBER; /* 1 stands for cachegroup or cgType to be 1, that is it is non-AR */
host1 varchar(200) := '&1';
datastore1 varchar(257) := '&2';
err_num NUMBER;
objectsFound BOOLEAN := FALSE;

/* Cursor walks through the tt_06_user_count table to find object_ids of cached table  */
cursor getObjId IS select object_id, cgType from tt_06_agent_status where LOWER(datastore) = LOWER(datastore1) and LOWER(host) = LOWER(host1) for update;
cursor lockcount IS select usercount, tablename from tt_06_user_count where object_id = object_id1 and cachegroup = 0 for update;
cursor lockcount1 IS select usercount, tablename from tt_06_user_count where object_id = object_id1 and cachegroup = 1 for update;


/* build sql to get total number of rows in a log table */
cursor dropLogTbl IS 
select 'drop table tt_06_' || to_char(object_id) || '_L' from tt_06_user_count where object_id = object_id1;

cursor dropTrig IS 
select 'drop trigger tt_06_' || to_char(object_id) || '_T' from tt_06_user_count where object_id = object_id1;

begin

/* loops through all cached tables found in tt_06_user_count table */
  DBMS_OUTPUT.PUT_LINE('*****************************OUTPUT**************************************');
  loop
    open getObjId;
    fetch getObjId into object_id, cgType;
    exit when getObjId%NOTFOUND or getObjId%NOTFOUND IS NULL;
    objectsFound := TRUE;	
    object_id1 := object_id;
    usecount := 0;
    usecount1 := 0;
    if (cgType = 0) then
      open lockcount;
      fetch lockcount into usecount, tablename;
    else
      open lockcount1;
      fetch lockcount1 into usecount, tablename;    
    end if;
    
    DBMS_OUTPUT.PUT_LINE('Performing cleanup for object_id: ' || object_id1 || ' which belongs to table : ' || tablename);
    DBMS_OUTPUT.PUT_LINE('Executing: delete from tt_06_agent_status where LOWER(host) = ' || LOWER(host1) || ' and LOWER(datastore) = ' || LOWER(datastore1) || ' and object_id = ' || object_id1 );	
    execute immediate 'delete from tt_06_agent_status where LOWER(host) = LOWER(:host) and LOWER(datastore) = LOWER(:datastore) and object_id = :object_id1' using host1, datastore1, object_id1;     
        
    if (cgType = 0) then /* Is this an autorefresh (on or paused) cache group */
       execute immediate 'select count(*) from tt_06_agent_status where object_id = :object_id1 and cgType = 0' into usecount using object_id1;    
      /* If the user count is 0, drop the trigger and the log table */
      if (usecount = 0) then
      	 /* Drop the trigger */
	 open dropTrig;
       	 fetch dropTrig into sqlString;
         DBMS_OUTPUT.PUT_LINE('Executing: ' || sqlString);
         begin 
           execute immediate sqlString;
         exception 
           when others then 
           err_num := SQLCODE;
         end;
         close dropTrig;
         /* Drop the log table */	
	 open dropLogTbl;
         fetch dropLogTbl into sqlString;
         DBMS_OUTPUT.PUT_LINE('Executing: ' || sqlString);
         begin 
          execute immediate sqlString;
         exception 
           when others then 
           err_num := SQLCODE;
         end;
         close dropLogTbl;
	 /* Now delete the row from the user_count table */
	 DBMS_OUTPUT.PUT_LINE('Executing: delete from tt_06_user_count where object_id = object_id1');
         execute immediate 'delete from tt_06_user_count where object_id = ' || object_id1 || ' and cachegroup = 0';
      else
	 /* Now update the user_count table to reflect the count */
         DBMS_OUTPUT.PUT_LINE('Executing: update tt_06_user_count set usercount = :usecount,' || 'usecount = ' || usecount || 'cachegroup = ' || cgType);
         execute immediate 'update tt_06_user_count set usercount = :usecount where cachegroup = :cgType'  using usecount, cgType;                  
      end if;
    else
       execute immediate 'select count(*) from tt_06_agent_status where object_id = :object_id1 and cgType = 1' into usecount1 using object_id1;
      if (usecount1 = 0) then 
	DBMS_OUTPUT.PUT_LINE('Executing: delete from tt_06_user_count where ' || ' object_id = ' || object_id1 || ' cachegroup = ' || cgType);
        execute immediate 'delete from tt_06_user_count where object_id = ' || object_id1 || ' and cachegroup = 1';      
      else
        DBMS_OUTPUT.PUT_LINE('Executing: update tt_06_user_count set usercount = :usecount,' || 'usecount = ' || usecount || 'cachegroup = ' || cgType);
        execute immediate 'update tt_06_user_count set usercount = :usecount where cachegroup = :cgType'  using usecount, cgType;                        
      end if;
      
    end if;
    commit;
    if (cgType = 0) then 
     close lockcount;
    else
     close lockcount1;    
    end if;
    close getObjId;
  end loop;
  

  DBMS_OUTPUT.PUT_LINE('Executing: delete from tt_06_databases where LOWER(host) = ' || LOWER(host1) || ' and LOWER(datastore) = ' || LOWER(datastore1) );
  execute immediate 'delete from tt_06_databases where LOWER(host) = LOWER(:host) and LOWER(datastore) = LOWER(:datastore)' using host1, datastore1;


  if (objectsFound = FALSE) then
    DBMS_OUTPUT.PUT_LINE('No cache objects are found for datastore ' || datastore1 || ' on host ' || host1);
    DBMS_OUTPUT.PUT_LINE('(If the target Timesten data store is on windows platform, please try all lowercase value for host and data store name)');
  end if;
  DBMS_OUTPUT.PUT_LINE('**************************************************************************');
  
end;
/

undefine 1;
undefine 2;
