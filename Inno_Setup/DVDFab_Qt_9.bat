"..\Bin\ASProtect\ASProtect.exe" -process ".\FabProcess_DVDFab.aspr"
"..\Bin\ASProtect\ASProtect.exe" -process ".\DVDFab_Qt_9.aspr"
Rem: "..\Bin\ASProtect\ASProtect.exe" -process ".\FabCopy.aspr"
Rem: "..\Bin\ASProtect\ASProtect.exe" -process ".\FabUpdate.aspr"

"..\Bin\signtool.exe" sign /v /a /n "Fengtao Software Inc." /t http://timestamp.verisign.com/scripts/timestamp.dll ".\V9_Qt\DVDFab.exe"
"..\Bin\signtool.exe" sign /v /a /n "Fengtao Software Inc." /t http://timestamp.verisign.com/scripts/timestamp.dll ".\V9_Qt\FabProcess_DVDFab.exe"

"..\Bin\signtool.exe" sign /v /a /n "Fengtao Software Inc." /t http://timestamp.verisign.com/scripts/timestamp.dll ".\Common\FileOp.exe"

Rem: "..\Bin\signtool.exe" sign /v /a /t http://timestamp.verisign.com/scripts/timestamp.dll ".\V9_Qt\FabCopy.exe"

Rem: "..\Bin\signtool.exe" sign /v /a /n "Fengtao Software Inc." /t http://timestamp.verisign.com/scripts/timestamp.dll ".\V9_Qt\FabCopy.exe"

Rem: "..\Bin\signtool.exe" sign /v /a /n "Li Xichen" /t http://timestamp.wosign.com/timestamp ".\V9_Qt\Tdmore.exe"

Rem: "..\Bin\signtool.exe" sign /v /a /t http://timestamp.verisign.com/scripts/timestamp.dll ".\V9_Qt\FabUpdate.exe"
Rem: "..\Bin\signtool.exe" sign /v /a /t http://timestamp.verisign.com/scripts/timestamp.dll ".\Common\FabCore.exe"
Rem: "..\Bin\signtool.exe" sign /v /a /t http://timestamp.verisign.com/scripts/timestamp.dll ".\Common\FabCheck.exe"
Rem: "..\Bin\signtool.exe" sign /v /a /t http://timestamp.verisign.com/scripts/timestamp.dll ".\Common\FabRegOp.exe"
Rem: "..\Bin\signtool.exe" sign /v /a /t http://timestamp.verisign.com/scripts/timestamp.dll ".\Qt\FabReport.exe"
Rem: "..\Bin\signtool.exe" sign /v /a /t http://timestamp.verisign.com/scripts/timestamp.dll ".\Qt\FileMover.exe"


Rem: call .\Signature.py



"..\Bin\Inno Setup 5\iscc.exe" "/Ssigntoolcmd=SignTool $p" ".\DVDFab_Qt_9.iss"


rd /s /q "C:\Program Files\DVDFab 9"

call .\install_DVDFab.py

call ..\FabUpdateCreator\Create_Fabupdate.bat

copy /Y ..\FabupdateCreator\Fabupdate\update.xml .\V9_Qt\

"..\Bin\Inno Setup 5\iscc.exe" "/Ssigntoolcmd=SignTool $p" ".\DVDFab_Qt_9.iss"

Rem: call .\copy_FabUpdate_to_nas.py