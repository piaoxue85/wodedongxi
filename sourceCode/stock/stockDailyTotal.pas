unit stockDailyTotal;

interface
uses
  Unit_MathFuncs ,
  stockDaily ,
  ado,
  Controls ,
  System.SysUtils, System.Variants, System.Classes ;

type
  TstockDailyTotal = class(TObject)
    name                :string ;
    code                :string ;
    dailyTotal          :TStringList ;
    MASetting           :TStringList ;
    KDJSetting          :TStringList ;
  private
    sql : string;
    res : integer ;
    resMsg : string ;
    db : TXlsADO ;
    stockDaily : TstockDaily ;

    ValTmp  : TStringList ;
    EmaVal1 : TStringList ;   //[0]-SLONG , [1]-SSHORT , [2]-LLONG , [3]-LSHORT
    EmaVal2 : TStringList ;   //[0]-SLONG , [1]-SSHORT , [2]-LLONG , [3]-LSHORT

    function  enoughTime(lastTop, thisTop: TstockDaily;intervalDay : integer): boolean;
    procedure getMA  (dayCursor : integer );
    procedure getKDJ (dayCursor : integer ) ;
    procedure getXSTD(dayCursor : integer ) ;

    function EMA( pValue, pLastValue , pN : double ): double;

  public
    connstr: string  ;

    constructor Create(pMaSetting : TStringList ; pKDJSetting : TStringList);
    Destructor  Destroy ;

    function getCodeList : TStringList ;

    function findTopBottom(var pTop : TStringList ; var pBottom : TStringList ; var pResMsg : string  ) : integer ;

    procedure getDay     (pcode : string );
    procedure getWeek    (pcode : string );
    procedure getMonth   (pcode : string );
    procedure getQuarter (pcode : string );
    procedure getHalfYear(pcode : string );
    procedure getYear    (pcode : string );

  end;

implementation

{ TstockDaily }



{ TstockDailyTotal }

constructor TstockDailyTotal.Create( pMaSetting : TStringList ; pKDJSetting : TStringList);
begin
  inherited create ;
  connstr :='Provider=OraOLEDB.Oracle.1;Password=didierg160;Persist Security Info=True;User ID=c##stock;Data Source=myoracle';
  MASetting := pMASetting ;
  KDJSetting := pKDJSetting ;
  self.dailyTotal := TStringList.Create ;

  EmaVal1 := TStringList.Create ;
  EmaVal1.Clear ;
  EmaVal1.Add('');
  EmaVal1.Add('');
  EmaVal1.Add('');
  EmaVal1.Add('');

  EmaVal2 := TStringList.Create ;
  EmaVal2.Clear ;
  EmaVal2.Add('');
  EmaVal2.Add('');
  EmaVal2.Add('');
  EmaVal2.Add('');
  //self.getDay( pcode ) ;
  //self.getYear( pcode ) ;
  //self.getMonth(pcode);
  //self.getQuarter(pcode);
  //self.getHalfYear( pcode );
  //self.getWeek( pcode );
end;

destructor TstockDailyTotal.Destroy;
begin
  dailyTotal.destroy;
  MASetting.destroy;
  KDJSetting.destroy;
  db.destroy;
  stockDaily.destroy;
  ValTmp.destroy;
  EmaVal1.destroy;
  EmaVal2.destroy;
  inherited destroy ;
end;


function TstockDailyTotal.enoughTime(lastTop, thisTop: TstockDaily;intervalDay : integer): boolean;
var
  dInteval : double ;
