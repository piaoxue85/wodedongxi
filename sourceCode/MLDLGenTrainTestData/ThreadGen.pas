unit ThreadGen;

interface

uses
  System.Variants ,
  point,
  System.SysUtils ,
  Unit_StrFuncs ,
  ado ,
  System.Classes;

type
  TThreadGen = class(TThread)
  private
    { Private declarations }
    db      : TXlsADO ;
    dbp     : TXlsADO ;
    dbcodes : TXlsADO ;
    slPoint : TStringList ;
    slRes   : TStringList ;
    iRes : integer ;
    sResMsg : string ;

    sql : string ;
    slParams : TStringList ;
    stmp : string;

    slLoadFile : TStringList ;
    slSaveFile : TStringList ;
    idays : integer ;

    spointfilename : string ;
    procedure genCSV(pfileName:string);
    procedure genPoint(var pResList:TStringLIst ; pcode : string ; pshi_jian_begin : string ) ;
    procedure addlist(plist:tstringlist ;ppoint:TPoint) ;
    procedure updatelist(plist:tstringlist ;ppoint:TPoint;pindex:integer ) ;
    procedure appendListToTxt(pList:TStringList ; pfileName:string) ;
  protected
    procedure Execute; override;
  end;

implementation

uses
  main ;

{ 
  Important: Methods and properties of objects in visual components can only be
  used in a method called using Synchronize, for example,

      Synchronize(UpdateCaption);  

  and UpdateCaption could look like,

    procedure TThreadGen.UpdateCaption;
    begin
      Form1.Caption := 'Updated in a thread';
    end; 
    
    or 
    
    Synchronize( 
      procedure 
      begin
        Form1.Caption := 'Updated in thread via an anonymous method' 
      end
      )
    );
    
  where an anonymous method is passed.
  
  Similarly, the developer can call the Queue method with similar parameters as 
  above, instead passing another TThread class as the first parameter, putting
  the calling thread in a queue with the other thread.
    
}

{ TThreadGen }

procedure TThreadGen.addlist(plist: tstringlist; ppoint: TPoint);
var
  pointtoadd : tpoint ;
begin
  pointtoadd := tpoint.Create ;

  pointtoadd.code      := ppoint.code ;
  pointtoadd.shi_jian  := ppoint.shi_jian ;
  pointtoadd.max_price := ppoint.max_price ;
  pointtoadd.min_price := ppoint.min_price ;
  pointtoadd.buy       := ppoint.buy ;


  plist.AddObject(pointtoadd.code + ',' + copy(pointtoadd.shi_jian , 1 , 8 ) + ',' + inttostr(pointtoadd.buy) ,
                  pointtoadd) ;
end;

procedure TThreadGen.appendListToTxt(pList: TStringList; pfileName: string);
var
  i : integer ;
begin
  for I := 0 to pList.Count - 1 do
  begin
    AppendTxtFile(pList.Strings[i],pfileName);
  end;

end;

procedure TThreadGen.Execute;
var
  ifileloop :integer ;
  stmp : string ;
begin
  { Place thread code here }
  slPoint := TStringList.Create;
  slRes   := TStringList.create;
  slLoadFile := TStringList.create;
  slSaveFile := TStringList.create;
  slParams := TStringList.Create ;

  slPoint.Clear ;
  slRes.Clear ;
  slLoadFile.Clear;
  slSaveFile.Clear;

//  idays := 64 ;
  idays := 128 ;

  db := TXLSAdo.Create ;
  ires := db.Connect('Provider=OraOLEDB.Oracle.1;Password=didierg160;Persist Security Info=True;User ID=c##stock;Data Source=myoracle',sresmsg);

  dbp := TXLSAdo.Create ;
  ires := dbp.Connect('Provider=OraOLEDB.Oracle.1;Password=didierg160;Persist Security Info=True;User ID=c##stock;Data Source=myoracle',sresmsg);

  dbcodes := TXLSAdo.Create ;
  ires := dbcodes.Connect('Provider=OraOLEDB.Oracle.1;Password=didierg160;Persist Security Info=True;User ID=c##stock;Data Source=myoracle',sresmsg);

  db.bWriteErrLog:= true;
  dbp.bWriteErrLog:= true;
  dbcodes.bWriteErrLog:= true;
  //*****************************************************************************************************
