unit TestCases;

interface

uses

 TestFrameWork;



type

 TTestCaseFirst = class(TTestCase)

 published

   procedure TestFirst;

 end;



implementation



procedure TTestCaseFirst.TestFirst;

begin

 Check(1 + 1 = 2, 'Catastrophic arithmetic failure!');

end;



initialization

 TestFramework.RegisterTest(TTestCaseFirst.Suite);

end.

