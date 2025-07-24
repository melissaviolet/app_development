; Installer Script for FreshTally Connector

!define APPNAME "FreshTally Connector"
!define EXENAME "main.exe"
!define INSTALLDIR "$PROGRAMFILES\${APPNAME}"

Outfile "FreshTallyConnectorSetup.exe"
InstallDir "${INSTALLDIR}"
RequestExecutionLevel admin

Page directory
Page instfiles

Section "Install"
  SetOutPath "$INSTDIR"

  ; Copy files
  File "C:\Users\user\Desktop\freshtall_connector\dist\main.exe"
  File "C:\Users\user\Desktop\freshtall_connector\config.json"
  File "C:\Users\user\Desktop\freshtall_connector\serviceAccountKey.json"
  File "C:\Users\user\Desktop\freshtall_connector\icon.ico"

  ; Optional: Log file (only include if you have it)
  ; File "app_log.txt"

  ; Create a shortcut in Start Menu
  CreateDirectory "$SMPROGRAMS\${APPNAME}"
  CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\${EXENAME}" "" "$INSTDIR\icon.ico"

  ; Create a shortcut on Desktop (optional)
  CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${EXENAME}" "" "$INSTDIR\icon.ico"

SectionEnd
