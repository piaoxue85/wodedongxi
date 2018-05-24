connect sys/t2h4o6m8@myoracle as sysdba ;
--设置用户密码永不过期
ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;
--股票数据库 
drop tablespace stock_data INCLUDING CONTENTS
/
create tablespace stock_data 
	datafile '/oracle/oradata/stock/stock_data01.dbf' 
		size 10M autoextend on maxsize unlimited extent management local segment space management auto
/

--股票数据库临时表空间
drop tablespace stock_data_tmp INCLUDING CONTENTS
/
create temporary tablespace stock_data_tmp
	tempfile '/oracle/oradata/stock/stock_data_tmp01.dbf' 
		size 10M autoextend on extent management local uniform size 1024K
/
		
/*-------------------
创建股票用户knl
--------------------*/
drop user c##stock CASCADE
/
create user c##stock identified by didierg160 default tablespace stock_data temporary tablespace stock_data_tmp
alter user c##stock identified by didierg160; 
/


/*-------------------
设置相应的用户权限、角色
--------------------*/
--授予ivrknl dba权限
grant dba to c##stock
/


