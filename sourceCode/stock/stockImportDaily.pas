unit stockImportDaily;

interface
uses
  System.DateUtils ,
  Vcl.StdCtrls ,
  stockImportNameAndCode ,
  Windows ,
  Unit_FileFuncs,
  Unit_StrFuncs ,
  comobj,
  ado ,
  Controls ,
  System.SysUtils, System.Variants, System.Classes ;

type
  TstockImportDaily = class(TObject)
  private
    db : TXLsAdo ;
    //xls : Variant ;
    res : integer ;
    resmsg : string ;

    code : string ;

    sql : string ;
    function import( pfileName : string ; var pResMsg : string ) : integer ; overload;
    //function getCodeByName(pName : string ; var presMsg :string  ) : string ;
    function find(List:TStringList; s:string ;var row:integer):boolean ;
  public
    connstr :string ;

    function  import(pFileList : TStringList ; var pResMsg : string ) : integer ; overload ;
    function  import(pFileList : TStringList ; memo : tmemo ; var pResMsg : string ) : integer ; overload ;
    constructor Create;
    Destructor  Destroy ;
  end;

implementation

{ TstockDaily }
constructor TstockImportDaily.Create;
begin
  inherited Create;
  db := TXLSAdo.Create ;
  db.bWriteErrLog := true ;
  //db.bWriteActLog := true ;
  //xls := createoleobject('Excel.Application');
  //connstr :='Provider=OraOLEDB.Oracle.1;Password=didierg160;Persist Security Info=True;User ID=c##stock;Data Source=myoracle';
end;

destructor TstockImportDaily.Destroy;
begin
  db.Destroy ;
  //xls.Quit ;
  //xls := unassigned ;
  inherited Destroy ;
end;

function TstockImportDaily.find(List: TStringList; s: string;
  var row: integer): boolean;
var
  loop:integer ;
begin
  result := false ;
  for loop := 0 to List.Count - 1 do
  begin
    if pos(s, list.Strings[loop])>0 then
    begin
      row := loop ;
      result := true ;
      break ;
    end;
  end;

end;

function TstockImportDaily.import(pFileList: TStringList; memo: tmemo;
  var pResMsg: string): integer;
var
  iLoopTime : integer ;
  res : integer ;
  resMsg : string ;
  ire : integer ;
begin
  { Place thread code here }

  //sql := 'truncate table tb_stock_data_daily';
  //res := db.Connect(connstr , resmsg);
  //res := db.ExecuteSql(sql , false , ire , resmsg);
  res := db.Connect(connstr , resmsg);
  for iLoopTime := 0 to pFileList.Count - 1 do
  begin
    memo.Lines.Add(datetimetostr(now) + ':' + pFileList.Strings[iLoopTime] + '开始');
    res:= import(pFileList.Strings[iLoopTime] , resMsg)  ;
    memo.Lines.Add(datetimetostr(now) + ':' + pFileList.Strings[iLoopTime] + '已完成,操作结果:'+resMsg);
  end;
  pResMsg := resmsg;
  db.Disconnect( resmsg);
  result := res ;

end;

function TstockImportDaily.import(pfileName: string; var pResMsg:string): integer;
var
  name  : string ;
  slTmp : TStringList ;
  //count : integer ;
  ire   : integer ;
  row   : integer ;
  row_  : integer ;

  shi_jian         : string ;
  price_today_open : string ;
  max_price        : string ;
  min_price        : string ;
  price            : string ;
  price_last_day   : string ;
  vol              : string ;
  amount           : string ;
  MA6         : string ;
  MA12        : string ;
  MA20        : string ;
  MA30        : string ;
  MA45        : string ;
  MA60        : string ;
  MA125       : string ;
  MA250       : string ;
  KDJ_K       : string ;
  KDJ_D       : string ;
  KDJ_J       : string ;
  xstd_SLONG  : string ;
  xstd_SSHORT : string ;
  xstd_LLONG  : string ;
  xstd_LSHORT : string ;
  BOLL_uBOLL  : string ;
  BOLL_dBOLL  : string ;
  BOLL_BOLL   : string ;
  MACD_DIF    : string ;
  MACD_MACD   : string ;
  MACD_DIF_MACD : string;
  DPO_DPO     : string ;
  DPO_6MA	    : string ;

  fileName : string ;
  importList : TstockImportNameAndCode ;

  last_Shi_jian : string ;

  first_Shi_jian : string ;
  price_first_day: string ;

  append : boolean ;
  eof    : boolean ;

  data : TStringList ;
  err : exception ;

  sTmp : string ;
  timeSplit : Tstringlist ;
