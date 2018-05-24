unit stockRecommend;

interface
uses
  stockDailyTotal ,
  Unit_MathFuncs ,
  stockDaily ,
  ado,
  Controls ,
  System.SysUtils, System.Variants, System.Classes ;

type
  TstockRecommend = class(TObject)
  private
    sql : string;
    res : integer ;
    resMsg : string ;
    db : TXlsADO ;

    total      : TStockDailyTotal ;
    codeList   : TStringList ;
    MASetting  : TStringList ;
    KDJSetting : TStringList ;



  public
    connstr: string  ;

    constructor Create(pMaSetting : TStringList ; pKDJSetting : TStringList);
    Destructor  Destroy ;

    function analyseDay      : TStringList;
    function analyseWeek     : TStringList;
    function analyseMonth    : TStringList;
    function analyseQuarter  : TStringList;
    function analyseHalfYear : TStringList;
    function analyseYear     : TStringList;

  end;

implementation


{ TstockRecommend }

function TstockRecommend.analyseDay: TStringList;
var
  res : Tstringlist;
  loopcodelist :integer ;
  loopday : integer ;
begin
  res := tstringlist.Create ;

  for loopcodelist:= 0 to codeList.Count -1 do
  begin
    total.getDay(codelist.Strings[loopcodelist]);
    //TStockDaily( total.dailyTotal.Objects[total.dailyTotal-1] ).KDJ_K

  end;



  result := res ;
end;

function TstockRecommend.analyseHalfYear: TStringList;
var
  res : Tstringlist;
  loopcodelist :integer ;
  loopday : integer ;
begin
  res := tstringlist.Create ;

  for loopcodelist:= 0 to codeList.Count -1 do
  begin
    total.getDay(codelist.Strings[loopcodelist]);
    //TStockDaily( total.dailyTotal.Objects[total.dailyTotal-1] ).KDJ_K

  end;

  result := res ;
end;

function TstockRecommend.analyseMonth: TStringList;
var
  res : Tstringlist;
  loopcodelist :integer ;
  loopday : integer ;
begin
  res := tstringlist.Create ;

  for loopcodelist:= 0 to codeList.Count -1 do
  begin
    total.getDay(codelist.Strings[loopcodelist]);
    //TStockDaily( total.dailyTotal.Objects[total.dailyTotal-1] ).KDJ_K

  end;

  result := res ;
end;

function TstockRecommend.analyseQuarter: TStringList;
var
  res : Tstringlist;
  loopcodelist :integer ;
  loopday : integer ;
begin
  res := tstringlist.Create ;

  for loopcodelist:= 0 to codeList.Count -1 do
  begin
    total.getDay(codelist.Strings[loopcodelist]);
    //TStockDaily( total.dailyTotal.Objects[total.dailyTotal-1] ).KDJ_K

  end;



  result := res ;
end;

function TstockRecommend.analyseWeek: TStringList;
var
  res : Tstringlist;
  loopcodelist :integer ;
  loopday : integer ;
  today :TStockDaily ;
begin
  res := tstringlist.Create ;

  for loopcodelist:= 0 to codeList.Count -1 do
  begin
    //total.getWeek(codelist.Strings[loopcodelist]);
    total.getWeek('sh000001');
    if total.dailyTotal.Count >0 then
      today := TStockDaily( total.dailyTotal.Objects[total.dailyTotal.Count-1] )
    else
      loopday := 0 ;

      {
    //[0]-K VALUE , [1]-D VALUE , [2]-J VALUE
    if today.KDJValues.Count<1 then
      continue ;

    if (
       (strtofloat(today.KDJValues.Strings[0]) <10.0 ) and
       (strtofloat(today.KDJValues.Strings[1]) <10.0 ) and
       (strtofloat(today.KDJValues.Strings[2]) > strtofloat(today.KDJValues.Strings[0])) and
       (strtofloat(today.KDJValues.Strings[0]) > strtofloat(today.KDJValues.Strings[1]))
       )
    then
    begin
      res.Add(today.code + ',' + today.name );
    end;
    }
    res.Add(datetimetostr(now) + ':'+today.code + 'price=' + floattostr( today.price) + ',price_last_day=' + floattostr(today.price_last_day)+ 'shijian=' +today.shi_jian);
    res.Add(datetimetostr(now) + ':'+today.code + ',k=' + today.KDJValues.Strings[0] + ',d=' +today.KDJValues.Strings[1] + ',j=' +today.KDJValues.Strings[2]);


  end;

  result := res ;
end;

function TstockRecommend.analyseYear: TStringList;
var
  res : Tstringlist;
  loopcodelist :integer ;
  loopday : integer ;
  today :TStockDaily ;
begin
  res := tstringlist.Create ;

  for loopcodelist:= 0 to codeList.Count -1 do
  begin
    total.getYear(codelist.Strings[loopcodelist]);
    if total.dailyTotal.Count >0 then
      today := TStockDaily( total.dailyTotal.Objects[total.dailyTotal.Count-1] )
    else
      loopday := 0 ;

      {
    //[0]-K VALUE , [1]-D VALUE , [2]-J VALUE
    if today.KDJValues.Count<1 then
      continue ;

    if (
       (strtofloat(today.KDJValues.Strings[0]) <10.0 ) and
       (strtofloat(today.KDJValues.Strings[1]) <10.0 ) and
       (strtofloat(today.KDJValues.Strings[2]) > strtofloat(today.KDJValues.Strings[0])) and
       (strtofloat(today.KDJValues.Strings[0]) > strtofloat(today.KDJValues.Strings[1]))
       )
    then
    begin
      res.Add(today.code + ',' + today.name );
    end;
    }
    res.Add(datetimetostr(now) + ':'+today.code + 'price=' + floattostr( today.price) + ',price_last_day=' + floattostr(today.price_last_day)+ 'shijian=' +today.shi_jian);
    res.Add(datetimetostr(now) + ':'+today.code + ',k=' + today.KDJValues.Strings[0] + ',d=' +today.KDJValues.Strings[1] + ',j=' +today.KDJValues.Strings[2]);


  end;

  result := res ;
end;

constructor TstockRecommend.Create( pMaSetting,  pKDJSetting: TStringList);
begin
  inherited create ;

  MASetting := TStringList.Create ;
  MASetting.Clear ;
  MASetting.Add('6');
  MASetting.Add('12');
  MASetting.Add('20');
  MASetting.Add('30');
  MASetting.Add('45');
  MASetting.Add('60');
  MASetting.Add('125');
  MASetting.Add('250');

  KDJSetting := TStringList.Create ;
  KDJSetting.Clear ;
  KDJSetting.Add('9');   //kdj天参数
  KDJSetting.Add('2');   //k
  KDJSetting.Add('3');   //d
  KDJSetting.Add('2');   //j形态参数

  total := TStockDailyTotal.Create(MASetting , KDJSetting) ;
  codeList := total.getCodeList ;
end;

destructor TstockRecommend.Destroy;
begin
  total.Destroy ;
  codelist.Destroy ;

  inherited Destroy;
end;



end.
