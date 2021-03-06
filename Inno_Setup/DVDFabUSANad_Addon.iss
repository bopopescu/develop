; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
OutputBaseFilename=Woookao
AppName=Woookao
AppVerName=Woookao
DefaultDirName={pf}\Woookao
DirExistsWarning=false
DefaultGroupName=Woookao
DisableReadyPage=true
;DisableDirPage=yes
;Uninstallable=no
;DisableProgramGroupPage=true
AllowNoIcons=true
DisableStartupPrompt=true
RestartIfNeededByRun=false
PrivilegesRequired=admin
WizardImageStretch=no
Compression=lzma2/ultra64
InternalCompressLevel=ultra64
SolidCompression=true
LanguageDetectionMethod=uilanguage
;Tells the installer to only display a select language dialog if the an exact match wasn't found
ShowUndisplayableLanguages=yes

[Languages]
;Inno Setup's Native Language
Name: English; MessagesFile: compiler:Languages\English.isl


[Files]
Source: ..\Runtime_mobile2\appcfg_uad.zip; DestDir: {code:NewTargetDir};  Check: IsExists; DestName: appcfg.zip; Flags: ignoreversion restartreplace
Source: ..\Runtime_mobile2\appcfg_uad.zip; DestDir: {code:TDMoreBDCopyTargetDir};  Check: IsTDMoreBDCopyExists; DestName: tdmore.zip; Flags: ignoreversion restartreplace
Source: ..\Runtime_mobile2\appcfg_uad.zip; DestDir: {code:TDMoreBDConverterTargetDir};  Check: IsTDMoreBDConverterExists; DestName: tdmore.zip; Flags: ignoreversion restartreplace
Source: ..\Runtime_mobile2\appcfg_uad.zip; DestDir: {code:TDMoreBDCopyShareVersionTargetDir};  Check: IsTDMoreBDCopyShareVersionExists; DestName: tdmore.zip; Flags: ignoreversion restartreplace
Source: dvd43\DVD43.dll; DestDir: "{sys}"; Flags: ignoreversion
Source: boooya\*; DestDir: {code:s123CopyDVDDir}; Check: is123CopyDVDExists; Flags: recursesubdirs  ignoreversion

[Icons]
Name: {group}\Uninstall Woookao; Filename: {uninstallexe}

[Code]

var
  bNeedRestart: Boolean;
  sNewPath: string;
  sTDMoreBDCopyNewPath: string;
  sTDMoreBDConverterNewPath: string;
  sTDMoreBDCopyShareVersionNewPath: string;
  s123CopyDVDPath: string;

function InitializeSetup(): Boolean;
var
  sInstallPathResult, 
  sTDMoreBDCopyInstallPathResult,
  sTDMoreBDConverterInstallPathResult,
  sTDMoreBDCopyShareVersionInstallPathResult,
  sSubPath, 
  sFileSearch,
  sNotifyStr : string;
  filename, newfilename: string;
  sFabPath: string;
  StrPost : integer;
  sKey, sValueName: string; 
  sTDMoreBDCopyKey, sTDMoreBDCopyValueName: string; 
  sTDMoreBDConverterKey, sTDMoreBDConverterValueName: string;
  sTDMoreBDCopyShareVersionKey, sTDMoreBDCopyShareVersionValueName: string; 

