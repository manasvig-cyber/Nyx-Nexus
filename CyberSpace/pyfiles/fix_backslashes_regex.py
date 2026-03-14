import os
import glob
import re

html_files = glob.glob('*.html')

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Use regex to find and replace the problematic onclick
    new_content = re.sub(r'onclick="window\.location\.href=\\?\'achievements\.html\\?\'"', r'onclick="window.location.href=\'achievements.html\'"', content)
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Fixed {f}")
