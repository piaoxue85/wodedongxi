unit recommend;

interface

uses
  stockDaily,
  stockDailyTotal ,
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants, System.Classes, Vcl.Graphics,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, Vcl.StdCtrls, Vcl.Menus;

type
  Tmain = class(TForm)
    MainMenu1: TMainMenu;
    N1: TMenuItem;
    Memo1: TMemo;
    procedure FormCreate(Sender: TObject);
    procedure N1Click(Sender: TObject);
  private
    { Private declarations }
    top : TStringList;
    bottom : TStringList ;
    MASetting : TStringList ;
    KDJSetting : TStringList ;
  public
    { Public declarations }
  end;

var
  main: Tmain;

implementation

{$R *.dfm}

procedure Tmain.FormCreate(Sender: TObject);
begin
  self.Memo1.Clear;
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
end;

procedure Tmain.N1Click(Sender: TObject);
var
  stock : TstockDailyTotal ;
begin
  stock := TstockDailyTotal.Create();

end;

end.
