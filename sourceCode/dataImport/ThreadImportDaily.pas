unit ThreadImportDaily;

interface

uses
  System.SysUtils,
  Unit_FileFuncs ,
  stockImportDaily,
  System.Classes;

type
  TThreadImportDaily = class(TThread)
  private
    { Private declarations }
    import : TstockImportDaily ;

    List : TStringList;
    sline : string ;
    procedure incCounter;
    procedure addMemo ;
  protected
    procedure Execute; override;
  public
    constructor Create(pFileList : TStringlist);
  end;

implementation
uses
  main;

{
  Important: Methods and properties of objects in visual components can only be
  used in a method called using Synchronize, for example,

      Synchronize(UpdateCaption);

  and UpdateCaption could look like,

    procedure TThreadImportQianLongXLS.UpdateCaption;
    begin
      Form1.Caption := 'Updated in a thread';
    end;

    or

    Synchronize(
      procedure
      begin
        Form1.Caption := 'Updated in thread via an anonymous method'
      end
      )
    );

  where an anonymous method is passed.

  Similarly, the developer can call the Queue method with similar parameters as
  above, instead passing another TThread class as the first parameter, putting
  the calling thread in a queue with the other thread.

}

{ TThreadImportQianLongXLS }

procedure TThreadImportDaily.addMemo;
begin
  //mainform.Memo1.Lines.Add(datetimetostr(now) +'出错:' + resmsg );
  mainform.Memo1.Lines.Add(sline );
end;

constructor TThreadImportDaily.Create(pFileList: TStringlist);
begin
  inherited Create;
  List := pFileList ;
end;

procedure TThreadImportDaily.Execute;
var
  iLoopTime : integer ;
  res : integer ;
  resMsg : string ;
  Err : Exception;
begin
  { Place thread code here }
  import := TstockImportDaily.Create  ;
  import.connstr := mainform.connstr ;
  try
    try
      {
        fileList.Clear ;
        fileList := MakeFileList('D:\Projects\j金融\g股票数据分析系统\sourceCode\data','.xls');

        for iLoopTime := 0 to fileList.Count - 1 do
        begin


          res:= import.import(fileList.Strings[iLoopTime] , resMsg)  ;
        end;
        }
      res := import.import(list,mainform.Memo1, resmsg);

      if res<>0 then
      begin
        sline := datetimetostr(now) +'出错:' + resmsg ;
        Synchronize(addmemo);
      end;
    except
      Err   := Exception(ExceptObject);
      sline := datetimetostr(now) +'出错:' + err.Message ;
      Synchronize(addmemo);
    end;
  finally
    List.Clear  ;
    Synchronize(incCounter);
    import.Destroy ;
  end;

end;

procedure TThreadImportDaily.incCounter;
begin
  inc( mainform.finished ) ;
end;

end.
