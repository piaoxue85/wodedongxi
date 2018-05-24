object fMain: TfMain
  Left = 0
  Top = 0
  Caption = 'fMain'
  ClientHeight = 387
  ClientWidth = 643
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  Menu = MainMenu1
  OldCreateOrder = False
  OnCreate = FormCreate
  PixelsPerInch = 96
  TextHeight = 13
  object Memo1: TMemo
    Left = 0
    Top = 0
    Width = 643
    Height = 387
    Align = alClient
    Lines.Strings = (
      'Memo1')
    ReadOnly = True
    ScrollBars = ssBoth
    TabOrder = 0
  end
  object MainMenu1: TMainMenu
    Left = 568
    Top = 16
    object N1: TMenuItem
      Caption = #36864#20986
    end
    object genCSV: TMenuItem
      Caption = #29983#25104'CSV'
      OnClick = genCSVClick
    end
    object genPoint: TMenuItem
      Caption = #29983#25104#20080#21334#28857
      OnClick = genPointClick
    end
  end
  object Timer1: TTimer
    Interval = 10
    OnTimer = Timer1Timer
    Left = 520
    Top = 16
  end
end
