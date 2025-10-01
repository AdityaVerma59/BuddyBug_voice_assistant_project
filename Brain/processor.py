# Brain/processor.py
import os
import subprocess
import json
from rapidfuzz import fuzz, process as fuzz_process
from Brain.ai import ask_ai

with open("Brain/question_bank.json", "r") as f:
    QUESTION_BANK = json.load(f)

def fuzzy_match(query, choices, threshold=70):
    """
    Returns the best fuzzy match if score >= threshold
    """
    match, score, _ = fuzz_process.extractOne(query, choices, scorer=fuzz.partial_ratio)
    if score >= threshold:
        return match
    return None

def process(query):
    """
    Processes a query and either executes a local command or asks AI.
    """
    query = query.lower()

    # Local commands

    #shortcuts
    if "open word" in query or "open ms word" in query:
        os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Office Word 2007.lnk")
        return "Opening Word"
    elif "close word" in query:
        os.system("taskkill /im WINWORD.EXE /f")
        return "MS word is closed"

    elif "open powerpoint" in query:
        os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Office PowerPoint 2007.lnk")
        return "Opening PowerPoint"
    elif "close powerpoint" in query:
        os.system("taskkill /im POWERPNT.EXE /f")
        return "Closing PowerPoint"

    elif "open excel" in query:
        os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office\Microsoft Office Excel 2007.lnk")
        return "Opening Excel"
    elif "close excel" in query:
        os.system("taskkill /im EXCEL.EXE /f")
        return "Closing Excel"
    
    elif "open whatsapp" in query:
        os.startfile(r"C:\Users\verma\OneDrive\Desktop\WhatsApp - Shortcut.lnk")
        return "WhatsApp is open now"
    elif "close whatsapp" in query:
        os.system("taskkill /im WhatsApp.exe /f")
        return "WhatsApp closed"

    elif "open vs code" in query:
        os.startfile(r"C:\Users\verma\OneDrive\Desktop\Visual Studio Code - Shortcut.lnk")
        return "Opening visual studio Code, vs code is now ready to use, sir"
    elif "close vs code" in query:
        os.system("taskkill /im Code.exe /f")
        return "Closing VS Code"
    
    elif "open copilot" in query or "open co pilot" in query or "open Ko pilot" in query:
        os.startfile(r"C:\Users\verma\OneDrive\Desktop\Copilot - Shortcut.lnk")
        return "Opening Copilot"
    elif "close copilot" in query or "close co pilot" in query or "close Ko pilot" in query:
        os.system("taskkill /im Copilot.exe /f")
        return "Closing Copilot"
    
    elif "open calendar" in query:
        os.startfile(r"C:\Users\verma\OneDrive\Desktop\Calendar - Shortcut.lnk")
        return "Opening Calendar"
    elif "close calendar" in query:
        os.system("taskkill /im Outlook.exe /f")
        return "Closing Calendar"
    
    elif "open this pc" in query:
        os.startfile(r"C:\Users\verma\OneDrive\Desktop\This PC - Shortcut.lnk")
        return "This pc window is now open file explorer"
    elif "close this pc" in query:
        os.system("taskkill /im explorer.exe /f")
        return "Closing this pc"
    
    elif "open hill climb racing" in query:
        os.startfile(r"C:\Users\verma\OneDrive\Desktop\Hill Climb Racing - Shortcut.lnk")
        return "Opening Hill Climb Racing"
    elif "close hill climb racing" in query:
        os.system("taskkill /im HillClimbRacing.exe /f")
        return "Closing Hill Climb Racing"
    
    elif "open linkedin" in query or "open linked in" in query:
        os.startfile(r"C:\Users\verma\OneDrive\Desktop\Hill Climb Racing - Shortcut.lnk")
        return "Linkedin is open now"
    elif "close linkedin" in query or "close linked in" in query:
        os.system("taskkill /im Linkedin.exe /f")
        return "Linkedin is closed now"
    
    elif "open ultraviewer" in query or "open ultra viewer" in query:
        os.startfile(r"C:\Users\verma\OneDrive\Desktop\UltraViewer - Shortcut.lnk")
        return "ultra viewer is open now"
    elif "close ultra viewer" in query or "close ultraviewer" in query:
        os.system("taskkill /im ultraviewer.exe /f")
        return "ultra viewer is closed now"
    
    elif "open photos" in query:
        os.startfile(r"C:\Users\verma\OneDrive\Desktop\Photos - Shortcut.lnk")
        return "Opening Photos"
    elif "close photos" in query:
        os.system("taskkill /im ApplicationFrameHost.exe /f")
        return "Closing Photos"

    elif "open paint 3d" in query:
        os.startfile(r"C:\Users\verma\OneDrive\Desktop\Paint 3D - Shortcut.lnk")
        return "Opening Paint 3D"
    elif "close paint 3d" in query:
        os.system("taskkill /im ApplicationFrameHost.exe /f")
        return "Closing Paint 3D"
    
    #exe files

    elif "open microsoft edge" in query or "open edge" in query:
        subprocess.Popen(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
        return "Microsoft Edge is open now, anything else sir"
    elif "close microsoft edge" in query or "close edge" in query:
        os.system("taskkill /im msedge.exe /f")
        return "Closing Microsoft Edge"

    elif "open chrome" in query:
        subprocess.Popen("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        return "Chrome is open now, anything else sir?"
    elif "close chrome" in query:
        os.system("taskkill /im chrome.exe /f")
        return "The Chrome window is closed"
    
    elif "open notepad" in query:
        subprocess.Popen("notepad.exe")
        return "Opening Notepad"
    elif "close notepad" in query:
        os.system("taskkill /im notepad.exe /f")
        return "Notepad closed"

    elif "open file explorer" in query:
        subprocess.Popen("explorer.exe")
        return "Opening File Explorer"
    elif "close file explorer" in query:
        os.system("taskkill /im explorer.exe /f")
        return "Closing File Explorer"

    elif "open microsoft store" in query:
        subprocess.Popen(r"C:\Windows\System32\WinStore.App.exe")
        return "I have opened a new tab in Microsoft Store for you, sir."
    elif "close microsoft store" in query:
        os.system("taskkill /im WinStore.App.exe /f")
        return "Microsoft Store is closed now"

    elif "start menu" in query or "open start" in query:
        subprocess.Popen("explorer.exe shell:::{2559a1f3-21d7-11d4-bdaf-00c04f60b9f0}")
        return "Opening Start Menu"

    elif "open windows search" in query or "open search" in query:
        subprocess.Popen("explorer.exe shell:::{9E5B12C9-0801-4D12-B8D3-0AB6D0B1C0CC}")
        return "Opening Windows Search"

    elif "open camera" in query:
        subprocess.Popen("microsoft.windows.camera:")
        return "Opening Camera"
    elif "close camera" in query:
        os.system("taskkill /im WindowsCamera.exe /f")
        return "Closing Camera"

    elif "open clock" in query:
        subprocess.Popen("ms-clock:")
        return "Opening Clock"
    elif "close clock" in query:
        os.system("taskkill /im ApplicationFrameHost.exe /f")
        return "Closing Clock"

    elif "open cortana" in query:
        subprocess.Popen("C:\\Windows\\System32\\Cortana.exe")
        return "Opening Cortana"
    elif "close cortana" in query:
        os.system("taskkill /im Cortana.exe /f")
        return "Closing Cortana"

    elif "open maps" in query:
        subprocess.Popen("bingmaps:")
        return "Opening Maps"
    elif "close maps" in query:
        os.system("taskkill /im ApplicationFrameHost.exe /f")
        return "Closing Maps"

    elif "open voice recorder" in query:
        subprocess.Popen("soundrecorder.exe")
        return "Opening Voice Recorder"
    elif "close voice recorder" in query:
        os.system("taskkill /im soundrecorder.exe /f")
        return "Closing Voice Recorder"

    elif "open skype" in query:
        subprocess.Popen(r"C:\Program Files (x86)\Microsoft\Skype for Desktop\Skype.exe")
        return "Opening Skype"
    elif "close skype" in query:
        os.system("taskkill /im Skype.exe /f")
        return "Closing Skype"

    elif "open chat gpt on chrome" in query:
        subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe https://chat.openai.com")
        return "Opening ChatGPT on Chrome"
    elif "open youtube on chrome" in query:
        subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe https://youtube.com")
        return "Opening YouTube on Chrome"
    
    #shutdown and restart pc commands
    
    elif "shutdown the pc" in query or "shutdown the computer" in query:
        os.system("shutdown /s /t 1")
        return "Shutting down your computer"

    elif "restart the pc" in query or "restart the computer" in query:
        os.system("shutdown /r /t 1")
        return "Restarting your computer"

    
    q_match = fuzzy_match(query, QUESTION_BANK.keys())
    if q_match:
        return QUESTION_BANK[q_match]
    
    else:
        return ask_ai(query)
