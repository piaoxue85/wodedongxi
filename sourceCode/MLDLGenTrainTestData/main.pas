unit main;

interface

uses
  ThreadGen ,
  Winapi.Windows, Winapi.Messages, System.SysUtils, System.Variants, System.Classes, Vcl.Graphics,
  Vcl.Controls, Vcl.Forms, Vcl.Dialogs, Vcl.StdCtrls, Vcl.Menus, Vcl.ExtCtrls;

type
  TfMain = class(TForm)
    MainMenu1: TMainMenu;
    N1: TMenuItem;
    genCSV: TMenuItem;
    Memo1: TMemo;
    Timer1: TTimer;
    genPoint: TMenuItem;
    procedure genCSVClick(Sender: TObject);
    procedure Timer1Timer(Sender: TObject);
    procedure genPointClick(Sender: TObject);
    procedure FormCreate(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  fMain: TfMain;

implementation

{$R *.dfm}

procedure TfMain.FormCreate(Sender: TObject);
begin
  self.Memo1.Clear ;
end;

procedure TfMain.genCSVClick(Sender: TObject);
var
  thGen : TThreadGen ;
begin
  thGen := TThreadGen.Create ;
  self.genCSV.Enabled := false ;
end;

procedure TfMain.genPointClick(Sender: TObject);
var
  thGen : TThreadGen ;
begin
  thGen := TThreadGen.Create ;
  self.genPoint.Enabled := false ;
end;

procedure TfMain.Timer1Timer(Sender: TObject);
begin
  if self.Memo1.Lines.Count>=5000 then
     self.Memo1.Clear ;
end;

end.
