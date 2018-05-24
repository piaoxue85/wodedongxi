program stock;

uses
  Vcl.Forms,
  main in 'main.pas' {Form1},
  stockDaily in 'stockDaily.pas',
  stockDailyTotal in 'stockDailyTotal.pas',
  stockImportNameAndCode in 'stockImportNameAndCode.pas',
  stockImportDaily in 'stockImportDaily.pas',
  ADO in '..\..\..\..\MyFunc\DelphiFunc\ADO.pas',
  adodb_tlb in '..\..\..\..\MyFunc\DelphiFunc\adodb_tlb.pas',
  Unit_FileFuncs in '..\..\..\..\MyFunc\DelphiFunc\Unit_FileFuncs.pas',
  Unit_StrFuncs in '..\..\..\..\MyFunc\DelphiFunc\Unit_StrFuncs.pas',
  Hashtable in '..\..\..\..\MyFunc\DelphiFunc\Hashtable.pas',
  Unit_MathFuncs in '..\..\..\..\MyFunc\DelphiFunc\Unit_MathFuncs.pas',
  stockRecommend in 'stockRecommend.pas' {/TestCases in 'TestCases.pas',},
  MarkovChains in 'MarkovChains.pas';

//TestCases in 'TestCases.pas',
  //TestFrameWork,
  //GUITestRunner;

{$R *.res}

begin
  Application.Initialize;
  Application.MainFormOnTaskbar := True;
  Application.CreateForm(TForm1, Form1);
  //GUITestRunner.RunRegisteredTests;
  Application.Run;
end.
