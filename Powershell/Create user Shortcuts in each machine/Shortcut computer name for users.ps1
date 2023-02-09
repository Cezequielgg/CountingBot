$hostname = hostname

$Account_array = Get-LocalUser | Where-Object Enabled | Select-Object -Property Name ;

$Array_of_user = $Account_array.name ;

foreach ($user in $Array_of_user){ $test = Test-Path -Path "C:\Users\$user\Desktop\THISCOMPUTERNAMEIS___$hostname.lnk" ;

if( $test -eq $False)

{ $TargetFile = "C:\windows\system32\systempropertiescomputername.exe" ;

$ShortcutFile = "C:\Users\$user\Desktop\THISCOMPUTERNAMEIS___$hostname.lnk";

$WScriptShell = New-Object -ComObject WScript.Shell;

$Shortcut = $WScriptShell.CreateShortcut($ShortcutFile);

$Shortcut.TargetPath = $TargetFile ;

$Shortcut.Save() } }