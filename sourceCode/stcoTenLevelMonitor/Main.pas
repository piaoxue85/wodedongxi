unit Main;

interface

uses
  TenLevel,
  IdHTTP ,
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants, System.Classes, Vcl.Graphics,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, Vcl.StdCtrls, Vcl.Menus, Vcl.ExtCtrls;

type
  TForm3 = class(TForm)
    MainMenu1: TMainMenu;
    N1: TMenuItem;
    N2: TMenuItem;
    Memo1: TMemo;
    Timer1: TTimer;
    procedure Timer1Timer(Sender: TObject);
    procedure N1Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Form3: TForm3;

implementation

{$R *.dfm}

procedure TForm3.N1Click(Sender: TObject);
begin
  //
  self.Timer1.Enabled := true ; ;
end;

procedure TForm3.Timer1Timer(Sender: TObject);
var
  http : TIdHTTP ;
  res : string ;
  ten : TRootClass ;
begin
  //
  http := TIdHTTP.Create(nil);
  //http.Request.CustomHeaders.Add('apikey:'+ baiduappkey);
  res := http.Get('https://app.leverfun.com/timelyInfo/timelyOrderForm?stockCode=600959');
  http.Destroy ;

  ten := TRootClass.FromJsonString(res) ;

  if not ten.success then
    exit ;

  memo1.Clear ;
  memo1.Lines.Add('��������');

  memo1.Lines.Add(floattostr(ten.code));
  memo1.Lines.Add(ten.message) ;

  memo1.Lines.Add(floattostr(TsellPankouClass(ten.data.sellPankou[9]).price) + '    ' + floattostr(TsellPankouClass(ten.data.sellPankou[9]).volume)) ;
  memo1.Lines.Add(floattostr(TsellPankouClass(ten.data.sellPankou[8]).price) + '    ' + floattostr(TsellPankouClass(ten.data.sellPankou[8]).volume)) ;
  memo1.Lines.Add(floattostr(TsellPankouClass(ten.data.sellPankou[7]).price) + '    ' + floattostr(TsellPankouClass(ten.data.sellPankou[7]).volume)) ;
  memo1.Lines.Add(floattostr(TsellPankouClass(ten.data.sellPankou[6]).price) + '    ' + floattostr(TsellPankouClass(ten.data.sellPankou[6]).volume)) ;
  memo1.Lines.Add(floattostr(TsellPankouClass(ten.data.sellPankou[5]).price) + '    ' + floattostr(TsellPankouClass(ten.data.sellPankou[5]).volume)) ;
  memo1.Lines.Add(floattostr(TsellPankouClass(ten.data.sellPankou[4]).price) + '    ' + floattostr(TsellPankouClass(ten.data.sellPankou[4]).volume)) ;
  memo1.Lines.Add(floattostr(TsellPankouClass(ten.data.sellPankou[3]).price) + '    ' + floattostr(TsellPankouClass(ten.data.sellPankou[3]).volume)) ;
  memo1.Lines.Add(floattostr(TsellPankouClass(ten.data.sellPankou[2]).price) + '    ' + floattostr(TsellPankouClass(ten.data.sellPankou[2]).volume)) ;
  memo1.Lines.Add(floattostr(TsellPankouClass(ten.data.sellPankou[1]).price) + '    ' + floattostr(TsellPankouClass(ten.data.sellPankou[1]).volume)) ;
  memo1.Lines.Add(floattostr(TsellPankouClass(ten.data.sellPankou[0]).price) + '    ' + floattostr(TsellPankouClass(ten.data.sellPankou[0]).volume)) ;

  memo1.Lines.Add(floattostr(ten.data.match ));

  memo1.Lines.Add(floattostr(TBuyPankouClass(ten.data.buyPankou[0]).price) + '    ' + floattostr(TBuyPankouClass(ten.data.buyPankou[0]).volume)) ;
  memo1.Lines.Add(floattostr(TBuyPankouClass(ten.data.buyPankou[1]).price) + '    ' + floattostr(TBuyPankouClass(ten.data.buyPankou[1]).volume)) ;
  memo1.Lines.Add(floattostr(TBuyPankouClass(ten.data.buyPankou[2]).price) + '    ' + floattostr(TBuyPankouClass(ten.data.buyPankou[2]).volume)) ;
  memo1.Lines.Add(floattostr(TBuyPankouClass(ten.data.buyPankou[3]).price) + '    ' + floattostr(TBuyPankouClass(ten.data.buyPankou[3]).volume)) ;
  memo1.Lines.Add(floattostr(TBuyPankouClass(ten.data.buyPankou[4]).price) + '    ' + floattostr(TBuyPankouClass(ten.data.buyPankou[4]).volume)) ;
  memo1.Lines.Add(floattostr(TBuyPankouClass(ten.data.buyPankou[5]).price) + '    ' + floattostr(TBuyPankouClass(ten.data.buyPankou[5]).volume)) ;
  memo1.Lines.Add(floattostr(TBuyPankouClass(ten.data.buyPankou[6]).price) + '    ' + floattostr(TBuyPankouClass(ten.data.buyPankou[6]).volume)) ;
  memo1.Lines.Add(floattostr(TBuyPankouClass(ten.data.buyPankou[7]).price) + '    ' + floattostr(TBuyPankouClass(ten.data.buyPankou[7]).volume)) ;
  memo1.Lines.Add(floattostr(TBuyPankouClass(ten.data.buyPankou[8]).price) + '    ' + floattostr(TBuyPankouClass(ten.data.buyPankou[8]).volume)) ;
  memo1.Lines.Add(floattostr(TBuyPankouClass(ten.data.buyPankou[9]).price) + '    ' + floattostr(TBuyPankouClass(ten.data.buyPankou[9]).volume)) ;




end;

end.
