object fMain: TfMain
  Left = 0
  Top = 0
  Caption = #23450#26102#26597#30475#21508#21608#26399#25968#25454#29983#25104#32467#26524#65292#22914#26524#26377#23601#24320#22987#25214
  ClientHeight = 430
  ClientWidth = 603
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
    Width = 603
    Height = 430
    Align = alClient
    Lines.Strings = (
      'Memo1')
    ReadOnly = True
    ScrollBars = ssBoth
    TabOrder = 0
  end
  object MainMenu1: TMainMenu
    Left = 480
    Top = 280
    object N1: TMenuItem
      Caption = #24320#22987
      OnClick = N1Click
    end
    object N2: TMenuItem
      Caption = #32467#26463
      OnClick = N2Click
    end
  end
end
