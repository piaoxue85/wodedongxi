object main: Tmain
  Left = 0
  Top = 0
  Caption = 'main'
  ClientHeight = 550
  ClientWidth = 695
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
    Width = 695
    Height = 550
    Align = alClient
    Lines.Strings = (
      'Memo1')
    TabOrder = 0
  end
  object MainMenu1: TMainMenu
    Left = 632
    Top = 408
    object N1: TMenuItem
      Caption = #24320#22987
      OnClick = N1Click
    end
  end
end
