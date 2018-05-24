connect sys/t2h4o6m8@myoracle as sysdba ;
--加了这句话健用户，角色不用带c##
alter session set "_ORACLE_SCRIPT"=true;
drop user TIMESTEN CASCADE;
drop role TT_CACHE_ADMIN_ROLE ;

drop tablespace timesten INCLUDING CONTENTS;
create tablespace timesten datafile '/oracle/oradata/ttdata/timesten01.dbf'
	size 10M autoextend on maxsize unlimited extent management local segment space management auto
/

@D:\Projects\j金融\g股票数据分析系统\db\timesten\oraclescripts\initCacheGlobalSchema.sql "timesten"
@D:\\Projects\\j金融\\g股票数据分析系统\\db\\timesten\\oraclescripts\\initCacheGlobalSchema.sql "timesten";

create temporary tablespace ttusers_temp
	tempfile '/oracle/oradata/ttdata/ttusers_temp01.dbf' 
		size 10M autoextend on extent management local uniform size 1024K
/

create user cacheadm identified by t2h4o6m8
default tablespace ttusers
quota unlimited on ttusers
temporary tablespace ttusers_temp;

grant admin to cacheadm; 


@D:\Projects\j金融\g股票数据分析系统\db\timesten\oraclescripts\grantCacheAdminPrivileges.sql 

connect stock/didierg160@myoracle ;
grant select, insert, update, delete on stock.tb_stock_list          to cacheadm;
grant select, insert, update, delete on stock.tb_stock_data_realtime to cacheadm;
grant select, insert, update, delete on stock.tb_stock_data_Daily    to cacheadm;

/*
connect "dsn=cachedb1_1122;uid=cacheadm;oraclepwd=t2h4o6m8";

call ttcacheuidpwdset ('cacheadm','t2h4o6m8');
call ttcacheuidget;

call ttgridcreate ('samplegrid');
call ttgridinfo;
call ttgridnameset ('samplegrid');
*/

call ttGridCreate('myGrid');
call ttGridNameSet('myGrid');  


call ttcacheuidpwdset('c##stock','didierg160');
call ttcachestart;