begin
  try
    try

      timeSplit := TStringList.Create ;
      timeSplit.Clear ;

      slTmp := TStringList.Create ;
      slTmp.Clear ;

      data := TStringList.Create ;
      data.Clear ;

      fileName := getFileName( pfileName ) ;



      //星期1~5 的 8:30 ~ 15:00 之间不导入，直接删文件。
      if (DayOfTheWeek(now)>=1) and (DayOfTheWeek(now)<=5) then
      begin
        sTmp := datetimetostr(now);

        SplitStr( timeSplit , sTmp , ' ');
        sTmp := timeSplit[timeSplit.count-1];
        timeSplit.Clear ;

        sTmp := StringReplace(sTmp,':','', [rfReplaceAll]);
//        sTmp := StringReplace(copy(sTmp,10,length(sTmp)-9),':','', [rfReplaceAll]);
        if (strtoint(sTmp)>=83000) and (strtoint(sTmp)<=150000) then
        begin
          deletefile(PChar(pfileName)) ;
          resmsg := '8:30 ~ 15:00 之间不导入，直接删文件。' ;
          res    := 0;
          exit ;
        end;
      end;

      if fileName = '上证指数--技术分析--日  线--不除权.txt' then
      begin
        code := 'sh000001' ;
        name := '上证指数';
      end
      else if fileName='深证成指--技术分析--日  线--不除权.txt' then
      begin
        code := 'sz399001';
        name := '深证成指';
      end
      else if fileName = '报价--沪深Ａ股.txt'  then
      begin
        importList := TstockImportNameAndCode.Create ;
        importList.connstr := connstr ;
        res := importList.import(pfileName,presmsg) ;
        importList.Destroy ;
        result := res ;
        exit ;
      end
      else if pos('日  线',fileName) <= 0 then
      begin
        res := 1 ;
        resmsg := '不是日线数据' ;
        pResMsg := '不是日线数据' ;
        result := 1 ;
        deletefile(PChar(pfileName)) ;
        exit ;
      end
      else
      begin
        SplitStr(slTmp , fileName , '--');
        name := trim(sltmp.Strings[0]);
        slTmp.Clear ;

        sql := 'select code from tb_stock_list where name = ''' + name + '''';
        //res := db.Connect(connstr , resmsg);
        res := db.OpenSql(sql , resmsg);

        if db.RS.EOF then
        begin
          db.RS.Close ;
          //db.Disconnect(resMsg) ;
          res := 1 ;
          resmsg := '通过股票名字没有找到对应的股票代码' ;
          pResMsg := '通过股票名字没有找到对应的股票代码' ;
          result := 1 ;
          deletefile(PChar(pfileName)) ;
          exit ;
        end;
        code := db.RS.Fields['code'].Value ;
        db.RS.Close ;
      end;

      sql := 'select price,to_char(shi_jian,''yyyy/mm/dd'') shi_jian from tb_stock_data_daily where '+
             '  code = ''' + code + '''' +
             '    and ' +
             '  shi_jian = (select max(shi_jian) from tb_stock_data_daily where code = ''' + code + ''')' ;
      res := db.OpenSql(sql , resmsg);

      //xls.workbooks.open(pfileName);
      data.Clear ;
      data.LoadFromFile(pfileName);
      append := true ;

      eof := db.RS.EOF ;
      if eof then
      begin
        append := false  ;
      end
      else
      begin
        append := true ;
        price_last_day:= db.RS.Fields['price'].Value ;
        last_shi_jian := db.RS.Fields['shi_jian'].Value ;

        if Find(data,last_shi_jian,Row) then
        begin
          SplitStr(slTmp , data.Strings[row] , '	');
          price := trim(slTmp.Strings[5 - 1]) ;
          slTmp.Clear ;
          if strtofloat(price) <> strtofloat(price_last_day) then
            append := false ;
        end
        else
          append := false ;
      end;

      db.RS.Close ;

      if append then
      begin
      
        sql := 'select price,to_char(shi_jian,''yyyy/mm/dd'') shi_jian from tb_stock_data_daily where '+
               '  code = ''' + code + '''' +
               '    and ' +
               '  shi_jian = (select min(shi_jian) from tb_stock_data_daily where code = ''' + code + ''')' ;
        res := db.OpenSql(sql , resmsg);

        //xls.workbooks.open(pfileName);
        data.Clear ;
        data.LoadFromFile(pfileName);

        eof := db.RS.EOF ;
        if eof then
        begin
          append := false  ;
        end
        else
        begin
          append := true ;
          price_first_day:= db.RS.Fields['price'].Value ;
          first_shi_jian := db.RS.Fields['shi_jian'].Value ;

          if Find(data,first_shi_jian,Row_) then
          begin
            SplitStr(slTmp , data.Strings[row_] , '	');
            price := trim(slTmp.Strings[5 - 1]) ;
            slTmp.Clear ;
            if strtofloat(price) <> strtofloat(price_first_day) then
              append := false ;
          end
          else
            append := false ;

          if db.RS.RecordCount > 1 then
            append := false ;

        end;

        db.RS.Close ;
      end;


      if append then
      begin
        inc(row) ;
      end
      else
      begin
        if not eof then
        begin
          sql :='delete tb_stock_data_daily where code=''' + code +'''';
          res := db.ExecuteSql(sql , false , ire , resmsg ) ;
        end;
        row := 3 ;
        price_last_day := '0' ;
      end;

      //count:= 0 ;

      while row <  data.Count   do
      begin
        //if count < 1 then
        //  db.beginTrans ;
        try
          slTmp.Clear ;
          SplitStr(slTmp , data.Strings[row] , '	');
          shi_jian         := trim(slTmp.Strings[1 - 1]);

          if trim(shi_jian)='' then
            break ;

          price_today_open := trim(slTmp.Strings[2  - 1]) ;
          max_price        := trim(slTmp.Strings[3  - 1]) ;
          min_price        := trim(slTmp.Strings[4  - 1]) ;
          price            := trim(slTmp.Strings[5  - 1]) ;
          vol              := trim(slTmp.Strings[6  - 1]) ;
          amount           := trim(slTmp.Strings[7  - 1]) ;
          MA6              := strreplace(trim(slTmp.Strings[8  - 1]),'----','null') ;
          MA12             := strreplace(trim(slTmp.Strings[9  - 1]),'----','null') ;
          MA20             := strreplace(trim(slTmp.Strings[10 - 1]),'----','null') ;
          MA30             := strreplace(trim(slTmp.Strings[11 - 1]),'----','null') ;
          MA45             := strreplace(trim(slTmp.Strings[12 - 1]),'----','null') ;
          MA60             := strreplace(trim(slTmp.Strings[13 - 1]),'----','null') ;
          MA125            := strreplace(trim(slTmp.Strings[14 - 1]),'----','null') ;
          MA250            := strreplace(trim(slTmp.Strings[15 - 1]),'----','null') ;
          KDJ_K            := strreplace(trim(slTmp.Strings[17 - 1]),'----','null') ;
          KDJ_D            := strreplace(trim(slTmp.Strings[18 - 1]),'----','null') ;
          KDJ_J            := strreplace(trim(slTmp.Strings[19 - 1]),'----','null') ;
          xstd_SLONG       := strreplace(trim(slTmp.Strings[21 - 1]),'----','null') ;
          xstd_SSHORT      := strreplace(trim(slTmp.Strings[22 - 1]),'----','null') ;
          xstd_LLONG       := strreplace(trim(slTmp.Strings[23 - 1]),'----','null') ;
          xstd_LSHORT      := strreplace(trim(slTmp.Strings[24 - 1]),'----','null') ;
          BOLL_uBOLL       := strreplace(trim(slTmp.Strings[25 - 1]),'----','null') ;
          BOLL_dBOLL       := strreplace(trim(slTmp.Strings[26 - 1]),'----','null') ;
          BOLL_BOLL        := strreplace(trim(slTmp.Strings[27 - 1]),'----','null') ;
          MACD_DIF         := strreplace(trim(slTmp.Strings[28 - 1]),'----','null') ;
          MACD_MACD        := strreplace(trim(slTmp.Strings[29 - 1]),'----','null') ;
          MACD_DIF_MACD    := strreplace(trim(slTmp.Strings[30 - 1]),'----','null') ;
          DPO_DPO          := strreplace(trim(slTmp.Strings[31 - 1]),'----','null') ;
          DPO_6MA          := strreplace(trim(slTmp.Strings[32 - 1]),'----','null') ;

          //if shi_jian = '2015/10/08' then
          //  sql :='';

          if strtofloat(amount) <= 0.0 then
          begin
            continue ;
          end;

          if strtofloat(price_last_day) <> 0.0 then
          begin
            sql := 'insert into tb_stock_data_Daily '+
                   '(                   '+
                   '  code             ,'+
                   '  name             ,'+
                   '  shi_jian         ,'+
                   '  price_today_open ,'+
                   '  max_price        ,'+
                   '  min_price        ,'+
                   '  price_last_day   ,'+
                   '  price            ,'+
                   '  vol              ,'+
                   '  amount           ,'+
                   '  MA6              ,'+
                   '  MA12             ,'+
                   '  MA20             ,'+
                   '  MA30             ,'+
                   '  MA45             ,'+
                   '  MA60             ,'+
                   '  MA125            ,'+
                   '  MA250            ,'+
                   '  KDJ_K            ,'+
                   '  KDJ_D            ,'+
                   '  KDJ_J            ,'+
                   '  xstd_SLONG       ,'+
                   '  xstd_SSHORT      ,'+
                   '  xstd_LLONG       ,'+
                   '  xstd_LSHORT      ,'+
                   '  BOLL_uBOLL       ,'+
                   '  BOLL_dBOLL       ,'+
                   '  BOLL_BOLL        ,'+
                   '  MACD_DIF         ,'+
                   '  MACD_MACD        ,'+
                   '  MACD_DIF_MACD    ,'+
                   '  zhang_die_rate   ,'+
                   '  zhang_die        ,'+
                   '  DPO_DPO          ,'+
                   '  DPO_6MA           '+
                   ')                   '+
                   'values              '+
                   '(                   '+
                   '  ''' + code        +''','+
                   '  ''' + name        +''','+
                   'to_date(''' + shi_jian +'150000'',''yyyy/mm/ddhh24miss''),'+
                   '  ' + price_today_open +','+
                   '  ' + max_price        +','+
                   '  ' + min_price        +','+
                   '  ' + price_last_day   +','+
                   '  ' + price            +','+
                   '  ' + vol              +','+
                   '  ' + amount           +','+
                   '  ' + MA6              +','+
                   '  ' + MA12             +','+
                   '  ' + MA20             +','+
                   '  ' + MA30             +','+
                   '  ' + MA45             +','+
                   '  ' + MA60             +','+
                   '  ' + MA125            +','+
                   '  ' + MA250            +','+
                   '  ' + KDJ_K            +','+
                   '  ' + KDJ_D            +','+
                   '  ' + KDJ_J            +','+
                   '  ' + xstd_SLONG       +','+
                   '  ' + xstd_SSHORT      +','+
                   '  ' + xstd_LLONG       +','+
                   '  ' + xstd_LSHORT      +','+
                   '  ' + BOLL_uBOLL       +','+
                   '  ' + BOLL_dBOLL       +','+
                   '  ' + BOLL_BOLL        +','+
                   '  ' + MACD_DIF         +','+
                   '  ' + MACD_MACD        +','+
                   '  ' + MACD_DIF_MACD    +','+
                   '  ' + floattostr((strtofloat(price) - strtofloat(price_last_day))/strtofloat(price_last_day))+','+
                   '  ' + floattostr(strtofloat(price) - strtofloat(price_last_day))                             +','+
                   '  ' + DPO_DPO          +','+
                   '  ' + DPO_6MA          +' '+
                   ')'
            end
            else
            begin
              if row > 3 then
              begin
                sql := 'insert into tb_stock_data_Daily '+
                       '(                   '+
                       '  code             ,'+
                       '  name             ,'+
                       '  shi_jian         ,'+
                       '  price_today_open ,'+
                       '  max_price        ,'+
                       '  min_price        ,'+
                       '  price_last_day   ,'+
                       '  price            ,'+
                       '  vol              ,'+
                       '  amount           ,'+
                       '  MA6              ,'+
                       '  MA12             ,'+
                       '  MA20             ,'+
                       '  MA30             ,'+
                       '  MA45             ,'+
                       '  MA60             ,'+
                       '  MA125            ,'+
                       '  MA250            ,'+
                       '  KDJ_K            ,'+
                       '  KDJ_D            ,'+
                       '  KDJ_J            ,'+
                       '  xstd_SLONG       ,'+
                       '  xstd_SSHORT      ,'+
                       '  xstd_LLONG       ,'+
                       '  xstd_LSHORT      ,'+
                       '  BOLL_uBOLL       ,'+
                       '  BOLL_dBOLL       ,'+
                       '  BOLL_BOLL        ,'+
                       '  MACD_DIF         ,'+
                       '  MACD_MACD        ,'+
                       '  MACD_DIF_MACD    ,'+
                       '  zhang_die        ,'+
                       '  DPO_DPO          ,'+
                       '  DPO_6MA           '+
                       ')                   '+
                       'values              '+
                       '(                   '+
                       '  ''' + code        +''','+
                       '  ''' + name        +''','+
                       'to_date(''' + shi_jian +'150000'',''yyyy/mm/ddhh24miss''),'+
                       '  ' + price_today_open +','+
                       '  ' + max_price        +','+
                       '  ' + min_price        +','+
                       '  ' + price_last_day   +','+
                       '  ' + price            +','+
                       '  ' + vol              +','+
                       '  ' + amount           +','+
                       '  ' + MA6              +','+
                       '  ' + MA12             +','+
                       '  ' + MA20             +','+
                       '  ' + MA30             +','+
                       '  ' + MA45             +','+
                       '  ' + MA60             +','+
                       '  ' + MA125            +','+
                       '  ' + MA250            +','+
                       '  ' + KDJ_K            +','+
                       '  ' + KDJ_D            +','+
                       '  ' + KDJ_J            +','+
                       '  ' + xstd_SLONG       +','+
                       '  ' + xstd_SSHORT      +','+
                       '  ' + xstd_LLONG       +','+
                       '  ' + xstd_LSHORT      +','+
                       '  ' + BOLL_uBOLL       +','+
                       '  ' + BOLL_dBOLL       +','+
                       '  ' + BOLL_BOLL        +','+
                       '  ' + MACD_DIF         +','+
                       '  ' + MACD_MACD        +','+
                       '  ' + MACD_DIF_MACD    +','+
                       '  ' + floattostr(strtofloat(price) - strtofloat(price_last_day)) +','+
                       '  ' + DPO_DPO          +','+
                       '  ' + DPO_6MA          +' '+
                       ')' ;
              end
              else
              begin
                sql := 'insert into tb_stock_data_Daily '+
                       '(                   '+
                       '  code             ,'+
                       '  name             ,'+
                       '  shi_jian         ,'+
                       '  price_today_open ,'+
                       '  max_price        ,'+
                       '  min_price        ,'+
                       '  price_last_day   ,'+
                       '  price            ,'+
                       '  vol              ,'+
                       '  amount           ,'+
                       '  MA6              ,'+
                       '  MA12             ,'+
                       '  MA20             ,'+
                       '  MA30             ,'+
                       '  MA45             ,'+
                       '  MA60             ,'+
                       '  MA125            ,'+
                       '  MA250            ,'+
                       '  KDJ_K            ,'+
                       '  KDJ_D            ,'+
                       '  KDJ_J            ,'+
                       '  xstd_SLONG       ,'+
                       '  xstd_SSHORT      ,'+
                       '  xstd_LLONG       ,'+
                       '  xstd_LSHORT      ,'+
                       '  BOLL_uBOLL       ,'+
                       '  BOLL_dBOLL       ,'+
                       '  BOLL_BOLL        ,'+
                       '  MACD_DIF         ,'+
                       '  MACD_MACD        ,'+
                       '  MACD_DIF_MACD    ,'+
                       '  DPO_DPO          ,'+
                       '  DPO_6MA           '+
                       ')                   '+
                       'values              '+
                       '(                   '+
                       '  ''' + code        +''','+
                       '  ''' + name        +''','+
                       'to_date(''' + shi_jian +'150000'',''yyyy/mm/ddhh24miss''),'+
                       '  ' + price_today_open +','+
                       '  ' + max_price        +','+
                       '  ' + min_price        +','+
                       '  ' + price_last_day   +','+
                       '  ' + price            +','+
                       '  ' + vol              +','+
                       '  ' + amount           +','+
                       '  ' + MA6              +','+
                       '  ' + MA12             +','+
                       '  ' + MA20             +','+
                       '  ' + MA30             +','+
                       '  ' + MA45             +','+
                       '  ' + MA60             +','+
                       '  ' + MA125            +','+
                       '  ' + MA250            +','+
                       '  ' + KDJ_K            +','+
                       '  ' + KDJ_D            +','+
                       '  ' + KDJ_J            +','+
                       '  ' + xstd_SLONG       +','+
                       '  ' + xstd_SSHORT      +','+
                       '  ' + xstd_LLONG       +','+
                       '  ' + xstd_LSHORT      +','+
                       '  ' + BOLL_uBOLL       +','+
                       '  ' + BOLL_dBOLL       +','+
                       '  ' + BOLL_BOLL        +','+
                       '  ' + MACD_DIF         +','+
                       '  ' + MACD_MACD        +','+
                       '  ' + MACD_DIF_MACD    +','+
                       '  ' + DPO_DPO          +','+
                       '  ' + DPO_6MA          +' '+
                       ')';

              end;
            end ;

          res := db.ExecuteSql(sql , false , ire , resmsg ) ;
          if res<>0 then
            break;

          //inc(count);
          //if count >= 10000 then
          //begin
          //  db.commitTrans ;
          //  count := 0 ;
          //end;
          price_last_day := price ;
        finally
          inc(row);
        end;
      end;
      //db.commitTrans ;
      //xls.WorkBooks.Close;
      sql := 'select code,count(1) from         '+
             '(                                 '+
             '    select code,                  '+
             '           name                   '+
             '    from tb_stock_data_Daily where'+
             '      code=''' + code +        ''''+
             '    group by code,name            '+
             ')                                 '+
             'group by code                     '+
             'having count(1)>1                 ' ;

      res := db.OpenSql(sql , resmsg);

      if res=0 then
      begin
        if not db.RS.EOF then
        begin
          sql := 'update tb_stock_data_Daily set name = ''' + name + ''' where code = ''' + code + '''';
          res := db.ExecuteSql(sql , false , ire , resmsg ) ;
        end;
      end;

      db.RS.Close ;

      if res=0 then
        deletefile(PChar(pfileName)) ;
    except
      Err := Exception(ExceptObject);
      res := 1 ;
      resmsg:= err.Message + ',' + pfileName ;
      //Err.Destroy ;
    end;
  finally
    slTmp.Destroy ;
    timeSplit.Destroy;
    data.Destroy ;
    presMsg := resmsg;
    result := res;
  end;

end;


{
function TstockImportDaily.import(pfileName: string; var pResMsg:string): integer;
var
  name  : string ;
  slTmp : TStringList ;
  count : integer ;
  ire   : integer ;
  row   : integer ;

  shi_jian         : string ;
  price_today_open : string ;
  max_price        : string ;
  min_price        : string ;
  price            : string ;
  vol              : string ;
  amount           : string ;
  MA6         : string ;
  MA12        : string ;
  MA20        : string ;
  MA30        : string ;
  MA45        : string ;
  MA60        : string ;
  MA125       : string ;
  MA250       : string ;
  KDJ_K       : string ;
  KDJ_D       : string ;
  KDJ_J       : string ;
  xstd_SLONG  : string ;
  xstd_SSHORT : string ;
  xstd_LLONG  : string ;
  xstd_LSHORT : string ;
  BOLL_uBOLL  : string ;
  BOLL_dBOLL  : string ;
  BOLL_BOLL   : string ;
  MACD_DIF    : string ;
  MACD_MACD   : string ;
  MACD_DIF_MACD : string;

  fileName : string ;
  importList : TstockImportNameAndCode ;

  last_Shi_jian : string ;
  last_Price    : string ;

  append : boolean ;
  eof    : boolean ;

  DesRange:Variant;
begin
  slTmp := TStringList.Create ;
  slTmp.Clear ;

  fileName := getFileName( pfileName ) ;

  if fileName = '上证指数--技术分析--日  线--不除权.xls' then
  begin
    code := 'sh000001' ;
    name := '上证指数';
  end
  else if fileName='深证成指--技术分析--日  线--不除权.xls' then
  begin
    code := 'sz399001';
    name := '深证成指';
  end
  else if fileName = '报价--沪深Ａ股.xls'  then
  begin
    importList := TstockImportNameAndCode.Create ;
    importList.connstr := connstr ;
    res := importList.import(pfileName,presmsg) ;
    importList.Destroy ;
    result := res ;
    exit ;
  end
  else
  begin
    SplitStr(slTmp , fileName , '--');
    name := trim(sltmp.Strings[0]);
    slTmp.Clear ;

    sql := 'select code from tb_stock_list where name = ''' + name + '''';
    //res := db.Connect(connstr , resmsg);
    res := db.OpenSql(sql , resmsg);

    if db.RS.EOF then
    begin
      db.RS.Close ;
      //db.Disconnect(resMsg) ;
      pResMsg := '通过股票名字没有找到对应的股票代码' ;
      result := 1 ;
      exit ;
    end;
    code := db.RS.Fields['code'].Value ;
    db.RS.Close ;
  end;

  sql := 'select price,to_char(shi_jian,''yyyy/mm/dd'') shi_jian from tb_stock_data_daily where '+
         '  code = ''' + code + '''' +
         '    and ' +
         '  shi_jian = (select max(shi_jian) from tb_stock_data_daily where code = ''' + code + ''')' ;
  res := db.OpenSql(sql , resmsg);

  xls.workbooks.open(pfileName);
  append := true ;

  eof := db.RS.EOF ;
  if eof then
  begin
    append := false  ;

  end
  else
  begin
    append := true ;
    last_Price    := db.RS.Fields['price'].Value ;
    last_shi_jian := db.RS.Fields['shi_jian'].Value ;
    db.RS.Close ;

    DesRange := xls.workbooks[1].sheets[1].Cells.Find(last_shi_jian);
    //DesRange := DesRange.offset[1];
    Row:=DesRange.Row;
    price := xls.workbooks[1].sheets[1].cells[row,5].value ;

    if price <> last_price then
      append := false ;
  end;

  db.RS.Close ;

  if append then
  begin
    inc(row)
  end
  else
  begin
    if not eof then
    begin
      sql :='delete tb_stock_data_daily where code=''' + code +'''';
      res := db.ExecuteSql(sql , false , ire , resmsg ) ;
    end;
    row := 2 ;
  end;

  while not varisnull( xls.workbooks[1].sheets[1].cells[row,1].value ) do
  begin
    shi_jian         := xls.workbooks[1].sheets[1].cells[row,1].value ;

    if trim(shi_jian)='' then
      break ;

    price_today_open := xls.workbooks[1].sheets[1].cells[row,2].value ;
    max_price        := xls.workbooks[1].sheets[1].cells[row,3].value ;
    min_price        := xls.workbooks[1].sheets[1].cells[row,4].value ;
    price            := xls.workbooks[1].sheets[1].cells[row,5].value ;
    vol              := xls.workbooks[1].sheets[1].cells[row,6].value ;
    amount           := xls.workbooks[1].sheets[1].cells[row,7].value ;

    MA6              := xls.workbooks[1].sheets[1].cells[row,8].value ;
    MA12             := xls.workbooks[1].sheets[1].cells[row,9].value ;
    MA20             := xls.workbooks[1].sheets[1].cells[row,10].value ;
    MA30             := xls.workbooks[1].sheets[1].cells[row,11].value ;
    MA45             := xls.workbooks[1].sheets[1].cells[row,12].value ;
    MA60             := xls.workbooks[1].sheets[1].cells[row,13].value ;
    MA125            := xls.workbooks[1].sheets[1].cells[row,14].value ;
    MA250            := xls.workbooks[1].sheets[1].cells[row,15].value ;
    KDJ_K            := xls.workbooks[1].sheets[1].cells[row,17].value ;
    KDJ_D            := xls.workbooks[1].sheets[1].cells[row,18].value ;
    KDJ_J            := xls.workbooks[1].sheets[1].cells[row,19].value ;
    xstd_SLONG       := xls.workbooks[1].sheets[1].cells[row,21].value ;
    xstd_SSHORT      := xls.workbooks[1].sheets[1].cells[row,22].value ;
    xstd_LLONG       := xls.workbooks[1].sheets[1].cells[row,23].value ;
    xstd_LSHORT      := xls.workbooks[1].sheets[1].cells[row,24].value ;
    BOLL_uBOLL       := xls.workbooks[1].sheets[1].cells[row,25].value ;
    BOLL_dBOLL       := xls.workbooks[1].sheets[1].cells[row,26].value ;
    BOLL_BOLL        := xls.workbooks[1].sheets[1].cells[row,27].value ;
    MACD_DIF         := xls.workbooks[1].sheets[1].cells[row,28].value ;
    MACD_MACD        := xls.workbooks[1].sheets[1].cells[row,29].value ;
    MACD_DIF_MACD    := xls.workbooks[1].sheets[1].cells[row,30].value ;

    sql := 'insert into tb_stock_data_Daily '+
           '(                   '+
           '  code             ,'+
           '  name             ,'+
           '  shi_jian         ,'+
           '  price_today_open ,'+
           '  max_price        ,'+
           '  min_price        ,'+
           '  price            ,'+
           '  vol              ,'+
           '  amount           ,'+
           '  MA6              ,'+
           '  MA12             ,'+
           '  MA20             ,'+
           '  MA30             ,'+
           '  MA45             ,'+
           '  MA60             ,'+
           '  MA125            ,'+
           '  MA250            ,'+
           '  KDJ_K            ,'+
           '  KDJ_D            ,'+
           '  KDJ_J            ,'+
           '  xstd_SLONG       ,'+
           '  xstd_SSHORT      ,'+
           '  xstd_LLONG       ,'+
           '  xstd_LSHORT      ,'+
           '  BOLL_uBOLL       ,'+
           '  BOLL_dBOLL       ,'+
           '  BOLL_BOLL        ,'+
           '  MACD_DIF         ,'+
           '  MACD_MACD        ,'+
           '  MACD_DIF_MACD     '+
           ')                   '+
           'values              '+
           '(                   '+
           '  ''' + code        +''','+
           '  ''' + name        +''','+
           'to_date(''' + shi_jian +'150000'',''yyyy/mm/ddhh24miss''),'+
           '  ''' + price_today_open +''','+
           '  ''' + max_price        +''','+
           '  ''' + min_price        +''','+
           '  ''' + price            +''','+
           '  ''' + vol              +''','+
           '  ''' + amount           +''','+
           '  ''' + MA6              +''','+
           '  ''' + MA12             +''','+
           '  ''' + MA20             +''','+
           '  ''' + MA30             +''','+
           '  ''' + MA45             +''','+
           '  ''' + MA60             +''','+
           '  ''' + MA125            +''','+
           '  ''' + MA250            +''','+
           '  ''' + KDJ_K            +''','+
           '  ''' + KDJ_D            +''','+
           '  ''' + KDJ_J            +''','+
           '  ''' + xstd_SLONG       +''','+
           '  ''' + xstd_SSHORT      +''','+
           '  ''' + xstd_LLONG       +''','+
           '  ''' + xstd_LSHORT      +''','+
           '  ''' + BOLL_uBOLL       +''','+
           '  ''' + BOLL_dBOLL       +''','+
           '  ''' + BOLL_BOLL        +''','+
           '  ''' + MACD_DIF         +''','+
           '  ''' + MACD_MACD        +''','+
           '  ''' + MACD_DIF_MACD    +''' '+
           ')' ;
    res := db.ExecuteSql(sql , false , ire , resmsg ) ;

    inc(row);
  end;

  xls.WorkBooks.Close;
  deletefile(PChar(pfileName)) ;

  presMsg := '操作成功';
  result := 0;

end;
}
function TstockImportDaily.import(pFileList : TStringList ; var pResMsg : string ) : integer ;
var
  iLoopTime : integer ;
  res : integer ;
  resMsg : string ;
  ire : integer ;
begin
  { Place thread code here }

  //sql := 'truncate table tb_stock_data_daily';
  //res := db.Connect(connstr , resmsg);
  //res := db.ExecuteSql(sql , false , ire , resmsg);
  res := db.Connect(connstr , resmsg);
  for iLoopTime := 0 to pFileList.Count - 1 do
  begin
    res:= import(pFileList.Strings[iLoopTime] , resMsg)  ;
    if res<>0 then
    begin
      res := db.Disconnect( resmsg);
      pResMsg := resmsg;
      result := res ;
      exit;
    end;
  end;

  res := db.Disconnect( resmsg);
  pResMsg := resmsg;
  result := res ;

end;

end.
