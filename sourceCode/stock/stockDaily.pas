unit stockDaily;

interface
uses
  Controls ,
  System.SysUtils, System.Variants, System.Classes ;

type
  TstockDaily = class(TObject)
    name                :string ;
    code                :string ;
    price               :double ;
    price_last_day      :double ;
    price_today_open    :double ;
    max_price           :double ;
    min_price           :double ;
    shi_jian            :string ;
    vol                 :double ;
    amount              :double ;
    MA6           : double ;
    MA12          : double ;
    MA20          : double ;
    MA30          : double ;
    MA45          : double ;
    MA60          : double ;
    MA125         : double ;
    MA250         : double ;
    KDJ_K         : double ;
    KDJ_D         : double ;
    KDJ_J         : double ;
    xstd_SLONG    : double ;
    xstd_SSHORT   : double ;
    xstd_LLONG    : double ;
    xstd_LSHORT   : double ;
    BOLL_uBOLL    : double ;
    BOLL_dBOLL    : double ;
    BOLL_BOLL     : double ;
    MACD_DIF      : double ;
    MACD_MACD     : double ;
    MACD_DIF_MACD : double ;

    MAValues            :TStringList;
    KDJValues           :TStringList;       //[0]-K VALUE , [1]-D VALUE , [2]-J VALUE
    XSTDValues          :TStringList ;      //[0]-SLONG , [1]-SSHORT , [2]-LLONG , [3]-LSHORT
  private

  public
    constructor Create;
    Destructor  Destroy ;
  end;

implementation

{ TstockDaily }

constructor TstockDaily.Create;
begin
  inherited Create;
  MAValues := TStringList.Create ;
  KDJValues := TStringList.Create ;
  XSTDValues := TStringList.Create ;

  MAValues.Clear ;
  KDJValues.Clear ;
  XSTDValues.Clear ;
end;

destructor TstockDaily.Destroy;
begin
  inherited Destroy ;
end;

end.
