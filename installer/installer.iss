#define AppName "Startup Notifier"
#define AppVersion GetEnv('APP_VERSION')
#define AppPublisher "Arsh Sisodiya"
#define AppExeName "StartupNotifier.exe"
#define AppDirName "Startup Notifier"
#define TaskName "StartupNotifierTask"

[Setup]
AppId={{9A5E9D2F-8C24-4F92-B2A9-STARTUPNOTIFIERBYARSH}}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={pf}\{#AppDirName}
DisableDirPage=yes
DefaultGroupName={#AppName}
OutputDir=output
OutputBaseFilename=StartupNotifierSetup-{#AppVersion}
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\{#AppExeName}
UninstallDisplayName={#AppName}
WizardStyle=modern
SetupLogging=yes
LicenseFile=license.txt

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "..\dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Registry]
; Remove Windows Run key entry on uninstall
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; \
    ValueName: "StartupNotifier"; \
    Flags: deletevalue uninsdeletevalue

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"

[Run]

Filename: "schtasks.exe"; \
Parameters: "/create /f /sc onlogon /tn ""{#TaskName}"" /tr """"{app}\{#AppExeName}"""""; \
Flags: runhidden

Filename: "{app}\{#AppExeName}"; \
Flags: nowait

; =============================
; UNINSTALL SECTION
; =============================

[UninstallRun]

; Kill running process safely
Filename: "taskkill.exe"; \
Parameters: "/f /im {#AppExeName}"; \
Flags: runhidden; \
RunOnceId: "KillStartupNotifier"

; Delete scheduled task safely
Filename: "schtasks.exe"; \
Parameters: "/delete /f /tn ""{#TaskName}"""; \
Flags: runhidden; \
RunOnceId: "DeleteStartupNotifierTask"

; =============================
; OPTIONAL DATA DELETE PROMPT
; =============================

[Code]

var
  DeleteData: Boolean;

procedure InitializeUninstallProgressForm;
var
  Response: Integer;
begin
  Response :=
    MsgBox(
      'Do you want to delete all application data (logs, config, activity data)?',
      mbConfirmation,
      MB_YESNO or MB_DEFBUTTON2
    );

  DeleteData := (Response = idYes);
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  DataPath: String;
begin
  if (CurUninstallStep = usPostUninstall) and DeleteData then
  begin
    DataPath := ExpandConstant('{localappdata}\{#AppDirName}');
    if DirExists(DataPath) then
      DelTree(DataPath, True, True, True);
  end;
end;
