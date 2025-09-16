[Setup]
; Basic application information
AppName=Automation Studio Selector
AppVersion=1.0.0
AppPublisher=Indigo R&D Division
AppPublisherURL=
AppSupportURL=
AppUpdatesURL=
DefaultDirName={autopf}\Automation Studio Selector
DefaultGroupName=Automation Studio Selector
AllowNoIcons=yes
LicenseFile=
InfoAfterFile=
OutputDir=installer
OutputBaseFilename=AutomationStudioSelector_Setup_v1.0.0
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
; Main application files
Source: "dist\AutomationStudioSelector\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Configuration example
Source: "auto_sync_config_example.xml"; DestDir: "{app}"; Flags: ignoreversion
; Documentation
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Automation Studio Selector"; Filename: "{app}\AutomationStudioSelector.exe"
Name: "{group}\{cm:UninstallProgram,Automation Studio Selector}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Automation Studio Selector"; Filename: "{app}\AutomationStudioSelector.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Automation Studio Selector"; Filename: "{app}\AutomationStudioSelector.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\AutomationStudioSelector.exe"; Description: "{cm:LaunchProgram,Automation Studio Selector}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{localappdata}\Automation Studio Selector"
Type: filesandordirs; Name: "{userappdata}\.automation_selector"

[Code]
procedure InitializeWizard;
begin
  WizardForm.WelcomeLabel1.Caption := 'Welcome to Automation Studio Selector Setup';
  WizardForm.WelcomeLabel2.Caption := 
    'This will install Automation Studio Selector v1.0.0 on your computer.' + #13#13 +
    'This professional tool allows you to manage multiple Automation Studio installations ' +
    'and seamlessly switch between project configurations.' + #13#13 +
    'Created by Vitaly Grosman - Indigo R&D Division' + #13#13 +
    'Click Next to continue, or Cancel to exit Setup.';
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
  if not IsWin64 then begin
    MsgBox('This application requires a 64-bit version of Windows.', mbError, MB_OK);
    Result := False;
  end;
end;
