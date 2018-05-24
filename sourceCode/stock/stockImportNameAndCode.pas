unit stockImportNameAndCode;

interface
uses
  Unit_StrFuncs ,
  comobj,
  ado ,
  Controls ,
  System.SysUtils, System.Variants, System.Classes ;

type
  TstockImportNameAndCode = class(TObject)
  private
    db : TXLsAdo ;
    //xls : Variant ;
    res : integer ;
    resmsg : string ;

  public
    connstr :string ;
    function import( pFilename : string ; var pResMsg:string ) : integer ;
    constructor Create;
    Destructor  Destroy ;
  end;

implementation

{ TstockDaily }

constructor TstockImportNameAndCode.Create;
begin
  inherited Create;
  db := TXLSAdo.Create ;
  db.bWriteErrLog := true ;
  //db.bWriteActLog := true ;
  //xls := createoleobject('Excel.Application');
  //connstr :='Provider=OraOLEDB.Oracle.1;Password=didierg160;Persist Security Info=True;User ID=c##stock;Data Source=myoracle';
end;

destructor TstockImportNameAndCode.Destroy;
begin
  db.Destroy ;
  //xls.Quit ;
  //xls := unassigned ;
  inherited Destroy ;
end;

function TstockImportNameAndCode.import(pFilename : string ; var pResMsg:string): integer;
var
  sql  : string ;
  name : string ;
  code : string ;
  pe   : string ;
  pb   : string ;
  LIQUID_ASSETS : string ;
  TOTAL_ASSETS  : string ;
  price :string ;
  row  : integer ;
  count: integer ;
  re : integer ;
  data : TStringList ;
  sltmp : tstringlist ;
begin
  data:= TStringList.Create ;
  data.Clear ;
  data.LoadFromFile(pfileName);

  sltmp:= TStringList.Create ;
  sltmp.Clear ;

  res := db.Connect(connstr , resmsg);

  sql := 'truncate table tb_stock_list ';
  res := db.ExecuteSql(sql , false , re , resmsg ) ;

  for  row:= 2 to data.Count -1 do
  begin
    if  trim(data.Strings[row]) = '' then
      continue ;

    slTmp.Clear ;
    SplitStr(slTmp , data.Strings[row] , '	');
    name := trim( slTmp.Strings[1]);
    code := trim( slTmp.Strings[2]);
    price:=  trim( slTmp.Strings[4]);
    pe   := trim( slTmp.Strings[14]);
    pb   := trim( slTmp.Strings[15]);
    LIQUID_ASSETS := trim( slTmp.Strings[19]);
    TOTAL_ASSETS  := trim( slTmp.Strings[20]);

    if pe = '亏损' then
      pe := ''',-1000000'
    else
    begin
      if pe = '----' then
        pe := ''',null'
      else
        pe := ''','+ pe ;
    end;

    if pb = '----' then
      pb := ',null'
    else
      pb := ','+ pb ;

//    if price = '----' then
//      price := ',null'
//    else
//      price := ','+ price ;

    price := ',null' ;

    if LIQUID_ASSETS ='----' then
      LIQUID_ASSETS := ',null'
    else
    begin
      if pos('亿',LIQUID_ASSETS) >0 then
        LIQUID_ASSETS := floattostr(strtofloat(LIQUID_ASSETS.Replace('亿','')) )
      else if pos('万',LIQUID_ASSETS) > 0 then
        LIQUID_ASSETS :=floattostr( strtofloat(LIQUID_ASSETS.Replace('万','')) * 0.0001 ) ;

      LIQUID_ASSETS := ','+ LIQUID_ASSETS ;
    end;

    if TOTAL_ASSETS = '----' then
      TOTAL_ASSETS := ',null'
    else
    begin
      if pos('亿',TOTAL_ASSETS) >0 then
        TOTAL_ASSETS := floattostr(strtofloat(TOTAL_ASSETS.Replace('亿',''))  )
      else if pos('万',TOTAL_ASSETS) > 0 then
        TOTAL_ASSETS := floattostr( strtofloat(TOTAL_ASSETS.Replace('万','')) * 0.0001 ) ;

      TOTAL_ASSETS := ','+ TOTAL_ASSETS ;
    end;

    //if name = '日照港' then
    //   name := '';

    sql := 'insert into tb_stock_list values ('''+ code +''','''+ name + pe + pb +LIQUID_ASSETS+TOTAL_ASSETS+price+',sysdate)';
    res := db.ExecuteSql(sql , false , re , resmsg ) ;
  end;

  data.Destroy ;
  sltmp.Destroy ;
  deletefile(PChar(pfileName)) ;

  pResMsg := '操作成功';
  result := 0;
end;


{
function TstockImportNameAndCode.import(pFilename : string ; var pResMsg:string): integer;
var
  sql  : string ;
  name : string ;
  code : string ;
  row  : integer ;
  count: integer ;
  re : integer ;
begin
  //xls.workbooks.open('D:\Projects\j金融\g股票数据分析系统\sourceCode\stock\Win32\Debug\报价--沪深Ａ股.xls');
  xls.workbooks.open(pFilename);

  res := db.Connect(connstr , resmsg);
  row := 2 ;

  sql := 'truncate table tb_stock_list ';
  res := db.ExecuteSql(sql , false , re , resmsg ) ;
  
  while not varisnull( xls.workbooks[1].sheets[1].cells[row,2].value ) and
        not varisnull( xls.workbooks[1].sheets[1].cells[row,3].value )  
  do 
  begin
    name := trim(xls.workbooks[1].sheets[1].cells[row,2].value );
    code := trim(xls.workbooks[1].sheets[1].cells[row,3].value ) ;

    if (code = '') or (name = '')  then
      break ;

    sql := 'insert into tb_stock_list values ('''+ code +''','''+ name +''')';
    res := db.ExecuteSql(sql , false , re , resmsg ) ;

    inc(row);
  end;

  xls.workbooks.close ;
  deletefile(PChar(pfileName)) ;
  //pResMsg := '操作成功';
  result := 0;
end;
}

end.
