program recommendStock;

uses
  Vcl.Forms,
  recommend in 'recommend.pas' {main},
  stockDaily in '..\stock\stockDaily.pas',
  stockDailyTotal in '..\stock\stockDailyTotal.pas',
  ADO in '..\..\..\..\MyFunc\DelphiFunc\ADO.pas',
  ADO_Controller in '..\..\..\..\MyFunc\DelphiFunc\ADO_Controller.pas',
  ADO_Shell in '..\..\..\..\MyFunc\DelphiFunc\ADO_Shell.pas',
  adodb_tlb in '..\..\..\..\MyFunc\DelphiFunc\adodb_tlb.pas',
  CnMD5 in '..\..\..\..\MyFunc\DelphiFunc\CnMD5.pas',
  ComPersist in '..\..\..\..\MyFunc\DelphiFunc\ComPersist.pas',
  Dailog in '..\..\..\..\MyFunc\DelphiFunc\Dailog.pas',
  Global_Setting in '..\..\..\..\MyFunc\DelphiFunc\Global_Setting.pas',
  Hashtable in '..\..\..\..\MyFunc\DelphiFunc\Hashtable.pas',
  MD5 in '..\..\..\..\MyFunc\DelphiFunc\MD5.pas',
  Unit_FileFuncs in '..\..\..\..\MyFunc\DelphiFunc\Unit_FileFuncs.pas',
  Unit_MathFuncs in '..\..\..\..\MyFunc\DelphiFunc\Unit_MathFuncs.pas',
  Unit_StrFuncs in '..\..\..\..\MyFunc\DelphiFunc\Unit_StrFuncs.pas';

{$R *.res}

begin
  Application.Initialize;
  Application.MainFormOnTaskbar := True;
  Application.CreateForm(Tmain, main);
  Application.Run;
end.
