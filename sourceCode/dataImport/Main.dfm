object MainForm: TMainForm
  Left = 0
  Top = 0
  Caption = 'MainForm'
  ClientHeight = 460
  ClientWidth = 834
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
    Width = 834
    Height = 460
    Align = alClient
    ImeName = #20013#25991'('#31616#20307') - '#30334#24230#36755#20837#27861
    Lines.Strings = (
      'Memo1')
    ReadOnly = True
    ScrollBars = ssBoth
    TabOrder = 0
  end
  object MainMenu1: TMainMenu
    Left = 776
    Top = 392
    object N1: TMenuItem
      Caption = #24320#22987
      OnClick = N1Click
    end
    object N2: TMenuItem
      Caption = #20572#27490
      OnClick = N2Click
    end
    object N3: TMenuItem
      Caption = #28165#23631
      OnClick = N3Click
    end
  end
  object Timer1: TTimer
    Interval = 10000
    OnTimer = Timer1Timer
    Left = 776
    Top = 352
  end
end
