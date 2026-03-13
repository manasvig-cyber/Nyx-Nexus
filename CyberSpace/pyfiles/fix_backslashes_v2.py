import os
import glob

html_files = glob.glob('*.html')

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Generic replacement for the href part
    new_content = content.replace("href=\\'achievements.html\\'", "href='achievements.html'")
    # Also handle if it somehow got double backslashed or similar
    new_content = new_content.replace("href=\'achievements.html\'", "href='achievements.html'")
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Fixed {f}")
