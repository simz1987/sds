from playwright.sync_api import sync_playwright
import time

def run_bot():
    print("🤖 Booting up the cloud bot...")
    with sync_playwright() as p:
        # headless=True because the GitHub cloud doesn't have a physical monitor!
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("🌐 Going to the login page...")
        # NOTE: Replace the URL below with the ACTUAL web link to your SDS Portal!
        page.goto("https://auth.gln.com/identityservice/Login?appID=03C7D14F-F49A-4069-8A9F-868064A863C8&returnURL=https%3a%2f%2fwww.services.lnos.com%2flogin%2fDefaultMDLP.aspx%3ftenant%3d%7b%24tenant%7d") 
        
        # Wait a second for the page to fully load
        time.sleep(2)

        print("⌨️ Finding the email box and typing...")
        # Here is the magic ID you just found! The '#' symbol means "look for this ID"
        page.fill('#i0116', 'robot_test@yourcompany.com')

        print("📸 Taking a picture to prove it worked...")
        page.screenshot(path="robot_screenshot.png")

        print("✅ Done! Closing browser.")
        browser.close()

if __name__ == "__main__":
    run_bot()
