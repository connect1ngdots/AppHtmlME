# vim: fileencoding=utf-8
"""
MarsEdit
@author Toshiya NISHIO(http://www.toshiya240.com)
"""
import subprocess

def inputText(msg):
    # 引用符をシェルのエスケープと AppleScript のエスケープの２重に行う
    cmd = ('osascript -e '
            '"tell application \"MarsEdit\"'
            ' to display dialog \"%s\"'
            ' buttons {\"Cancel\", \"OK\"} default button \"OK\" default answer \"\""' % msg.replace('"', '\\\\\\"'))
    p = subprocess.Popen(cmd, shell=True, close_fds=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate(None)

    result = ""
    if p.returncode != 0:
        result = None
    else:
        line = stdout.replace('\n', '')
        result = line.split(',')[0].split(':')[1]
    return result

def choose(msg, dic):
    # 引用符をシェルのエスケープと AppleScript のエスケープの２重に行う
    keys = '{%s}' % ",".join(['\\"%s\\"' % k.replace('"', '\\\\\\"') for k in sorted(dic.keys())])
    cmd = ('osascript -e '
            '"tell application \\"MarsEdit\\"'
            ' to choose from list %s'
            ' with prompt \\"%s\\"'
            ' cancel button name \\"Cancel\\"'
            ' without multiple selections allowed"'
            ) % (keys, msg)
    p = subprocess.Popen(cmd, shell=True, close_fds=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate(None)
    key = stdout.rstrip('\n')

    result = ''
    if key == 'false':
        result = None
    else:
        result = dic[key]
    return result

def write(text):
    p = subprocess.Popen("osascript - \"%s\"" % text.replace('"', '\\"') , shell=True, close_fds=True,
            stdin=subprocess.PIPE)
    p.communicate("""
    on run {input}
        tell application \"MarsEdit\"
            set dc to count documents
            if dc is equal to 0 then
                make new document
            end if
            set currentWindow to document 1

            set delim_orig to text item delimiters of AppleScript
            set text item delimiters of AppleScript to return
            set selected text of currentWindow to input as text
            set text item delimiters of AppleScript to delim_orig
            activate
        end tell
    end run
    """)

def displayError(msg):
    cmd = ('osascript -e '
            '\'tell application "MarsEdit"'
            ' to display dialog "%s"'
            ' buttons {"OK"} default button "OK"'
            ' with icon caution\'') % msg
    subprocess.call(cmd, shell=True)
