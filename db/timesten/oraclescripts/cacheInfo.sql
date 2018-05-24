/* This script is to be run on oracle using sqlplus 
 * Script assumes that user is connected to the oracle database
 * as cache admin user. 
 * Script prints information for each log table corresponding to
 * a cached table on each timesten datastore & host 
 * 
 * Example:
 * sqlplus <cacheadminuid>/<cacheadminpwd>@<oracleid> 
 * @<installdir>/oraclescripts/cacheInfo.sql;
 *  
 * Sample Output: 
 ****************************
 * Host name: my-pc
 * Timesten daatastore name: c:\data\tt70
 * Cache table name: scott.FOO
 * Change log table name: tt_06_67238_L
 * Number of rows in change log table: 100000
 * Maximum logseq on the change log table: 38
 * Timesten has autorefreshed updates upto logseq: 38
 * Number of updates waiting to be autorefreshed: 0
 * Number of updates that has not been marked with a valid logseq: 0
 ****************************
 * 
*/

set serveroutput on;
declare
sqlString varchar(256);
object_id number;
object_id1 number;
schema varchar(31);
tablename varchar(31);
datastore varchar(257);
host varchar(200);
oraBookmark number;
ttBookmark number;
numrows number;
numUnmarkedRows number;
numToBeAutorefRows number;
err_num NUMBER;
usecount NUMBER;
trigger varchar(31);
ddlTriggerFound int := 0;
autoRefObjsFound int := 0;

/* Cursor walks through the tt_06_user_count table to find object_ids of cached table  */
cursor getObjId IS select a.object_id, schema, tablename, host, datastore, logseq, bookmark from tt_06_agent_status a, tt_06_user_count b where a.object_id = b.object_id and a.cgType = 0 and b.cachegroup = 0 order by host, datastore, schema, tablename; 

/* build sql to get total number of rows in a log table */
cursor getNumRows IS 
select 'select count(*) from tt_06_' || to_char(object_id) || '_L' from tt_06_user_count where object_id = object_id1;

/* build sql to get number of rows that are waiting to be autorefreshed in a log table */
cursor getNumToBeAutorefRows IS 
select 'select count(*) from tt_06_' || to_char(object_id) || '_L' || ' where logseq > :ttBookmark' from tt_06_user_count where object_id = object_id1;

/* build sql to get number of rows in a log table that are not marked yet */
cursor getUnmarkedRows IS
select 'select count(*) from tt_06_' || to_char(object_id) || '_L' || ' where logseq = 99999999999999999999999999999999999999' from tt_06_user_count where object_id = object_id1;

cursor getDDLTriggers IS
select b.username, a.trigger_name, nvl(c.usecount,0) from user_triggers a,all_users b, (select distinct(schema), sum(usercount) usecount from tt_06_user_count group by schema) c where regexp_substr(trigger_name, '[[:digit:]]+',7) = b.user_id and b.username = c.schema(+);

begin
  open getObjId;

/* loops through all cached tables found in tt_06_user_count table */
  loop
    fetch getObjId into object_id, schema, tablename, host, datastore, oraBookmark, ttBookmark;
    exit when getObjId%NOTFOUND;
    if (autoRefObjsFound = 0) then
    autoRefObjsFound := 1;
    DBMS_OUTPUT.PUT_LINE('*************Autorefresh Objects Information  ***************');	
    end if;
    object_id1 := object_id;
    open getNumRows;
    fetch getNumRows into sqlString;
    close getNumRows;
    begin 
      /* get total number of rows in the change log table tt_06_<object_id>_L */
      execute immediate sqlString into numRows;
      open getNumToBeAutorefRows; 
      fetch getNumToBeAutorefRows into sqlString; 
      /* get number of rows that are waiting to be autorefreshed in the change log table */
      execute immediate sqlString into numToBeAutorefRows using ttBookmark; 
      close getNumToBeAutorefRows;
      open getUnmarkedRows;
      fetch getUnmarkedRows into sqlString;
      /* get number of unmarked rows in the change log table */
      execute immediate sqlString into numUnmarkedRows; 
      close getUnmarkedRows;
      DBMS_OUTPUT.PUT_LINE('Host name: ' || host);
      DBMS_OUTPUT.PUT_LINE('Timesten datastore name: ' || datastore);
      DBMS_OUTPUT.PUT_LINE('Cache table name: ' || schema || '.' || tablename );
      DBMS_OUTPUT.PUT_LINE('Change log table name: tt_06_' ||  object_id1 || '_L');
      DBMS_OUTPUT.PUT_LINE('Number of rows in change log table: ' || numRows);
      DBMS_OUTPUT.PUT_LINE('Maximum logseq on the change log table: ' || oraBookmark);
      DBMS_OUTPUT.PUT_LINE('Timesten has autorefreshed updates upto logseq: ' || ttBookmark);
      DBMS_OUTPUT.PUT_LINE('Number of updates waiting to be autorefreshed: ' || numToBeAutorefRows);
      DBMS_OUTPUT.PUT_LINE('Number of updates that has not been marked with a valid logseq: ' || numUnmarkedRows);
      DBMS_OUTPUT.PUT_LINE('****************************');
    exception
      when others then
      err_num := SQLCODE; 
      /* go to the next log table if one log table is not found */
      if(err_num != -942) THEN
        RAISE;
      end if; 
    end;
  end loop;
  close getObjId;
  if(autoRefObjsFound = 0) then
  DBMS_OUTPUT.PUT_LINE('*************No autorefresh objects are found*************');
  end if;
  /* Query to find ddl triggers */
  open getDDLTriggers;
  loop 
  fetch getDDLTriggers into schema, trigger, usecount;
  exit when getDDLTriggers%NOTFOUND;
  if(ddlTriggerFound = 0) then 
    ddlTriggerFound := 1;
     DBMS_OUTPUT.PUT_LINE('*************DDL Tracking Object Information  ***************');
     DBMS_OUTPUT.PUT_LINE('Common DDL Log Table Name: TT_06_DDL_L');
  end if;
  DBMS_OUTPUT.PUT_LINE('DDL Trigger Name: ' || trigger);
  DBMS_OUTPUT.PUT_LINE('Schema for which DDL Trigger is tracking: ' || schema);
  DBMS_OUTPUT.PUT_LINE('Number of cache groups using the DDL Trigger: ' || usecount);
  DBMS_OUTPUT.PUT_LINE('****************************');	
  end loop;
  close getDDLTriggers;
  if(ddlTriggerFound = 0) then
  DBMS_OUTPUT.PUT_LINE('*************No DDL Tracking objects are found*************');
  end if;
end;
/


