connect sys/t2h4o6m8@myoracle as sysdba ;
--�����û�������������
ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;
--��Ʊ���ݿ� 
drop tablespace stock_data INCLUDING CONTENTS
/
create tablespace stock_data 
	datafile '/oracle/oradata/stock/stock_data01.dbf' 
		size 10M autoextend on maxsize unlimited extent management local segment space management auto
/

--��Ʊ���ݿ���ʱ��ռ�
drop tablespace stock_data_tmp INCLUDING CONTENTS
/
create temporary tablespace stock_data_tmp
	tempfile '/oracle/oradata/stock/stock_data_tmp01.dbf' 
		size 10M autoextend on extent management local uniform size 1024K
/
		
/*-------------------
������Ʊ�û�knl
--------------------*/
drop user c##stock CASCADE
/
create user c##stock identified by didierg160 default tablespace stock_data temporary tablespace stock_data_tmp
alter user c##stock identified by didierg160; 
/


/*-------------------
������Ӧ���û�Ȩ�ޡ���ɫ
--------------------*/
--����ivrknl dbaȨ��
grant dba to c##stock
/


