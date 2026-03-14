import os
import glob
import re

directory = r"c:\Users\deepu\Desktop\cyber space new updated\cyber space new\cyber space new"

html_files = glob.glob(os.path.join(directory, "*.html"))

# We want to replace the Nova AI nav item with Cyber Tips
# The pattern should match <div class="nav-item" style="--i: #8b5cf6; --j: #ec4899;" (optional onclick)> ... <i class="fas fa-robot"></i> ... <span class="nav-label">Nova AI</span> ... </div>

nova_nav_pattern = re.compile(
    r'<div class="nav-item" style="--i: #8b5cf6; --j: #ec4899;"[^>]*>\s*<i class="fas fa-robot"></i>\s*<span class="nav-label">Nova AI</span>\s*</div>',
    re.IGNORECASE | re.DOTALL
)

replacement = """<div class="nav-item" style="--i: #8b5cf6; --j: #ec4899;">
                <i class="fas fa-lightbulb"></i>
                <span class="nav-label">Cyber Tips</span>
            </div>"""

for file in html_files:
    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = nova_nav_pattern.sub(replacement, content)
        
        if new_content != content:
            with open(file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {os.path.basename(file)}")
            
    except Exception as e:
        print(f"Error processing {file}: {e}")

