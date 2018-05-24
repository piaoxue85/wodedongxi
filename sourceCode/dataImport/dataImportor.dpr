program dataImportor;

uses
  Vcl.Forms,
  Main in 'Main.pas' {MainForm},
  stockDaily in '..\stock\stockDaily.pas',
  stockDailyTotal in '..\stock\stockDailyTotal.pas',
  stockImportDaily in '..\stock\stockImportDaily.pas',
  stockImportNameAndCode in '..\stock\stockImportNameAndCode.pas',
  ThreadImportQianLongXLS in 'ThreadImportQianLongXLS.pas',
  ADO in '..\..\..\..\MyFunc\DelphiFunc\ADO.pas',
  adodb_tlb in '..\..\..\..\MyFunc\DelphiFunc\adodb_tlb.pas',
  Unit_FileFuncs in '..\..\..\..\MyFunc\DelphiFunc\Unit_FileFuncs.pas',
  Unit_StrFuncs in '..\..\..\..\MyFunc\DelphiFunc\Unit_StrFuncs.pas',
  Hashtable in '..\..\..\..\MyFunc\DelphiFunc\Hashtable.pas',
  Unit_MathFuncs in '..\..\..\..\MyFunc\DelphiFunc\Unit_MathFuncs.pas',
  ThreadImportDaily in 'ThreadImportDaily.pas';

{$R *.res}

begin
  Application.Initialize;
  Application.MainFormOnTaskbar := True;
  Application.CreateForm(TMainForm, MainForm);
  Application.Run;
end.
