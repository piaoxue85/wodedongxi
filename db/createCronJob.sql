/*#################################################################################################
说明:定时搬运短信发送记录
#################################################################################################*/
--删除job
/*
declare
  v_num number;
  v_ProcName varchar2(1024);  
begin
  v_ProcName := 'proc_month_telebill_hj(to_char(sysdate,''yyyymm''),10);';
  select count(1) into v_num from user_jobs where what = v_ProcName;
  if v_num>0 then
    select job into v_num from user_jobs where what = v_ProcName;
    dbms_job.remove(v_num);
  end if;
end;
/

--创建job
variable job1 number;
begin
  dbms_job.submit(:job1,'proc_month_telebill_hj(to_char(sysdate,''yyyymm''),10);',to_date('20080427003000','yyyymmddhh24miss'),null);   --每天24小时，即一小时运行proc_si_movesmshis过程一次
end;
/

--运行job
begin
  dbms_job.run(:job1);
end;
/

*/

declare
  cursor cur is
    select job from user_jobs ;  
  rt cur%rowtype ;
begin	
	for rt in cur loop		
	  dbms_job.remove(rt.job);
	end loop ;
	commit;
end;
/


--创建job
variable job number;
begin
  dbms_job.submit(:job,'proc_stock_get_week_all    ;',to_date('20160102150000','yyyymmddhh24miss'), 'to_date(to_char(trunc(sysdate + 9,''d'')-1,''yyyymmdd'')||120000,''yyyymmddhh24miss'')');   
  dbms_job.submit(:job,'proc_stock_get_month_all   ;',to_date('20160102150000','yyyymmddhh24miss'), 'to_date(to_char(add_months(trunc(sysdate,''month''),1 ),''yyyymmdd'')||150000,''yyyymmddhh24miss'')'); 
  --dbms_job.submit(:job,'proc_stock_get_Quarter_all ;',to_date('20160102150000','yyyymmddhh24miss'), 'to_date(to_char(add_months(trunc(sysdate,''q''    ),3 ),''yyyymmdd'')||150000,''yyyymmddhh24miss'')');   
  dbms_job.submit(:job,'proc_stock_get_Quarter_all ;',to_date('20160102150000','yyyymmddhh24miss'), 'to_date(to_char(trunc(sysdate + 9,''d'')-1,''yyyymmdd'')||170000,''yyyymmddhh24miss'')');   
  dbms_job.submit(:job,'proc_stock_get_HalfYear_all;',to_date('20160102150000','yyyymmddhh24miss'), 'to_date(to_char(f_truncHalfYear(add_months(sysdate,6 )),''yyyymmdd'')||150000,''yyyymmddhh24miss'')');  
  dbms_job.submit(:job,'proc_stock_get_Year_all    ;',to_date('20160102150000','yyyymmddhh24miss'), 'to_date(to_char(add_months(trunc(sysdate,''year'' ),12),''yyyymmdd'')||150000,''yyyymmddhh24miss'')');    
  commit;
end;


--创建job
variable job number;
begin
  dbms_job.submit(:job,'proc_stock_get_week_all    ;',to_date('20160102150000','yyyymmddhh24miss'), 'to_date(to_char(trunc(sysdate + 9,''d'')-1,''yyyymmdd'')||150000,''yyyymmddhh24miss'')');   
  dbms_job.submit(:job,'proc_stock_get_month_all   ;',to_date('20160102150000','yyyymmddhh24miss'), 'to_date(to_char(add_months(trunc(sysdate,''month''),1 ),''yyyymmdd'')||150000,''yyyymmddhh24miss'')'); 
  dbms_job.submit(:job,'proc_stock_get_Quarter_all ;',to_date('20160102150000','yyyymmddhh24miss'), 'to_date(to_char(add_months(trunc(sysdate,''q''    ),3 ),''yyyymmdd'')||150000,''yyyymmddhh24miss'')');   
  dbms_job.submit(:job,'proc_stock_get_HalfYear_all;',to_date('20160102150000','yyyymmddhh24miss'), 'to_date(to_char(f_truncHalfYear(add_months(sysdate,6 )),''yyyymmdd'')||150000,''yyyymmddhh24miss'')');  
  dbms_job.submit(:job,'proc_stock_get_Year_all    ;',to_date('20160102150000','yyyymmddhh24miss'), 'to_date(to_char(add_months(trunc(sysdate,''year'' ),12),''yyyymmdd'')||150000,''yyyymmddhh24miss'')');    
  commit;
end;


--创建job
variable job number;
begin
  dbms_job.submit(:job,'proc_stock_get_week_all    ;',sysdate + 0.6, 'to_date(to_char(trunc(sysdate + 9,''d'')-1,''yyyymmdd'')||120000,''yyyymmddhh24miss'')');   
  dbms_job.submit(:job,'proc_stock_get_month_all   ;',sysdate + 0.6, 'to_date(to_char(add_months(trunc(sysdate,''month''),1 ),''yyyymmdd'')||150000,''yyyymmddhh24miss'')'); 
  --dbms_job.submit(:job,'proc_stock_get_Quarter_all ;',sysdate + 0.6, 'to_date(to_char(add_months(trunc(sysdate,''q''    ),3 ),''yyyymmdd'')||150000,''yyyymmddhh24miss'')');   
  dbms_job.submit(:job,'proc_stock_get_Quarter_all ;',sysdate + 0.6, 'to_date(to_char(trunc(sysdate + 9,''d'')-1,''yyyymmdd'')||170000,''yyyymmddhh24miss'')');   
  dbms_job.submit(:job,'proc_stock_get_HalfYear_all;',sysdate + 0.6, 'to_date(to_char(f_truncHalfYear(add_months(sysdate,6 )),''yyyymmdd'')||150000,''yyyymmddhh24miss'')');  
  dbms_job.submit(:job,'proc_stock_get_Year_all    ;',sysdate + 0.6, 'to_date(to_char(add_months(trunc(sysdate,''year'' ),12),''yyyymmdd'')||150000,''yyyymmddhh24miss'')');    
  dbms_job.submit(:job,'proc_stock_new_stock       ;',sysdate + 10/(24*60), 'trunc(sysdate)+1+ 8.5/24');    
  commit;
end;