begin
	bNeedRestart := FALSE;
	Result := True;
  sNewPath := '';
  sTDMoreBDCopyNewPath := '';
  sTDMoreBDConverterNewPath := '';
  sTDMoreBDCopyShareVersionNewPath := '';
  s123CopyDVDPath := '';

  sFabPath := ExpandConstant('{userappdata}') + '\DVDFab9';
  sNotifyStr := 'Sorry, but DVDFab is not found on your PC. Please download DVDFab at http://www.dvdfab.cn. Setup will exit now.';

  sKey := 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\DVDFab 9 US_is1';
  sValueName := 'InstallLocation';   
  //check if install DVDFabNonDecAll by register uninstall key of DVDFabNonDecAll
  //if RegQueryStringValue(HKEY_LOCAL_MACHINE, sKey, sValueName, sInstallPathResult) then
  if RegQueryStringValue(HKEY_LOCAL_MACHINE, sKey, sValueName, sInstallPathResult) then
  begin
  //MsgBox(sInstallPathResult, mbInformation, MB_OK);
      if DirExists(sInstallPathResult) then
      begin
          sNewPath := sInstallPathResult;         
          filename := sNewPath + '\appcfg.zip'
          newfilename := sFabPath + '\appcfg.zip'
          if FileExists(filename) then
          begin
            FileCopy(filename,newfilename, True);  
          end; 
      end;
  end;

  

  sFabPath := ExpandConstant('{userappdata}') + '\TDMore Blu-ray Copy';
  sTDMoreBDCopyKey := 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\TDMore Blu-ray Copy_is1';
  sTDMoreBDCopyValueName := 'InstallLocation';   
  //if RegQueryStringValue(HKEY_LOCAL_MACHINE, sKey, sValueName, sInstallPathResult) then
  if RegQueryStringValue(HKEY_LOCAL_MACHINE, sTDMoreBDCopyKey, sTDMoreBDCopyValueName, sTDMoreBDCopyInstallPathResult) then
  begin
  //MsgBox(sInstallPathResult, mbInformation, MB_OK);
      if DirExists(sTDMoreBDCopyInstallPathResult) then
      begin
          sTDMoreBDCopyNewPath := sTDMoreBDCopyInstallPathResult;           
          filename := sTDMoreBDCopyNewPath + '\tdmore.zip'
          newfilename := sFabPath + '\tdmore.zip'
          if FileExists(filename) then
          begin
            FileCopy(filename,newfilename, True);  
          end;       
      end; 
  end;


  sFabPath := ExpandConstant('{userappdata}') + '\TDMore Blu-ray Converter';
  sTDMoreBDConverterKey := 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\TDMore Blu-ray Converter_is1';
  sTDMoreBDConverterValueName := 'InstallLocation';   
  //if RegQueryStringValue(HKEY_LOCAL_MACHINE, sKey, sValueName, sInstallPathResult) then
  if RegQueryStringValue(HKEY_LOCAL_MACHINE, sTDMoreBDConverterKey, sTDMoreBDConverterValueName, sTDMoreBDConverterInstallPathResult) then
  begin
  //MsgBox(sInstallPathResult, mbInformation, MB_OK);
      if DirExists(sTDMoreBDConverterInstallPathResult) then
      begin
          sTDMoreBDConverterNewPath := sTDMoreBDConverterInstallPathResult; 
          filename := sTDMoreBDConverterNewPath + '\tdmore.zip'
          newfilename := sFabPath + '\tdmore.zip'
          if FileExists(filename) then
          begin
            FileCopy(filename,newfilename, True);  
          end;         
      end; 
  end;


  sFabPath := ExpandConstant('{userappdata}') + '\TDMore Blu-ray Copy Share Version';
  sTDMoreBDCopyShareVersionKey := 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\TDMore Blu-ray Copy Share Version_is1';
  sTDMoreBDCopyShareVersionValueName := 'InstallLocation';   
  //if RegQueryStringValue(HKEY_LOCAL_MACHINE, sKey, sValueName, sInstallPathResult) then
  if RegQueryStringValue(HKEY_LOCAL_MACHINE, sTDMoreBDCopyShareVersionKey, sTDMoreBDCopyShareVersionValueName, sTDMoreBDCopyShareVersionInstallPathResult) then
  begin
  //MsgBox(sInstallPathResult, mbInformation, MB_OK);
      if DirExists(sTDMoreBDCopyShareVersionInstallPathResult) then
      begin
          sTDMoreBDCopyShareVersionNewPath := sTDMoreBDCopyShareVersionInstallPathResult;           
          filename := sTDMoreBDCopyShareVersionNewPath + '\tdmore.zip'
          newfilename := sFabPath + '\tdmore.zip'
          if FileExists(filename) then
          begin
            FileCopy(filename,newfilename, True);  
          end;       
      end; 
  end;


  sInstallPathResult := '';
  //whether 123CopyDVD installed
  sKey := 'SOFTWARE\BlingSoftwareLtd';
  sValueName := '123CopyDVDPlatinum'; 
  if RegQueryStringValue(HKEY_LOCAL_MACHINE, sKey, sValueName, sInstallPathResult) then
  begin
  //MsgBox(sInstallPathResult, mbInformation, MB_OK);
      if DirExists(sInstallPathResult) then
      begin
          s123CopyDVDPath := sInstallPathResult;      
      end; 
  end;
     end;


