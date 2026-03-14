import os
import glob
import re

html_files = glob.glob('*.html')

sidebar_addition = """                <div class="nav-item" style="--i: #8b5cf6; --j: #ec4899;">
                    <i class="fas fa-robot"></i>
                    <span class="nav-label">Nova AI</span>
                </div>
                <div class="nav-item" style="--i: #06b6d4; --j: #3b82f6;" onclick="window.location.href='achievements.html'">
                    <i class="fas fa-trophy"></i>
                    <span class="nav-label">Achievements</span>
                </div>"""

css_addition = """    <link rel="stylesheet" href="cyber-notifications.css">
</head>"""

js_addition = """    <script src="cyber-notifications.js"></script>
</body>"""

for f in html_files:
    if f == 'achievements.html':
        continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Update sidebar
    pattern = r'(\s*)<div class="nav-item" style="--i: #8b5cf6; --j: #ec4899;">\s*<i class="fas fa-robot"></i>\s*<span class="nav-label">Nova AI</span>\s*</div>(?!\s*<div class="nav-item" style="--i: #06b6d4; --j: #3b82f6;")'
    
    replacement = r'\1<div class="nav-item" style="--i: #8b5cf6; --j: #ec4899;">\1    <i class="fas fa-robot"></i>\1    <span class="nav-label">Nova AI</span>\1</div>\1<div class="nav-item" style="--i: #06b6d4; --j: #3b82f6;" onclick="window.location.href=\'achievements.html\'">\1    <i class="fas fa-trophy"></i>\1    <span class="nav-label">Achievements</span>\1</div>'
    
    content = re.sub(pattern, replacement, content)
    
    # Add css (if not already there)
    if 'cyber-notifications.css' not in content:
        content = content.replace('</head>', css_addition)
    
    # Add js
    if 'cyber-notifications.js' not in content:
        content = content.replace('</body>', js_addition)
        
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
print("Updated HTML files!")