//  slLoadFile.Add('D:\Projects\j金融\g股票数据分析系统\sourceCode\MLDLGenTrainTestData\train.txt');
//  slSaveFile.Add('D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\deep_recommend_system-master\data\cancer\StockTrain.csv');
//  slLoadFile.Add('D:\Projects\j金融\g股票数据分析系统\sourceCode\MLDLGenTrainTestData\test.txt');
//  slSaveFile.Add('D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\deep_recommend_system-master\data\cancer\StockTest.csv');
////
//  slLoadFile.Add('D:\Projects\j金融\g股票数据分析系统\sourceCode\MLDLGenTrainTestData\inference.txt');
//  slSaveFile.Add('D:\Projects\j金融\g股票数据分析系统\sourceCode\TuShare\test\deep_recommend_system-master\data\cancer\StockInference.csv');
////
//  db.sErrLogFileName := 'd:\err.log';
//  dbp.sErrLogFileName := 'd:\err.log';
//  dbcodes.sErrLogFileName := 'd:\err.log';
//  spointfilename := 'd:\a.txt';

  //*****************************************************************************************************
  slLoadFile.Add('.\train.txt');
  slSaveFile.Add('Z:\StockTrain.csv');
  slLoadFile.Add('.\test.txt');
  slSaveFile.Add('Z:\StockTest.csv');
//
//  slLoadFile.Add('.\inference.txt');
//  slSaveFile.Add('Z:\StockInference.csv');

  db.sErrLogFileName := 'C:\stock\err.log';
  dbp.sErrLogFileName := 'C:\stock\err.log';
  dbcodes.sErrLogFileName := 'C:\stock\err.log';
  spointfilename := 'C:\stock\a.txt';
  //*****************************************************************************************************


  //***********************************************************************
  if not fmain.genPoint.Enabled then
  begin
    slPoint.Create ;
    ResetTxtFile(spointfilename) ;
//    sql := 'select distinct(code) from tb_stock_data_daily order by DBMS_RANDOM.value';
    sql := 'select distinct(code) from tb_stock_data_daily order by code asc';
//    sql := 'select distinct(code) from tb_stock_data_daily where code=''600582'' order by code asc';
    ires := dbcodes.OpenSql(sql , sresmsg);
    dbcodes.RS.MoveFirst ;
    fmain.Memo1.Lines.Add(datetimetostr(now) + ' 开始生成买卖点。')  ;
    while not dbcodes.RS.EOF do
    begin
      stmp := dbcodes.RS.Fields['code'].Value;
      self.genPoint( slpoint , stmp , '19900101000000');
      self.appendListToTxt(slpoint,spointfilename);
      fmain.Memo1.Lines.Add(datetimetostr(now) + ' 已生成: ' + stmp)  ;
      slpoint.Clear ;
      dbcodes.RS.MoveNext ;
    end;
    fmain.Memo1.Lines.Add(datetimetostr(now) + ' 生成买卖点结束。')  ;
    fmain.genPoint.Enabled := true ;
    exit;
  end;

  //***********************************************************************

  for ifileloop := 0 to self.slLoadFile.Count -1  do
  begin
    deletefile(PChar(slSaveFile.Strings[ifileloop])) ;
    slPoint.Clear ;
    slPoint.LoadFromFile(slLoadFile.Strings[ifileloop]);
    //regenPoint ;
    fmain.Memo1.Lines.Add(slLoadFile.Strings[ifileloop] + ' loaded!') ;
    self.genCSV(slSaveFile.Strings[ifileloop]) ;
    //self.slRes.SaveToFile(slSaveFile.Strings[ifileloop]);

    fmain.Memo1.Lines.Add(slSaveFile.Strings[ifileloop] + ' saved!') ;
  end;

  slPoint.Destroy ;
  slRes.Destroy ;
  slLoadFile.Destroy ;
  slSaveFile.Destroy ;
  slParams.Destroy ;
  db.Destroy ;
  fmain.genCSV.Enabled := true;
