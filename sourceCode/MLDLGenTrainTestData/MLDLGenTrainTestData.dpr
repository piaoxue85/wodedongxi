program MLDLGenTrainTestData;

uses
  Vcl.Forms,
  main in 'main.pas' {fMain},
  ThreadGen in 'ThreadGen.pas',
  ADO in '..\..\..\..\MyFunc\DelphiFunc\ADO.pas',
  adodb_tlb in '..\..\..\..\MyFunc\DelphiFunc\adodb_tlb.pas',
  Unit_DateTimeFuncs in '..\..\..\..\MyFunc\DelphiFunc\Unit_DateTimeFuncs.pas',
  Unit_FileFuncs in '..\..\..\..\MyFunc\DelphiFunc\Unit_FileFuncs.pas',
  Unit_MathFuncs in '..\..\..\..\MyFunc\DelphiFunc\Unit_MathFuncs.pas',
  Unit_StrFuncs in '..\..\..\..\MyFunc\DelphiFunc\Unit_StrFuncs.pas',
  Hashtable in '..\..\..\..\MyFunc\DelphiFunc\Hashtable.pas',
  Point in 'Point.pas';

{$R *.res}

begin
  Application.Initialize;
  Application.MainFormOnTaskbar := True;
  Application.CreateForm(TfMain, fMain);
  Application.Run;
end.