//function InitializeUninstall(): Boolean;
//var
//  sInstallPathResult,
//  srcfile: string;
//  destfile: string;
//  sFabPath: string;
//  sKey, sValueName: string;
//begin
// sFabPath := ExpandConstant('{userappdata}') + '\DVDFab9';
//  sKey := 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\DVDFab 9 UAD_is1';
//  sValueName := 'InstallLocation';
//  if RegQueryStringValue(HKEY_LOCAL_MACHINE, sKey, sValueName, sInstallPathResult) then
//  begin
//    srcfile := sFabPath + '\appcfg.zip'
//    destfile := sInstallPathResult + '\appcfg.zip'
//
//    if FileExists(srcfile) then
//    begin
//      FileCopy(srcfile,destfile,False);
//    end;
//  end;
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  sInstallPathResult,
  srcfile: string;
  destfile: string;
  sFabPath: string;
  sKey, sValueName: string;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    sFabPath := ExpandConstant('{userappdata}') + '\DVDFab9';
    sKey := 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\DVDFab 9 US_is1';
    sValueName := 'InstallLocation';
    if RegQueryStringValue(HKEY_LOCAL_MACHINE, sKey, sValueName, sInstallPathResult) then
    begin
      srcfile := sFabPath + '\appcfg.zip'
      destfile := sInstallPathResult + '\appcfg.zip'

      if FileExists(srcfile) then
      begin
        FileCopy(srcfile,destfile,False);
        DeleteFile(srcfile);
      end;
    end;

    sFabPath := ExpandConstant('{userappdata}') + '\TDMore Blu-ray Copy';
    sKey := 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\TDMore Blu-ray Copy_is1';
    sValueName := 'InstallLocation';
    if RegQueryStringValue(HKEY_LOCAL_MACHINE, sKey, sValueName, sInstallPathResult) then
    begin
      srcfile := sFabPath + '\tdmore.zip'
      destfile := sInstallPathResult + '\tdmore.zip'

      if FileExists(srcfile) then
      begin
        FileCopy(srcfile,destfile,False);
        DeleteFile(srcfile);
      end;
    end;


    sFabPath := ExpandConstant('{userappdata}') + '\TDMore Blu-ray Converter';
    sKey := 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\TDMore Blu-ray Converter_is1';
    sValueName := 'InstallLocation';
    if RegQueryStringValue(HKEY_LOCAL_MACHINE, sKey, sValueName, sInstallPathResult) then
    begin
      srcfile := sFabPath + '\tdmore.zip'
      destfile := sInstallPathResult + '\tdmore.zip'

      if FileExists(srcfile) then
      begin
        FileCopy(srcfile,destfile,False);
        DeleteFile(srcfile);
      end;
    end;


    sFabPath := ExpandConstant('{userappdata}') + '\TDMore Blu-ray Copy Share Version';
    sKey := 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\TDMore Blu-ray Copy Share Version_is1';
    sValueName := 'InstallLocation';
    if RegQueryStringValue(HKEY_LOCAL_MACHINE, sKey, sValueName, sInstallPathResult) then
    begin
      srcfile := sFabPath + '\tdmore.zip'
      destfile := sInstallPathResult + '\tdmore.zip'

      if FileExists(srcfile) then
      begin
        FileCopy(srcfile,destfile,False);
        DeleteFile(srcfile);
      end;
    end;


  end;
end;


function NewTargetDir(subPath:string): String;
var
  newPath: string;
begin
    newPath := sNewPath;
    Result := newPath;
end;


function IsExists(): Boolean;
var 
  is_exists: Boolean;

begin
  if  DirExists(sNewPath) then 
  begin
    is_exists := True;
  end
  else begin
    is_exists := False;
  end;
  Result := is_exists;
end;


function TDMoreBDCopyTargetDir(subPath:string): String;
var
  newPath: string;
begin
    newPath := sTDMoreBDCopyNewPath;
    Result := newPath;
end;


function IsTDMoreBDCopyExists(): Boolean;
var 
  is_exists: Boolean;

begin
  if  DirExists(sTDMoreBDCopyNewPath) then 
  begin
    is_exists := True;
  end
  else begin
    is_exists := False;
  end;
  Result := is_exists;
end;



function TDMoreBDConverterTargetDir(subPath:string): String;
var
  newPath: string;
begin
    newPath := sTDMoreBDConverterNewPath;
    Result := newPath;
end;


function IsTDMoreBDConverterExists(): Boolean;
var 
  is_exists: Boolean;

begin
  if  DirExists(sTDMoreBDConverterNewPath) then 
  begin
    is_exists := True;
  end
  else begin
    is_exists := False;
  end;
  Result := is_exists;
end;



function TDMoreBDCopyShareVersionTargetDir(subPath:string): String;
var
  newPath: string;
begin
    newPath := sTDMoreBDCopyShareVersionNewPath;
    Result := newPath;
end;


function IsTDMoreBDCopyShareVersionExists(): Boolean;
var 
  is_exists: Boolean;

begin
  if  DirExists(sTDMoreBDCopyShareVersionNewPath) then 
  begin
    is_exists := True;
  end
  else begin
    is_exists := False;
  end;
  Result := is_exists;
end;


function s123CopyDVDDir(subPath:string): String;
var
  newPath: string;
begin
    newPath := s123CopyDVDPath;
    Result := newPath;
end;


function is123CopyDVDExists(): Boolean;
var 
  is_exists: Boolean;

begin
  if  DirExists(s123CopyDVDPath) then 
  begin
    is_exists := True;
  end
  else begin
    is_exists := False;
  end;
  Result := is_exists;
end;


procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssDone  then
  begin
    MsgBox('If the movie copy or ripping program which you want to use Woookao to help to decrtpt is running now, you have to restart it to make Woookao work.', mbInformation, MB_OK);
  end
end;

//procedure DeinitializeSetup();
//begin
//  MsgBox('You need restart the software', mbInformation, MB_OK); 
//end;