end;

procedure TThreadGen.genCSV(pfileName:string);
var
  iloopsql : integer ;
  iloop : integer ;
begin
  slRes.Clear ;
  for iloop := 0 to slPoint.Count -1 do
  begin
    if length(trim(slPoint.Strings[iloop])) <1 then
      continue ;

    slParams.Clear ;
    SplitStr(slParams , trim(slPoint.Strings[iloop]) ,',');

//    if (strtoint(slParams[2])> 1) then
//      continue ;

    {
    sql := 'select decode(to_char(price           ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(price           ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(price_last_day  ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(price_last_day  ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(price_today_open,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(price_today_open,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(zhang_die       ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(zhang_die       ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(zhang_die_rate  ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(zhang_die_rate  ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(max_price       ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(max_price       ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(min_price       ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(min_price       ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(vol             ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(vol             ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(amount          ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(amount          ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(MA6             ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(MA6             ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(MA12            ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(MA12            ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(MA20            ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(MA20            ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(MA30            ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(MA30            ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(MA45            ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(MA45            ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(MA60            ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(MA60            ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(MA125           ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(MA125           ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(MA250           ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(MA250           ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(KDJ_K           ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(KDJ_K           ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(KDJ_D           ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(KDJ_D           ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(KDJ_J           ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(KDJ_J           ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(xstd_SLONG      ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(xstd_SLONG      ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(xstd_SSHORT     ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(xstd_SSHORT     ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(xstd_LLONG      ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(xstd_LLONG      ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(xstd_LSHORT     ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(xstd_LSHORT     ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(BOLL_uBOLL      ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(BOLL_uBOLL      ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(BOLL_dBOLL      ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(BOLL_dBOLL      ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(BOLL_BOLL       ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(BOLL_BOLL       ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(MACD_DIF        ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(MACD_DIF        ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(MACD_MACD       ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(MACD_MACD       ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(MACD_DIF_MACD   ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(MACD_DIF_MACD   ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(DPO_DPO         ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(DPO_DPO         ,''fm999999999999990.099999999999999999999''))||'',''||'+
           '       decode(to_char(DPO_6MA         ,''fm999999999999990.099999999999999999999''),null,''0.0'',to_char(DPO_6MA         ,''fm999999999999990.099999999999999999999''))||'','' res '+
           'from tb_stock_data_daily where  '+
           '  code = '''+ slParams.Strings[0] + '''' +
           '    and                         '+
           '  shi_jian <= to_date(''' + slParams[1] + '150000'',''yyyymmddhh24miss'') ' +
           'order by shi_jian desc';
    }
    sql := 'select * from ( '+
           '  select to_char(decode(price           ,null,''0.0'',price           ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(price_last_day  ,null,''0.0'',price_last_day  ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(price_today_open,null,''0.0'',price_today_open),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(zhang_die       ,null,''0.0'',zhang_die       ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(zhang_die_rate  ,null,''0.0'',zhang_die_rate  ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(max_price       ,null,''0.0'',max_price       ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(min_price       ,null,''0.0'',min_price       ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(vol             ,null,''0.0'',vol             ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(amount          ,null,''0.0'',amount          ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(MA6             ,null,''0.0'',MA6             ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(MA12            ,null,''0.0'',MA12            ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(MA20            ,null,''0.0'',MA20            ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(MA30            ,null,''0.0'',MA30            ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(MA45            ,null,''0.0'',MA45            ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(MA60            ,null,''0.0'',MA60            ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(MA125           ,null,''0.0'',MA125           ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(MA250           ,null,''0.0'',MA250           ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(KDJ_K           ,null,''0.0'',KDJ_K           ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(KDJ_D           ,null,''0.0'',KDJ_D           ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(KDJ_J           ,null,''0.0'',KDJ_J           ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(xstd_SLONG      ,null,''0.0'',xstd_SLONG      ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(xstd_SSHORT     ,null,''0.0'',xstd_SSHORT     ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(xstd_LLONG      ,null,''0.0'',xstd_LLONG      ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(xstd_LSHORT     ,null,''0.0'',xstd_LSHORT     ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(BOLL_uBOLL      ,null,''0.0'',BOLL_uBOLL      ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(BOLL_dBOLL      ,null,''0.0'',BOLL_dBOLL      ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(BOLL_BOLL       ,null,''0.0'',BOLL_BOLL       ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(MACD_DIF        ,null,''0.0'',MACD_DIF        ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(MACD_MACD       ,null,''0.0'',MACD_MACD       ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(MACD_DIF_MACD   ,null,''0.0'',MACD_DIF_MACD   ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(DPO_DPO         ,null,''0.0'',DPO_DPO         ),''fm999999999999990.099999999999999999999'')||'',''||'+
           '         to_char(decode(DPO_6MA         ,null,''0.0'',DPO_6MA         ),''fm999999999999990.099999999999999999999'')||'','' res '+
           '  from tb_stock_data_daily where  '+
           '    code = '''+ slParams.Strings[0] + '''' +
           '      and                         '+
           '    shi_jian <= to_date(''' + slParams[1] + '150000'',''yyyymmddhh24miss'') ' +
           '  order by shi_jian desc )' +
           'where rownum<= '+ inttostr(idays + 1);

