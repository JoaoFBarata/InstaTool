Set oShell = CreateObject ("Wscript.Shell")
Dim strArgs
scriptdir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
strArgs = "cmd /c " & Chr(34) & scriptdir & "\launch.bat" & Chr(34)
oShell.Run strArgs, 0, false