begin
  sql := 'select (to_date(''' + lastTop.shi_jian +''',''yyyymmddhh24miss'') + '+inttostr(intervalDay) +') - ' +
         '       to_date(''' + thisTop.shi_jian + ''',''yyyymmddhh24miss'') as inteval from dual';

  db := TXlsADO.Create ;
  res := db.Connect(connstr,resMsg);
  res := db.OpenSql(sql , resMsg);

  dInteval := db.RS.Fields['inteval'].Value ;

  db.RS.Close ;
  db.Disconnect(resMsg) ;
  db.Destroy ;

  if dInteval <= 0.0 then
    result := true
  else
    result := false ;

end;

function TstockDailyTotal.findTopBottom(var pTop, pBottom: TStringList;
  var pResMsg: string): integer;
var
  iLoopTime : integer ;
  //daily : TStockDaily ;
  top : TStockDaily ;
  bottom : TStockDaily ;
  newTop:boolean ;
  newBottom : boolean ;

  stmp : string ;

begin

  if (self.dailyTotal.Count<1) then
  begin
    pResMsg := '每日数据为空';
    Result := -1 ;
    exit;
  end;

  pTop := TStringlist.Create ;
  pBottom := TStringList.Create ;

  pTop.clear ;
  pBottom.clear;

  newTop := true ;
  newBottom := false ;

  StockDaily :=  TStockDaily.Create ;
  StockDaily.name :=TStockDaily(dailyTotal.Objects[0]).name ;
  StockDaily.code :=TStockDaily(dailyTotal.Objects[0]).code ;
  StockDaily.price := 0;
  StockDaily.price_last_day := 0 ;
  StockDaily.price_today_open := 0 ;
  StockDaily.max_price := 0 ;
  StockDaily.min_price := 0 ;
  StockDaily.shi_jian := '19891231000000';

  pTop.AddObject(StockDaily.shi_jian + ',收盘价：'+floattostr( StockDaily.price)+',今开'+floattostr( StockDaily.price_today_open) + ',最高：'+floattostr( StockDaily.max_price )+ ',最低：' + floattostr( StockDaily.min_price) ,StockDaily);
  pBottom.AddObject(StockDaily.shi_jian + ',收盘价：'+floattostr( StockDaily.price)+',今开'+floattostr( StockDaily.price_today_open) + ',最高：'+floattostr( StockDaily.max_price )+ ',最低：' + floattostr( StockDaily.min_price) ,StockDaily);

  for iLoopTime := 0 to dailyTotal.Count - 1 do
  begin
    StockDaily := TStockDaily(dailyTotal.Objects[iLoopTime]) ;


    if iLoopTime = 0 then
    begin
      //pTop.AddObject(StockDaily.shi_jian + ',收盘价：'+floattostr( StockDaily.price)+',今开'+floattostr( StockDaily.price_today_open) + ',最高：'+floattostr( StockDaily.max_price )+ ',最低：' + floattostr( StockDaily.min_price) ,StockDaily);
      //pBottom.AddObject(StockDaily.shi_jian + ',收盘价：'+floattostr( StockDaily.price)+',今开'+floattostr( StockDaily.price_today_open) + ',最高：'+floattostr( StockDaily.max_price )+ ',最低：' + floattostr( StockDaily.min_price) ,StockDaily);
      continue ;
    end;


    if StockDaily.shi_jian = '19910522150000' then
      stmp := '';

    if (StockDaily.max_price > TStockDaily(dailyTotal.Objects[iLoopTime-1]).max_price) and
       (StockDaily.price > TStockDaily(dailyTotal.Objects[iLoopTime-1]).price)
    then
    begin
      if (StockDaily.max_price > TStockDaily(pBottom.Objects[pBottom.Count-1]).min_price*1.2)
      then
      begin
        if newtop  and (enoughTime(TStockDaily(pTop.Objects[pTop.Count-1]) , StockDaily , 120)  )  then
        begin
          newTop := false ;
          newBottom := true ;
          pTop.AddObject(StockDaily.shi_jian + ',收盘价：'+floattostr( StockDaily.price)+',今开'+floattostr( StockDaily.price_today_open) + ',最高：'+floattostr( StockDaily.max_price )+ ',最低：' + floattostr( StockDaily.min_price) ,StockDaily);
        end
        else
        begin

          if StockDaily.max_price>=TStockDaily(pTop.Objects[pTop.Count-1]).max_price then
          begin
            pTop.Delete(pTop.Count-1);
            pTop.AddObject(StockDaily.shi_jian + ',收盘价：'+floattostr( StockDaily.price)+',今开'+floattostr( StockDaily.price_today_open) + ',最高：'+floattostr( StockDaily.max_price )+ ',最低：' + floattostr( StockDaily.min_price) ,StockDaily);
          end;
        end;

      end;
    end;

    //
    if (StockDaily.min_price < TStockDaily(dailyTotal.Objects[iLoopTime-1]).min_price) and
       (StockDaily.price < TStockDaily(dailyTotal.Objects[iLoopTime-1]).price)
    then
    begin

      if (StockDaily.min_price < TStockDaily(pTop.Objects[pTop.Count-1]).max_price*0.8) then
      begin
        if newBottom  and (enoughTime(TStockDaily(pBottom.Objects[pBottom.Count-1]) , StockDaily , 120)) then
        begin
          newTop    := true ;
          newBottom := false ;
          pBottom.AddObject(StockDaily.shi_jian + ',收盘价：'+floattostr( StockDaily.price)+',今开'+floattostr( StockDaily.price_today_open) + ',最高：'+floattostr( StockDaily.max_price )+ ',最低：' + floattostr( StockDaily.min_price) ,StockDaily);
        end
        else
        begin
            pBottom.Delete(pBottom.Count-1);
            pBottom.AddObject(StockDaily.shi_jian + ',收盘价：'+floattostr( StockDaily.price)+',今开'+floattostr( StockDaily.price_today_open) + ',最高：'+floattostr( StockDaily.max_price )+ ',最低：' + floattostr( StockDaily.min_price) ,StockDaily);
        end;
      end;
    end;
  end;
  resMsg := 'success';
  result := 0 ;

end;

function TstockDailyTotal.getCodeList: TStringList;
var
  list : TStringList;
begin
  //sql := 'select * from (select distinct(code) code from tb_stock_data_Daily where code in (''sh000001'',''002202''))';
  sql := 'select distinct(code) code from tb_stock_data_Daily ';
  //sql := 'select * from (select distinct(code) code from tb_stock_data_Daily )where rownum<11';

  db := TXlsADO.Create ;
  res := db.Connect(connstr,resMsg);
  res := db.OpenSql(sql , resMsg);

  if  db.RS.EOF then
  begin
    db.RS.Close ;
    db.Disconnect(resMsg);
    db.Destroy ;
    exit ;
  end;

  list := TStringList.Create ;
  db.RS.MoveFirst ;

  while not db.RS.EOF do
  begin
    list.Add( db.RS.Fields['code'].Value );
    db.RS.MoveNext ;
  end;

  db.RS.Close ;
  db.Disconnect(resMsg) ;
  db.Destroy ;
  result := list ;
end;

procedure TstockDailyTotal.getDay(pcode : string );
begin
  sql := 'select '+
  			 'name             ,'+
         'code             ,'+
         'price            ,'+
         'price_last_day   ,'+
         'price_today_open ,'+
         'max_price        ,'+
         'min_price        ,'+
         'to_char(shi_jian,''yyyymmddhh24miss'') shi_jian '+
         'decode(MA6          ,null,-999999.9,MA6          ) MA6           ,'+
         'decode(MA12         ,null,-999999.9,MA12         ) MA12          ,'+
         'decode(MA20         ,null,-999999.9,MA20         ) MA20          ,'+
         'decode(MA30         ,null,-999999.9,MA30         ) MA30          ,'+
         'decode(MA45         ,null,-999999.9,MA45         ) MA45          ,'+
         'decode(MA60         ,null,-999999.9,MA60         ) MA60          ,'+
         'decode(MA125        ,null,-999999.9,MA125        ) MA125         ,'+
         'decode(MA250        ,null,-999999.9,MA250        ) MA250         ,'+
         'decode(KDJ_K        ,null,-999999.9,KDJ_K        ) KDJ_K         ,'+
         'decode(KDJ_D        ,null,-999999.9,KDJ_D        ) KDJ_D         ,'+
         'decode(KDJ_J        ,null,-999999.9,KDJ_J        ) KDJ_J         ,'+
         'decode(xstd_SLONG   ,null,-999999.9,xstd_SLONG   ) xstd_SLONG    ,'+
         'decode(xstd_SSHORT  ,null,-999999.9,xstd_SSHORT  ) xstd_SSHORT   ,'+
         'decode(xstd_LLONG   ,null,-999999.9,xstd_LLONG   ) xstd_LLONG    ,'+
         'decode(xstd_LSHORT  ,null,-999999.9,xstd_LSHORT  ) xstd_LSHORT   ,'+
         'decode(BOLL_uBOLL   ,null,-999999.9,BOLL_uBOLL   ) BOLL_uBOLL    ,'+
         'decode(BOLL_dBOLL   ,null,-999999.9,BOLL_dBOLL   ) BOLL_dBOLL    ,'+
         'decode(BOLL_BOLL    ,null,-999999.9,BOLL_BOLL    ) BOLL_BOLL     ,'+
         'decode(MACD_DIF     ,null,-999999.9,MACD_DIF     ) MACD_DIF      ,'+
         'decode(MACD_MACD    ,null,-999999.9,MACD_MACD    ) MACD_MACD     ,'+
         'decode(MACD_DIF_MACD,null,-999999.9,MACD_DIF_MACD) MACD_DIF_MACD  '+
         'from tb_stock_data_Daily where '+
         '  code ='''+ pCode  + ''' order by shi_jian asc';

  db := TXlsADO.Create ;
  res := db.Connect(connstr,resMsg);

  res := db.OpenSql(sql , resMsg);

  if  db.RS.EOF then
  begin
    db.RS.Close ;
    db.Disconnect(resMsg);
    db.Destroy ;
    exit ;
  end;

  db.RS.MoveFirst ;
  {
  EmaVal1 := TStringList.Create ;
  EmaVal1.Clear ;
  EmaVal1.Add('');
  EmaVal1.Add('');
  EmaVal1.Add('');
  EmaVal1.Add('');

  EmaVal2 := TStringList.Create ;
  EmaVal2.Clear ;
  EmaVal2.Add('');
  EmaVal2.Add('');
  EmaVal2.Add('');
  EmaVal2.Add('');
  }

  while not db.RS.EOF do
  begin
    stockDaily := TstockDaily.Create ;
    stockDaily.name             := db.RS.Fields['name'].Value             ;
    stockDaily.code             := db.RS.Fields['code'].Value             ;
    stockDaily.price            := db.RS.Fields['price'].Value            ;
    stockDaily.price_last_day   := db.RS.Fields['price_last_day'].Value   ;
    stockDaily.price_today_open := db.RS.Fields['price_today_open'].Value ;
    stockDaily.max_price        := db.RS.Fields['max_price'].Value        ;
    stockDaily.min_price        := db.RS.Fields['min_price'].Value        ;
    stockDaily.shi_jian         := db.RS.Fields['shi_jian'].Value         ;
    stockDaily.MA6          := db.RS.Fields['MA6'          ].Value ;
    stockDaily.MA12         := db.RS.Fields['MA12'         ].Value ;
    stockDaily.MA20         := db.RS.Fields['MA20'         ].Value ;
    stockDaily.MA30         := db.RS.Fields['MA30'         ].Value ;
    stockDaily.MA45         := db.RS.Fields['MA45'         ].Value ;
    stockDaily.MA60         := db.RS.Fields['MA60'         ].Value ;
    stockDaily.MA125        := db.RS.Fields['MA125'        ].Value ;
    stockDaily.MA250        := db.RS.Fields['MA250'        ].Value ;
    stockDaily.KDJ_K        := db.RS.Fields['KDJ_K'        ].Value ;
    stockDaily.KDJ_D        := db.RS.Fields['KDJ_D'        ].Value ;
    stockDaily.KDJ_J        := db.RS.Fields['KDJ_J'        ].Value ;
    stockDaily.xstd_SLONG   := db.RS.Fields['xstd_SLONG'   ].Value ;
    stockDaily.xstd_SSHORT  := db.RS.Fields['xstd_SSHORT'  ].Value ;
    stockDaily.xstd_LLONG   := db.RS.Fields['xstd_LLONG'   ].Value ;
    stockDaily.xstd_LSHORT  := db.RS.Fields['xstd_LSHORT'  ].Value ;
    stockDaily.BOLL_uBOLL   := db.RS.Fields['BOLL_uBOLL'   ].Value ;
    stockDaily.BOLL_dBOLL   := db.RS.Fields['BOLL_dBOLL'   ].Value ;
    stockDaily.BOLL_BOLL    := db.RS.Fields['BOLL_BOLL'    ].Value ;
    stockDaily.MACD_DIF     := db.RS.Fields['MACD_DIF'     ].Value ;
    stockDaily.MACD_MACD    := db.RS.Fields['MACD_MACD'    ].Value ;
    stockDaily.MACD_DIF_MACD:= db.RS.Fields['MACD_DIF_MACD'].Value ;

    self.dailyTotal.AddObject(stockDaily.shi_jian,stockDaily) ;

    //getMA  (dailyTotal.Count - 1);
    //getKDJ (dailyTotal.Count - 1);
    //getXSTD(dailyTotal.Count - 1);

    db.RS.MoveNext ;
  end;

  db.RS.Close ;
  db.Disconnect(resMsg) ;
  db.Destroy ;
end;

procedure TstockDailyTotal.getHalfYear;
var
  max_Half   : string ;
  min_Half   : string ;
  cursor     : string ;
  first_day  : string ;
  last_day   : string ;
  iloopTime  : integer ;
  last_price : double ;
  sTmp : string;
begin
  sql := 'select f_getHalfYear(max(shi_jian)) max_Half , f_getHalfYear(min(shi_jian)) min_Half from tb_stock_data_Daily where code ='''+
          pCode  + '''';

  db  := TXlsADO.Create ;
  res := db.Connect(connstr,resMsg);
  res := db.OpenSql(sql , resMsg);

  if  db.RS.EOF then
  begin
    db.RS.Close ;
    db.Disconnect(resMsg);
    db.Destroy ;
    exit ;
  end;

  self.dailyTotal.Clear ;

  min_Half  := db.RS.Fields['min_Half'].Value ;
  max_Half  := db.RS.Fields['max_Half'].Value ;

  db.RS.Close ;

  cursor := min_Half ;
  last_price := 0.0 ;
  while strtoint(cursor) <= strtoint(max_Half) do
  begin

    if cursor = '1996' then
      stmp:= '';

    //赋值股票代码
    StockDaily.code := pCode ;

    sql := 'select '+
           '       sum(vol)                                    vol       ,'+
           '       sum(amount)                                 amount    ,'+
           '       to_char(min(shi_jian),''yyyymmddhh24miss'') first_day ,'+
           '       to_char(max(shi_jian),''yyyymmddhh24miss'') last_day  ,'+
           '       max(max_price)                             max_price  ,'+
           '       min(min_price)                             min_price   '+
           'from tb_stock_data_Daily where                                '+
           '  code = ''' + pCode +                                    '''' +
           '    and  ' +
           '  f_getHalfYear(shi_jian ) = ''' + cursor + '''';

    res := db.OpenSql(sql , resMsg);

    if  db.RS.EOF then
    begin
      db.RS.Close ;
      db.Disconnect(resMsg);
      db.Destroy ;
      exit ;
    end;

    StockDaily := TStockDaily.Create ;
    first_day  := db.RS.Fields['first_day'].Value ;
    last_day   := db.RS.Fields['last_day' ].Value ;

    StockDaily.max_price := db.RS.Fields['max_price'].Value ;
    StockDaily.min_price := db.RS.Fields['min_price'].Value ;
    StockDaily.vol       := db.RS.Fields['vol'      ].Value ;
    StockDaily.amount    := db.RS.Fields['amount'   ].Value ;
    StockDaily.shi_jian := last_day ;

    db.RS.Close ;

    sql := 'select * from                                     '+
           '(                                                 '+
           '  select price_today_open                         '+
           '  from tb_stock_data_Daily where                  '+
           '    shi_jian = to_date('''+first_day+''',''yyyymmddhh24miss'') '+
           ')a,                                               '+
           '(                                                 '+
           '  select price                                    '+
           '  from tb_stock_data_Daily where                  '+
           '    shi_jian = to_date('''+last_day+''',''yyyymmddhh24miss'') '+
           ')b';

    res := db.OpenSql(sql , resMsg);
    StockDaily.price_today_open := db.RS.Fields['price_today_open'].Value ;
    StockDaily.price            := db.RS.Fields['price'           ].Value ;
    db.RS.Close ;
    StockDaily.price_last_day :=  last_price ;
    last_price := StockDaily.price ;
    self.dailyTotal.AddObject(StockDaily.shi_jian + ',收盘价：'+floattostr( StockDaily.price)+',今开'+floattostr( StockDaily.price_today_open) + ',最高：'+floattostr( StockDaily.max_price )+ ',最低：' + floattostr( StockDaily.min_price) ,StockDaily);

    if strtoint( copy(cursor,6,1)) + 1 <= 2 then
    begin
      cursor := copy(cursor,1,4) + inttostr(strtoint( copy(cursor,6,1) )+ 1);
    end
    else
    begin
      cursor := inttostr( strtoint(copy(cursor,1,4)) + 1 ) + '01';
    end;

    getMA  (dailyTotal.Count - 1);
    getKDJ (dailyTotal.Count - 1);
    getXSTD(dailyTotal.Count - 1);

  end;



end;

procedure TstockDailyTotal.getKDJ(dayCursor: integer);
var
  rsv : double ;
  Ln : double ;
  Hn : double ;
  K : double ;
  d : double ;
  J : double ;
  max : TStringList ;
  min : TStringList ;

  loopTime : integer ;
begin

  if dayCursor < strtoint( kdjsetting.Strings[0]) - 1 then
    exit ;

  max := TStringList.Create ;
  min := TStringList.Create ;

  max.Clear ;
  min.Clear ;
  if daycursor >= strtoint( kdjsetting.Strings[0])  then
  begin
    for loopTime := 0 to strtoint( kdjsetting.Strings[0]) - 1 do
    begin
      max.Add( floattostr( TStockDaily( self.dailyTotal.Objects[ dayCursor - loopTime]).max_price ) ) ;
      min.Add( floattostr( TStockDaily( self.dailyTotal.Objects[ dayCursor - loopTime]).min_price ) ) ;
    end;
    Hn := getMax( max ) ;
    Ln := getMin( min ) ;
  end;


  max.Destroy ;
  min.Destroy ;

  if (Hn - Ln) <> 0 then
  begin
    rsv :=((TStockDaily( self.dailyTotal.Objects[dayCursor]).price - Ln )/(Hn - Ln))*100 ;
    if TStockDaily( self.dailyTotal.Objects[dayCursor - 1]).KDJValues.Count  < 1 then
    begin
      //k := ( 2/3*50 ) + (1/3)*rsv ;
      //d := ( 2/3*50 ) + (1/3)*k   ;
      k:=50.0 ;
      d:=50.0 ;
    end
    else
    begin
      k := ( 2/3* strtofloat( TStockDaily( self.dailyTotal.Objects[dayCursor - 1]).KDJValues.Strings[0]) ) + (1/3)*rsv ;
      d := ( 2/3* strtofloat( TStockDaily( self.dailyTotal.Objects[dayCursor - 1]).KDJValues.Strings[1]) ) + (1/3)*k   ;
    end;

    if ( strtoint( kdjsetting.Strings[3] ) = 1 )  then
      j := 3*d - 2*k
    else
      j := 3*k - 2*d ;
  end
  else
  begin
    k:=50.0 ;
    d:=50.0 ;
    j:=50.0 ;
  end ;
  TStockDaily( self.dailyTotal.Objects[dayCursor-1]).KDJValues.Clear ;
  TStockDaily( self.dailyTotal.Objects[dayCursor-1]).KDJValues.add(floattostr(k));
  TStockDaily( self.dailyTotal.Objects[dayCursor-1]).KDJValues.add(floattostr(d));
  TStockDaily( self.dailyTotal.Objects[dayCursor-1]).KDJValues.add(floattostr(j));

end;

procedure TstockDailyTotal.getMA(dayCursor: integer);
var
  iLoopDay : integer ;
  iLoopMASetting : integer ;
  sumPrice : double ;
begin
  for iLoopMASetting := 0 to self.MASetting.Count -1 do
  begin
    if dayCursor < MASetting.Strings[iLoopMASetting].ToInteger -1 then
    begin
      continue;
    end;
    sumPrice := 0.0 ;

    for iLoopDay := 0 to strtoint(MASetting.Strings[iLoopMASetting]) - 1 do
    begin
      sumPrice := sumPrice + TStockDaily( self.dailyTotal.Objects[dayCursor - iLoopDay] ).price ;
    end;
    TStockDaily( self.dailyTotal.Objects[dayCursor] ).MAValues.Add(floattostr(sumPrice/strtofloat(MASetting.Strings[iLoopMASetting])));
  end;

end;

procedure TstockDailyTotal.getMonth;
var
  min_month  : string ;
  max_month  : string ;
  cursor     : string ;
  first_day  : string ;
  last_day   : string ;
  //iloopTime  : integer ;
  sTmp : string;

  last_price : double ;
begin
  sql := 'select to_char(max(shi_jian),''yyyymm'') max_month , to_char(min(shi_jian),''yyyymm'') min_month  from  tb_stock_data_Daily where code ='''+
          pCode  + '''';

  db  := TXlsADO.Create ;
  res := db.Connect(connstr,resMsg);
  res := db.OpenSql(sql , resMsg);

  if  db.RS.EOF then
  begin
    db.RS.Close ;
    db.Disconnect(resMsg);
    db.Destroy ;
    exit ;
  end;

  self.dailyTotal.Clear ;

  min_month  := db.RS.Fields['min_month'].Value ;
  max_month  := db.RS.Fields['max_month'].Value ;

  db.RS.Close ;

  cursor := min_month ;
  last_price := 0.0 ;
  while strtoint(cursor) <= strtoint(max_month) do
  begin


    if cursor = '1996' then
      stmp:= '';

    //赋值股票代码
    StockDaily.code := pCode ;

    sql := 'select to_char(add_months(to_date('''+cursor+''',''yyyymm''),1),''yyyymm'') next_month , '+
           '       to_char(min(shi_jian),''yyyymmddhh24miss'') first_day ,'+
           '       to_char(max(shi_jian),''yyyymmddhh24miss'') last_day  ,'+
           '       sum(vol)                                    vol       ,'+
           '       sum(amount)                                 amount    ,'+
           '       max(max_price)                             max_price  ,'+
           '       min(min_price)                             min_price   '+
           'from tb_stock_data_Daily where                                '+
           '  code = ''' + pCode +                                    '''' +
           '    and  ' +
           '  price > 0 ' +
           '     and ' +
           '  to_char(shi_jian,''yyyymm'') = ''' + cursor + '''';

    res := db.OpenSql(sql , resMsg);

    if  db.RS.EOF then
    begin
      db.RS.Close ;
      db.Disconnect(resMsg);
      db.Destroy ;
      exit ;
    end;

    StockDaily := TStockDaily.Create ;

    first_day := db.RS.Fields['first_day'].Value ;
    last_day  := db.RS.Fields['last_day' ].Value ;
    cursor    := db.RS.Fields['next_month'].Value ;

    StockDaily.max_price := db.RS.Fields['max_price'].Value ;
    StockDaily.min_price := db.RS.Fields['min_price'].Value ;
    StockDaily.vol       := db.RS.Fields['vol'      ].Value ;
    StockDaily.amount    := db.RS.Fields['amount'   ].Value ;

    StockDaily.shi_jian := last_day ;

    db.RS.Close ;

    sql := 'select * from                                     '+
           '(                                                 '+
           '  select price_today_open                         '+
           '  from tb_stock_data_Daily where                  '+
           '    shi_jian = to_date('''+first_day+''',''yyyymmddhh24miss'') '+
           ')a,                                               '+
           '(                                                 '+
           '  select price                                    '+
           '  from tb_stock_data_Daily where                  '+
           '    shi_jian = to_date('''+last_day+''',''yyyymmddhh24miss'') '+
           ')b';

    res := db.OpenSql(sql , resMsg);
    StockDaily.price_today_open := db.RS.Fields['price_today_open'].Value ;
    StockDaily.price            := db.RS.Fields['price'           ].Value ;
    StockDaily.price_last_day   := last_price ;
    db.RS.Close ;

    last_price := StockDaily.price ;

    self.dailyTotal.AddObject(StockDaily.shi_jian + ',收盘价：'+floattostr( StockDaily.price)+',今开'+floattostr( StockDaily.price_today_open) + ',最高：'+floattostr( StockDaily.max_price )+ ',最低：' + floattostr( StockDaily.min_price) ,StockDaily);

    getMA  (dailyTotal.Count - 1);
    getKDJ (dailyTotal.Count - 1);
    getXSTD(dailyTotal.Count - 1);
  end;


end;

procedure TstockDailyTotal.getQuarter;
var
  max_Quarter: string ;
  min_Quarter: string ;
  cursor     : string ;
  first_day  : string ;
  last_day   : string ;
  last_price : double ;
  sTmp : string;
begin
  sql := 'select to_char(max(shi_jian),''yyyyq'') max_Quarter , to_char(min(shi_jian),''yyyyq'') min_Quarter from tb_stock_data_Daily where code ='''+
          pCode  + '''';

  db  := TXlsADO.Create ;
  res := db.Connect(connstr,resMsg);
  res := db.OpenSql(sql , resMsg);

  if  db.RS.EOF then
  begin
    db.RS.Close ;
    db.Disconnect(resMsg);
    db.Destroy ;
    exit ;
  end;

  self.dailyTotal.Clear ;

  min_Quarter  := db.RS.Fields['min_Quarter'].Value ;
  max_Quarter  := db.RS.Fields['max_Quarter'].Value ;

  db.RS.Close ;

  cursor := min_Quarter ;
  last_price := 0.0 ;
  while strtoint(cursor) <= strtoint(max_Quarter) do
  begin
    StockDaily := TStockDaily.Create ;

    if cursor = '1996' then
      stmp:= '';

    //赋值股票代码
    StockDaily.code := pCode ;

    sql := 'select '+
           '       sum(vol)                                    vol       ,'+
           '       sum(amount)                                 amount    ,'+
           '       to_char(min(shi_jian),''yyyymmddhh24miss'') first_day ,'+
           '       to_char(max(shi_jian),''yyyymmddhh24miss'') last_day  ,'+
           '       max(max_price)                              max_price ,'+
           '       min(min_price)                              min_price  '+
           'from tb_stock_data_Daily where                                '+
           '  code = ''' + pCode +                                    '''' +
           '    and  ' +
           '  to_char(shi_jian,''yyyyq'') = ''' + cursor + '''';

    res := db.OpenSql(sql , resMsg);

    if  db.RS.EOF then
    begin
      db.RS.Close ;
      db.Disconnect(resMsg);
      db.Destroy ;
      exit ;
    end;

    first_day := db.RS.Fields['first_day'].Value ;
    last_day  := db.RS.Fields['last_day' ].Value ;

    StockDaily.max_price := db.RS.Fields['max_price'].Value ;
    StockDaily.min_price := db.RS.Fields['min_price'].Value ;
    StockDaily.vol       := db.RS.Fields['vol'      ].Value ;
    StockDaily.amount    := db.RS.Fields['amount'   ].Value ;
    StockDaily.shi_jian  := last_day ;

    db.RS.Close ;

    sql := 'select * from                                     '+
           '(                                                 '+
           '  select price_today_open                         '+
           '  from tb_stock_data_Daily where                  '+
           '    shi_jian = to_date('''+first_day+''',''yyyymmddhh24miss'') '+
           ')a,                                               '+
           '(                                                 '+
           '  select price                                    '+
           '  from tb_stock_data_Daily where                  '+
           '    shi_jian = to_date('''+last_day+''',''yyyymmddhh24miss'') '+
           ')b';

    res := db.OpenSql(sql , resMsg);
    StockDaily.price_today_open := db.RS.Fields['price_today_open'].Value ;
    StockDaily.price            := db.RS.Fields['price'    ].Value ;
    db.RS.Close ;
    StockDaily.price_last_day :=  last_price ;
    last_price := StockDaily.price ;

    self.dailyTotal.AddObject(StockDaily.shi_jian + ',收盘价：'+floattostr( StockDaily.price)+',今开'+floattostr( StockDaily.price_today_open) + ',最高：'+floattostr( StockDaily.max_price )+ ',最低：' + floattostr( StockDaily.min_price) ,StockDaily);

    if strtoint( copy(cursor,5,1)) + 1 <=4 then
    begin
      cursor := copy(cursor,1,4) + inttostr(strtoint( copy(cursor,5,1) )+ 1);
    end
    else
    begin
      cursor := inttostr( strtoint(copy(cursor,1,4)) + 1 ) + '1';
    end;

    getMA  (dailyTotal.Count - 1);
    getKDJ (dailyTotal.Count - 1);
    getXSTD(dailyTotal.Count - 1);
  end;


end;

{
procedure TstockDailyTotal.getWeek;
var
  max_Week   : string ;
  min_Week   : string ;
  cursor     : string ;
  first_day  : string ;
  last_day   : string ;
  last_price : double ;

  sTmp : string;
begin
  sql := 'select to_char(trunc(max(shi_jian),''d''),''yyyymmddhh24miss'') max_Week , to_char(trunc(min(shi_jian),''d''),''yyyymmddhh24miss'') min_Week from tb_stock_data_Daily where code ='''+
          pCode  + '''';

  db  := TXlsADO.Create ;
  res := db.Connect(connstr,resMsg);
  res := db.OpenSql(sql , resMsg);

  if  db.RS.EOF then
  begin
    db.RS.Close ;
    db.Disconnect(resMsg);
    db.Destroy ;
    exit ;
  end;

  self.dailyTotal.Clear ;

  max_Week  := db.RS.Fields['max_Week'].Value ;
  min_Week  := db.RS.Fields['min_Week'].Value ;

  db.RS.Close ;

  cursor := min_Week ;
  last_price := 0.0 ;
  while strtofloat(cursor) <= strtofloat(max_Week) do
  begin
    StockDaily := TStockDaily.Create ;

    //if cursor = '1996' then
    //  stmp:= '';

    //赋值股票代码
    StockDaily.code := pCode ;

    sql := 'select '+
           '       to_char(to_date(''' + cursor + ''',''yyyymmddhh24miss'') + 7,''yyyymmddhh24miss'') next_cursor,' +
           '       sum(vol)                                    vol       ,'+
           '       sum(amount)                                 amount    ,'+
           '       to_char(min(shi_jian),''yyyymmddhh24miss'') first_day ,'+
           '       to_char(max(shi_jian),''yyyymmddhh24miss'') last_day  ,'+
           '       max(max_price)                              max_price ,'+
           '       min(min_price)                              min_price  '+
           'from tb_stock_data_Daily where                                '+
           '  code = ''' + pCode +                                    '''' +
           '    and  ' +
           '  trunc(shi_jian,''d'') = to_date(''' + cursor + ''',''yyyymmddhh24miss'')';

    res := db.OpenSql(sql , resMsg);

    if  db.RS.EOF then
    begin
      db.RS.Close ;
      db.Disconnect(resMsg);
      db.Destroy ;
      exit ;
    end;

    cursor    := db.RS.Fields['next_cursor' ].Value ;

    if varIsNull(db.RS.Fields['first_day'].Value) or
       varIsNull(db.RS.Fields['last_day' ].Value) or
       varIsNull(db.RS.Fields['max_price'].Value) or
       varIsNull(db.RS.Fields['min_price'].Value) or
       varIsNull(db.RS.Fields['vol'      ].Value) or
       varIsNull(db.RS.Fields['amount'   ].Value)
    then
    begin
      db.RS.Close ;
      continue ;
    end;

    first_day :=            db.RS.Fields['first_day'].Value ;
    last_day  :=            db.RS.Fields['last_day' ].Value ;
    StockDaily.max_price := db.RS.Fields['max_price'].Value ;
    StockDaily.min_price := db.RS.Fields['min_price'].Value ;
    StockDaily.vol       := db.RS.Fields['vol'      ].Value ;
    StockDaily.amount    := db.RS.Fields['amount'   ].Value ;
    StockDaily.shi_jian  := last_day ;


    sql := 'select * from                                     '+
           '(                                                 '+
           '  select price_today_open                         '+
           '  from tb_stock_data_Daily where                  '+
           '    code = ''' + pCode +                      '''' +
           '      and  ' +
           '    shi_jian = to_date('''+first_day+''',''yyyymmddhh24miss'') '+
           ')a,                                               '+
           '(                                                 '+
           '  select price                                    '+
           '  from tb_stock_data_Daily where                  '+
           '    code = ''' + pCode +                      '''' +
           '      and  ' +
           '    shi_jian = to_date('''+last_day+''',''yyyymmddhh24miss'') '+
           ')b';

    res := db.OpenSql(sql , resMsg);

    if varIsNull(db.RS.Fields['price_today_open'].Value) or
       varIsNull(db.RS.Fields['price' ].Value)
    then
    begin
      stmp := '';
    end;

    StockDaily.price_today_open := db.RS.Fields['price_today_open'].Value ;
    StockDaily.price            := db.RS.Fields['price'    ].Value ;
    db.RS.Close ;
    StockDaily.price_last_day := last_price ;
    last_price := StockDaily.price ;

    self.dailyTotal.AddObject(StockDaily.shi_jian + ',收盘价：'+floattostr( StockDaily.price)+',今开'+floattostr( StockDaily.price_today_open) + ',最高：'+floattostr( StockDaily.max_price )+ ',最低：' + floattostr( StockDaily.min_price) ,StockDaily);

    getMA  (dailyTotal.Count - 1);
    getKDJ (dailyTotal.Count - 1);
    getXSTD(dailyTotal.Count - 1);
  end;

  //db.RS.Close ;
  db.Disconnect(resMsg);
  db.Destroy ;
end;
}

procedure TstockDailyTotal.getWeek;
var
  max_Week   : string ;
  min_Week   : string ;
  cursor     : string ;
  last_price : double ;
  //sTmp       : string;
begin
  sql := 'select to_char(trunc(max(shi_jian),''d''),''yyyymmddhh24miss'') max_Week , to_char(trunc(min(shi_jian),''d''),''yyyymmddhh24miss'') min_Week from tb_stock_data_Daily where code ='''+
          pCode  + '''';

  db  := TXlsADO.Create ;
  res := db.Connect(connstr,resMsg);
  res := db.OpenSql(sql , resMsg);

  if  db.RS.EOF then
  begin
    db.RS.Close ;
    db.Disconnect(resMsg);
    db.Destroy ;
    exit ;
  end;

  self.dailyTotal.Clear ;

  max_Week  := db.RS.Fields['max_Week'].Value ;
  min_Week  := db.RS.Fields['min_Week'].Value ;

  db.RS.Close ;

  cursor := min_Week ;
  last_price := 0.0 ;
  while strtoint64(cursor) <= strtoint64(max_Week) do
  begin


    //if cursor = '1996' then
    //  stmp:= '';



    sql :='select * from'+
          '(             '+
          '   select '+
          '          to_char(to_date(''' + cursor + ''',''yyyymmddhh24miss'') + 7,''yyyymmddhh24miss'') next_cursor,'+
          '          to_char(max(shi_jian),''yyyymmddhh24miss'') last_day  ,'+
          '          sum(vol)                                    vol       ,'+
          '          sum(amount)                                 amount    ,'+
          '          max(max_price)                              max_price ,'+
          '          min(min_price)                              min_price  '+
          '   from tb_stock_data_Daily where                                '+
          '     code = ''' + pCode +                                     ''''+
          '       and  ' +
          '     trunc(shi_jian,''d'') = to_date(''' + cursor + ''',''yyyymmddhh24miss'')'+
          ')a, '+
          '(   '+
          '  select price_today_open from tb_stock_data_Daily where '+
          '    code = ''' + pCode + ''''+
          '      and '+
          '    shi_jian = (select min(shi_jian)  from tb_stock_data_Daily where '+
          '                  code = ''' + pCode + ''''+
          '                    and '+
          '                  trunc(shi_jian,''d'') = to_date(''' + cursor + ''',''yyyymmddhh24miss'')' +
          '                ) '+
          ')b,'+
          '(  '+
          '  select price from tb_stock_data_Daily where '+
          '    code = ''' + pCode + ''''+
          '      and '+
          '    shi_jian = ( '+
          '                  select max(shi_jian) from tb_stock_data_Daily where '+
          '                    code = ''' + pCode + ''''+
          '                      and '+
          '                    trunc(shi_jian,''d'') = to_date(''' + cursor + ''',''yyyymmddhh24miss'')' +
          '                ) '+
          ')c ';

    res := db.OpenSql(sql , resMsg);

    if  db.RS.EOF then
    begin
      db.RS.Close ;
      sql := 'select to_char(to_date(''' + cursor + ''',''yyyymmddhh24miss'') + 7,''yyyymmddhh24miss'')) next_cursor from dual' ;
      res := db.OpenSql(sql , resMsg);
      cursor := db.RS.Fields['next_cursor' ].Value ;
      db.RS.Close ;
      //db.Disconnect(resMsg);
      //db.Destroy ;
      continue ;
    end;

    StockDaily := TStockDaily.Create ;



    if varIsNull(db.RS.Fields['max_price'].Value) or
       varIsNull(db.RS.Fields['min_price'].Value) or
       varIsNull(db.RS.Fields['vol'      ].Value) or
       varIsNull(db.RS.Fields['amount'   ].Value)
    then
    begin
      db.RS.Close ;
      continue ;
    end;

    //赋值股票代码
    StockDaily.code := pCode ;
    cursor    := db.RS.Fields['next_cursor' ].Value ;

    StockDaily.max_price := db.RS.Fields['max_price'].Value ;
    StockDaily.min_price := db.RS.Fields['min_price'].Value ;
    StockDaily.vol       := db.RS.Fields['vol'      ].Value ;
    StockDaily.amount    := db.RS.Fields['amount'   ].Value ;
    StockDaily.shi_jian  := db.RS.Fields['last_day' ].Value ;
    StockDaily.price_today_open := db.RS.Fields['price_today_open'].Value ;
    StockDaily.price            := db.RS.Fields['price'    ].Value ;
    db.RS.Close ;

    StockDaily.price_last_day := last_price ;
    last_price := StockDaily.price ;

    self.dailyTotal.AddObject(StockDaily.shi_jian + ',收盘价：'+floattostr( StockDaily.price)+',今开'+floattostr( StockDaily.price_today_open) + ',最高：'+floattostr( StockDaily.max_price )+ ',最低：' + floattostr( StockDaily.min_price) ,StockDaily);
    getMA  (dailyTotal.Count -1);
    getKDJ (dailyTotal.Count );
    getXSTD(dailyTotal.Count -1);
  end;

  //db.RS.Close ;
  db.Disconnect(resMsg);
  db.Destroy ;
end;

function TstockDailyTotal.EMA( pValue, pLastValue , pN : double): double;
begin
  result :=(2*pValue+(pN-1)*pLastValue)/(pN+1) ;
end;

procedure TstockDailyTotal.getXSTD(dayCursor: Integer);
var
  dTmp : double ;
begin

  //[0]-SLONG , [1]-SSHORT , [2]-LLONG , [3]-LSHORT
  if self.dailyTotal.Count = 1 then
  begin
    //SLONG
    EmaVal1.Strings[0] := floattostr(EMA(TStockDaily( self.dailyTotal.Objects[dayCursor]).max_price , 0 , 1  )) ;
    EmaVal2.Strings[0] := floattostr(EMA(strtofloat( self.EmaVal1.Strings[0] ) , 0 , 1 ) ) ;

    //SSHORT
    EmaVal1.Strings[1] := floattostr(EMA(TStockDaily( self.dailyTotal.Objects[dayCursor]).min_price , 0 , 1  )) ;
    EmaVal2.Strings[1] := floattostr(EMA(strtofloat( self.EmaVal1.Strings[1] ) , 0 , 1 ) ) ;

    //LLONG
    EmaVal1.Strings[2] := floattostr(EMA(TStockDaily( self.dailyTotal.Objects[dayCursor]).max_price , 0 , 1  )) ;
    EmaVal2.Strings[2] := floattostr(EMA(strtofloat( self.EmaVal1.Strings[2] ) , 0 , 1 ) ) ;

    //LSHORT
    EmaVal1.Strings[3] := floattostr(EMA(TStockDaily( self.dailyTotal.Objects[dayCursor]).min_price , 0 , 1  )) ;
    EmaVal2.Strings[3] := floattostr(EMA(strtofloat( self.EmaVal1.Strings[3] ) , 0 , 1 ) ) ;
  end
  else
  begin
    //SLONG
    EmaVal1.Strings[0] := floattostr(EMA( TStockDaily( self.dailyTotal.Objects[dayCursor]).max_price , strtofloat(EmaVal1.Strings[0] ) , 5  ));
    EmaVal2.Strings[0] := floattostr(EMA( strtofloat(self.EmaVal1.Strings[0] ) , strtofloat(EmaVal2.Strings[0] ) , 10 )  );
    //SSHORT
    EmaVal1.Strings[1] := floattostr(EMA( TStockDaily( self.dailyTotal.Objects[dayCursor]).min_price , strtofloat(EmaVal1.Strings[1] ) , 5  ));
    EmaVal2.Strings[1] := floattostr(EMA( strtofloat(self.EmaVal1.Strings[1] ) , strtofloat(EmaVal2.Strings[1] ) , 10 )  );
    //LLONG
    EmaVal1.Strings[2] := floattostr(EMA( TStockDaily( self.dailyTotal.Objects[dayCursor]).max_price , strtofloat(EmaVal1.Strings[2] ) , 5  ));
    EmaVal2.Strings[2] := floattostr(EMA( strtofloat(self.EmaVal1.Strings[2] ) , strtofloat(EmaVal2.Strings[2] ) , 5 )  );
    //LSHORT
    EmaVal1.Strings[3] := floattostr(EMA( TStockDaily( self.dailyTotal.Objects[dayCursor]).min_price , strtofloat(EmaVal1.Strings[3] ) , 5  ));
    EmaVal2.Strings[3] := floattostr(EMA( strtofloat(self.EmaVal1.Strings[3] ) , strtofloat(EmaVal2.Strings[3] ) , 5 )  );
  end;

  //dTmp := strtofloat( EmaVal2.Strings[0])*1.12  ;
  //dTmp := strtofloat( EmaVal2.Strings[1])*0.86  ;
  //dTmp := strtofloat( EmaVal2.Strings[2])*1.04  ;
  //dTmp := strtofloat( EmaVal2.Strings[3])*0.94  ;

  TStockDaily( self.dailyTotal.Objects[self.dailyTotal.Count - 1]).XSTDValues.Add( floattostr( strtofloat( EmaVal2.Strings[0]) *  1.12 ));
  TStockDaily( self.dailyTotal.Objects[self.dailyTotal.Count - 1]).XSTDValues.Add( floattostr( strtofloat( EmaVal2.Strings[1]) *  0.86 ));
  TStockDaily( self.dailyTotal.Objects[self.dailyTotal.Count - 1]).XSTDValues.Add( floattostr( strtofloat( EmaVal2.Strings[2]) *  1.04 ));
  TStockDaily( self.dailyTotal.Objects[self.dailyTotal.Count - 1]).XSTDValues.Add( floattostr( strtofloat( EmaVal2.Strings[3]) *  0.94 ));
end;

procedure TstockDailyTotal.getYear(pCode : string );
var
  years : integer ;
  minYear : integer ;
  iloopTime : integer ;
  cursorYear : integer ;
  last_price : double ;
  sTmp : string;
begin

  sql := 'select to_char(max(shi_jian),''yyyy'') - to_char(min(shi_jian),''yyyy'') years , to_char(min(shi_jian),''yyyy'') minyear from  tb_stock_data_Daily where code ='''+
          pCode  + '''';

  db := TXlsADO.Create ;
  res := db.Connect(connstr,resMsg);
  res := db.OpenSql(sql , resMsg);

  if  db.RS.EOF then
  begin
    db.RS.Close ;
    db.Disconnect(resMsg);
    db.Destroy ;
    exit ;
  end;

  self.dailyTotal.Clear ;

  years := db.RS.Fields['years'].Value ;
  minYear := db.RS.Fields['minyear'].Value ;
  //cursorYear := minYear ;

  db.RS.Close ;

  last_price := 0.0 ;

  for iLoopTime := 0 to years  do
  begin
    StockDaily := TStockDaily.Create ;
    cursorYear := minYear + iLoopTime ;

    if cursorYear = 1996 then
      stmp:= '';

    //赋值股票代码
    StockDaily.code := pCode ;

    //获得开盘价,昨收价,股票名
    sql := 'select price_today_open ,decode(price_last_day,null,0,price_last_day) price_last_day,name ' +
           'from tb_stock_data_Daily where ' +
           '  code ='''+ pCode  + '''      ' +
           '    and                        ' +
           '  shi_jian = (                 ' +
           '               select min(shi_jian) from tb_stock_data_Daily where '+
           '                 code ='''+ pCode  + '''' +
           '                   and ' +
           '                 to_char(shi_jian,''yyyy'') = '+ inttostr( cursorYear ) +
           '                   and ' +
           '                 price > 0 '+
           '              ) ';
    res := db.OpenSql(sql , resMsg);

    if db.RS.EOF then
    begin
      StockDaily.Destroy ;
      continue;
    end;


    StockDaily.price_today_open :=  db.RS.Fields['price_today_open'].Value ;

    StockDaily.price_last_day := db.RS.Fields['price_last_day'].Value ;
    StockDaily.name := db.RS.Fields['name'].Value ;
    db.RS.Close;


    //获得收盘价
    sql := 'select price                   ' +
           'from tb_stock_data_Daily where ' +
           '  code ='''+ pCode  + '''      ' +
           '    and                        ' +
           '  shi_jian = (                 ' +
           '               select max(shi_jian) from tb_stock_data_Daily where '+
           '                 code ='''+ pCode  + '''' +
           '                   and ' +
           '                 to_char(shi_jian,''yyyy'') = '+ inttostr( cursorYear ) +
           '                   and ' +
           '                 price > 0 '+
           '              ) ';
    res := db.OpenSql(sql , resMsg);
    StockDaily.price :=  db.RS.Fields['price'].Value ;
    db.RS.Close;

    //获得最高,最低价,收盘时间
    sql := 'select max(max_price) max_price,min(min_price) min_price,to_char(max(shi_jian) ,''yyyymmddhh24miss'') shi_jian ,' +
           '  sum(vol) vol , sum(amount) amount '+
           'from tb_stock_data_Daily where ' +
           '  code ='''+ pCode  + '''      ' +
           '    and ' +
           '  price > 0 '+
           '    and                        ' +
           '  to_char( shi_jian , ''yyyy'' ) = ' + inttostr(cursorYear) ;
    res := db.OpenSql(sql , resMsg);
    StockDaily.max_price :=  db.RS.Fields['max_price'].Value ;
    StockDaily.min_price :=  db.RS.Fields['min_price'].Value ;
    StockDaily.shi_jian  :=  db.RS.Fields['shi_jian' ].Value ;
    StockDaily.vol       :=  db.RS.Fields['vol'      ].Value ;
    StockDaily.amount    :=  db.RS.Fields['amount'   ].Value ;
    db.RS.Close;

    StockDaily.price_last_day :=  last_price ;
    last_price := StockDaily.price ;

    dailyTotal.AddObject(StockDaily.shi_jian + ',收盘价：'+floattostr( StockDaily.price)+',今开'+floattostr( StockDaily.price_today_open) + ',最高：'+floattostr( StockDaily.max_price )+ ',最低：' + floattostr( StockDaily.min_price),StockDaily );

    getMA  (dailyTotal.Count - 1);
    getKDJ (dailyTotal.Count - 1);
    getXSTD(dailyTotal.Count - 1);
  end;

  //db.RS.Close ;
  db.Disconnect(resMsg) ;
  db.Destroy ;

end;

end.