//    sql := 'select * from ( '+
//           '  select to_char(decode(price           ,null,''0.0'',price           ),''fm999999999999990.099999999999999999999'')||'',''||'+
//           '         to_char(decode(price_last_day  ,null,''0.0'',price_last_day  ),''fm999999999999990.099999999999999999999'')||'',''||'+
//           '         to_char(decode(price_today_open,null,''0.0'',price_today_open),''fm999999999999990.099999999999999999999'')||'',''||'+
//           '         to_char(decode(max_price       ,null,''0.0'',max_price       ),''fm999999999999990.099999999999999999999'')||'',''||'+
//           '         to_char(decode(min_price       ,null,''0.0'',min_price       ),''fm999999999999990.099999999999999999999'')||'',''||'+
//           '         to_char(decode(vol             ,null,''0.0'',vol             ),''fm999999999999990.099999999999999999999'')||'',''||'+
//           '         to_char(decode(amount          ,null,''0.0'',amount          ),''fm999999999999990.099999999999999999999'')||'','' res '+
//           '  from tb_stock_data_daily where  '+
//           '    code = '''+ slParams.Strings[0] + '''' +
//           '      and                         '+
//           '    shi_jian <= to_date(''' + slParams[1] + '150000'',''yyyymmddhh24miss'') ' +
//           '  order by shi_jian desc )' +
//           'where rownum<= '+ inttostr(idays + 1);
    ires := db.OpenSql(sql , sresmsg);

    if ires <> 0 then
    begin
      fmain.Memo1.Lines.Add(sresmsg);
      exit ;
    end;

    if db.RS.EOF then
    begin
      continue ;
    end;

    if db.RS.RecordCount <= idays -1 then
      continue ;

    db.RS.MoveFirst ;

    stmp := '';

    for iloopsql := 0 to idays - 1 do
    begin
      stmp := stmp+ db.RS.fields['res'].value ;
      db.RS.MoveNext ;
      if db.RS.EOF then
        break ;
    end;

    stmp := stmp  + slParams[2]+'.0';

    fmain.Memo1.Lines.Add(datetimetostr(now)+'    '+slPoint.Strings[iloop]) ;
    //slRes.Add(stmp);
    AppendTxtFile(stmp,pfileName);
    db.RS.Close ;
  end;
end;

procedure TThreadGen.genPoint(var pResList:TStringLIst ; pcode : string ; pshi_jian_begin : string ) ;
var
  i : integer ;
  shi_jian : integer;
  max_price : double ;
  min_price : double ;
  pointlist : TStringList ;
  point : TPoint ;
  pointnextday : tpoint ;
  pointlastbuy : tpoint ;
  pointlastday : tpoint ;
  pointbuy     : tpoint ;

  point1 : tpoint ;
  point2 : tpoint ;

  max_max_price : double ;
  min_min_price : double ;

  shi_jian_begin : string ;

  which : double ;

