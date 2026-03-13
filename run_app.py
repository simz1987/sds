import os
import sys
import streamlit.web.cli as stcli

if __name__ == "__main__":
    # If the app is compiled into an .exe, PyInstaller unzips it into a hidden temp folder.
    # This tells the app to look inside that temp folder for your app.py and logo.png!
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)
        
    # This tricks the computer into running the Streamlit terminal command silently
    sys.argv = ["streamlit", "run", "app.py", "--global.developmentMode=false"]
    sys.exit(stcli.main())