begin
  pointlist := Tstringlist.Create ;

  sql := 'select max(shi_jian) - to_date(''' + pshi_jian_begin +''',''yyyymmddhh24miss'') which , ' +
         '       to_char(max(shi_jian),''yyyymmddhh24miss'') shi_jian '+
         'from tb_stock_data_daily where '+
         '  code = '''+ pcode + ''' '+
         '    and                   '+
         '  max_price= 0            ';

  ires := db.OpenSql(sql , sresmsg);

  if db.RS.EOF then
    shi_jian_begin := pshi_jian_begin
  else
  begin
    if varisnull( db.RS.Fields['which'].Value) then
      shi_jian_begin := pshi_jian_begin
    else
    begin
      which := db.RS.Fields['which'].Value ;

      if which >=0 then
        shi_jian_begin := db.RS.Fields['shi_jian'].Value
      else
        shi_jian_begin := pshi_jian_begin ;
    end;
  end;

  sql := 'select to_char(shi_jian,''yyyymmddhh24miss'') shijian , '+
         '       max_price                   , '+
         '       min_price                     '+
         'from tb_stock_data_daily where       '+
         '  code = '''+ pcode + '''            '+
         '    and                              '+
         '  shi_jian >= to_date(''' + shi_jian_begin +''',''yyyymmddhh24miss'') '+
         'order by shi_jian asc                ' ;

  ires := db.OpenSql(sql , sresmsg);
  db.RS.MoveFirst ;

  if db.RS.RecordCount <= idays then
    exit;

  for I := 0 to idays-1 do
  begin
    db.RS.MoveNext;
  end;

  point        := Tpoint.Create;
  pointlastbuy := Tpoint.Create;
  pointlastday := tpoint.Create;
  pointbuy     := tpoint.Create;
  point1       := tpoint.Create;
  point2       := tpoint.Create;
  pointnextday := tpoint.Create ;

  {
  point.code      := pcode ;
  point.shi_jian  := db.RS.fields['shijian'].value ;
  point.max_price := db.RS.fields['max_price'].value ;
  point.min_price := db.RS.fields['min_price'].value ;

  self.addlist(pointlist,point);

  pointlastday.code := point.code ;
  pointlastday.shi_jian := point.shi_jian ;
  pointlastday.max_price := point.max_price ;
  pointlastday.min_price := point.min_price ;

  db.RS.MoveNext ;
  }
  while not db.RS.EOF do
  begin
    try
      point.code      := pcode ;
      point.shi_jian  := db.RS.fields['shijian'].value ;
      point.max_price := db.RS.fields['max_price'].value ;
      point.min_price := db.RS.fields['min_price'].value ;

      if pointlist.Count <= 0 then
      begin
        db.RS.MoveNext ;

        while not db.RS.EOF do
        begin
          try
            pointnextday.code      := pcode ;
            pointnextday.shi_jian  := db.RS.fields['shijian'].value ;
            pointnextday.max_price := db.RS.fields['max_price'].value ;
            pointnextday.min_price := db.RS.fields['min_price'].value ;

            sql := 'select to_char(shi_jian,''yyyymmddhh24miss'') shijian ,max_price,min_price from '+
                   '( '+
                   '  select shi_jian,max_price,min_price from tb_stock_data_daily where '+
                   '    code = '''+pcode+'''                                             '+
                   '      and                                                            '+
                   '    shi_jian >= to_date('''+point.shi_jian+''',''yyyymmddhh24miss'') '+
                   '      and                                                            '+
                   '    shi_jian <= to_date('''+pointnextday.shi_jian+''',''yyyymmddhh24miss'')     '+
                   '      and                                                            '+
                   '    max_price =                                                    '+
                   '    (                                                              '+
                   '      select max(max_price) from tb_stock_data_daily where         '+
                   '        code = '''+pcode+'''                                       '+
                   '          and                                                      '+
                   '        shi_jian >= to_date('''+point.shi_jian+''',''yyyymmddhh24miss'') '+
                   '          and                                                        '+
                   '        shi_jian <= to_date('''+pointnextday.shi_jian+''',''yyyymmddhh24miss'') '+
                   '    )                                                                '+
                   '      and    '+
                   '    rownum<2 '+
                   '  union all                                                            '+
                   '  select shi_jian,max_price,min_price from tb_stock_data_daily where   '+
                   '    code = '''+pcode+'''                                               '+
                   '      and                                                              '+
                   '    shi_jian >= to_date('''+point.shi_jian+''',''yyyymmddhh24miss'')   '+
                   '      and                                                              '+
                   '    shi_jian <= to_date('''+pointnextday.shi_jian+''',''yyyymmddhh24miss'')       '+
                   '      and                                                              '+
                   '    min_price =                                                      '+
                   '    (                                                                '+
                   '      select min(min_price) from tb_stock_data_daily where           '+
                   '        code = '''+pcode+'''                                         '+
                   '          and                                                        '+
                   '        shi_jian >= to_date('''+point.shi_jian+''',''yyyymmddhh24miss'') '+
                   '          and                                                        '+
                   '        shi_jian <= to_date('''+pointnextday.shi_jian+''',''yyyymmddhh24miss'') '+
                   '    )                                                                '+
                   '      and    '+
                   '    rownum<2 '+
                   ') order by shi_jian asc ';

            ires := dbp.OpenSql(sql,sresmsg);
            if dbp.RS.EOF then
            begin
              continue ;
            end;

            dbp.RS.MoveFirst ;
            point1.code      := pcode         ;
            point1.shi_jian  := dbp.RS.Fields['shijian'].Value ;
            point1.max_price := dbp.RS.Fields['MAX_PRICE'].Value;
            point1.min_price := dbp.RS.Fields['MIN_PRICE'].Value;

            dbp.RS.MoveNext;
            point2.code      := pcode         ;
            point2.shi_jian  := dbp.RS.Fields['shijian'].Value ;
            point2.max_price := dbp.RS.Fields['MAX_PRICE'].Value;
            point2.min_price := dbp.RS.Fields['MIN_PRICE'].Value;

            if //(point.shi_jian = point1.shi_jian ) or
               (pointnextday.shi_jian = point2.shi_jian )
            then
            begin
              continue;
            end;

            //是不是卖点？
            if point2.max_price*0.7 >= pointnextday.min_price  then
            begin
              point2.buy := 0 ;
              self.addlist(pointlist,point2);
              break ;
            end;

            //是不是买点？
            if point2.min_price * 1.5 <= pointnextday.max_price then
            begin
              point2.buy := 1;
              self.addlist(pointlist,point2);
              break;
            end;
          finally
            db.RS.MoveNext ;
          end;

        end;

      end;

      if db.RS.EOF then
        continue;

      point.code      := pcode ;
      point.shi_jian  := db.RS.fields['shijian'].value ;
      point.max_price := db.RS.fields['max_price'].value ;
      point.min_price := db.RS.fields['min_price'].value ;

      //上一个买卖点
      pointlastbuy := tpoint(pointlist.Objects[pointlist.Count-1 ]) ;

      if pointlastbuy.buy = 1 then
      begin
        sql := 'select max(max_price) max_max_price from tb_stock_data_daily where          '+
               '  code = '''+point.code + '''                                               '+
               '    and  '+
               '  shi_jian >= to_date(''' + pointlastbuy.shi_jian + ''',''yyyymmddhh24miss'') '+
               '    and                                                                     '+
               '  shi_jian <= to_date(''' + point.shi_jian + ''',''yyyymmddhh24miss'')        ' ;


        ires := dbp.OpenSql(sql,sresmsg);

        max_max_price := dbp.RS.fields['max_max_price'].value ;

        if max_max_price * 0.7 >= point.min_price then
        begin
          sql := 'select to_char(shi_jian,''yyyymmddhh24miss'') shijian , '+
                 '       max_price                   , '+
                 '       min_price                     '+
                 'from tb_stock_data_daily where       '+
                 '  code = '''+ pcode + '''            '+
                 '    and                              '+
                 '  shi_jian =                                       ' +
                 '  (                                                ' +
                 '  	select shi_jian from tb_stock_data_daily where ' +
                 '  	  code = '''+ pcode + '''                      ' +
                 '  	    and                                        ' +
								 ' 			shi_jian >= to_date(''' + pointlastbuy.shi_jian + ''',''yyyymmddhh24miss'') ' +
								 ' 			  and                                                                     ' +
								 ' 			shi_jian <= to_date(''' + point.shi_jian + ''',''yyyymmddhh24miss'')        ' +
                 '        and  '+
                 '  	  max_price = ' + floattostr(max_max_price )   +
                 '        and    '+
                 '      rownum<2 '+
                 '  ) ';

          ires := dbp.OpenSql(sql,sresmsg);

          pointbuy.code      := pcode ;
          pointbuy.shi_jian  := dbp.RS.fields['shijian'].value ;
          pointbuy.max_price := dbp.RS.fields['max_price'].value ;
          pointbuy.min_price := dbp.RS.fields['min_price'].value ;
          pointbuy.buy := 0;
          self.addlist(pointlist,pointbuy);
        end;

      end;

      if pointlastbuy.buy = 0 then
      begin
        sql := 'select min(min_price) min_min_price from tb_stock_data_daily where          '+
               '  code = '''+point.code + '''                                               '+
               '    and  '+
               '  shi_jian >= to_date(''' + pointlastbuy.shi_jian + ''',''yyyymmddhh24miss'') '+
               '    and                                                                     '+
               '  shi_jian <= to_date(''' + point.shi_jian + ''',''yyyymmddhh24miss'')        ' ;

        ires := dbp.OpenSql(sql,sresmsg);

        min_min_price := dbp.RS.fields['min_min_price'].value ;

        if min_min_price * 1.5 <= point.max_price then
        begin
          sql := 'select to_char(shi_jian,''yyyymmddhh24miss'') shijian , '+
                 '       max_price                   , '+
                 '       min_price                     '+
                 'from tb_stock_data_daily where       '+
                 '  code = '''+ pcode + '''            '+
                 '    and                              '+
                 '  shi_jian =                                       ' +
                 '  (                                                ' +
                 '    select shi_jian from tb_stock_data_daily where ' +
                 '      code = '''+ pcode + '''                      ' +
                 '        and                                        ' +
                 '       shi_jian >= to_date(''' + pointlastbuy.shi_jian + ''',''yyyymmddhh24miss'') ' +
                 '         and                                                                     ' +
                 '       shi_jian <= to_date(''' + point.shi_jian + ''',''yyyymmddhh24miss'')        ' +
                 '        and  '+
                 '      min_price = ' + floattostr(min_min_price )  +
                 '        and    '+
                 '      rownum<2 '+
                 '  ) ';

          ires := dbp.OpenSql(sql,sresmsg);

          pointbuy.code      := pcode ;
          pointbuy.shi_jian  := dbp.RS.fields['shijian'].value ;
          pointbuy.max_price := dbp.RS.fields['max_price'].value ;
          pointbuy.min_price := dbp.RS.fields['min_price'].value ;
          pointbuy.buy := 1;
          self.addlist(pointlist,pointbuy);
        end;

      end;



    finally
      pointlastday.code := point.code ;
      pointlastday.shi_jian := point.shi_jian ;
      pointlastday.max_price := point.max_price ;
      pointlastday.min_price := point.min_price ;

      if not db.RS.EOF then
        db.RS.MoveNext ;
    end;


  end;
  pResList.Clear ;
  pResList.AddStrings(pointlist);
  //pointlist.SaveToFile('d:\a.txt');
end;

procedure TThreadGen.updatelist(plist: tstringlist; ppoint: TPoint;
  pindex: integer);
begin
//  plist.AddObject(ppoint.code + ',' + inttostr(ppoint.shi_jian) + ',' + inttostr(ppoint.buy) ,
//                  ppoint) ;
    plist.Delete(pindex);
    self.addlist(plist,ppoint);
end;

end.
