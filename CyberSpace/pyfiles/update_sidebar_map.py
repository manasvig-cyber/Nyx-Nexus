
import os
import re

files_to_update = [
    "security-automation-room.html",
    "python-basics-room.html",
    "programming-automation-rooms.html",
    "networking-rooms.html",
    "network-room2.html",
    "network-room1.html",
    "network-room2-tasks.html",
    "learning-path.html",
    "games.html",
    "cyberspace.html",
    "cyber-roadmap.html",
    "ctf-challenges.html",
    "achievements.html",
    "about.html"
]

base_dir = r"c:\Users\deepu\Desktop\cyber space new updated\cyber space new\cyber space new"

# Updated search pattern to catch various formatting
# Target: <div class="nav-item"...><i class="fas fa-lightbulb"></i><span class="nav-label">Cyber Tips</span></div>

for filename in files_to_update:
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for the nav-item containing Cyber Tips
    # We want to add the onclick if it's missing, and change the label
    
    # First, let's find the Cyber Tips block
    # Sample: 
    # <div class="nav-item" style="--i: #8b5cf6; --j: #ec4899;">
    #   <i class="fas fa-lightbulb"></i>
    #   <span class="nav-label">Cyber Tips</span>
    # </div>
    
    # We'll use a regex to find the div and its contents
    pattern = re.compile(r'(<div\s+class="nav-item"[^>]*style="--i:\s*#8b5cf6;\s*--j:\s*#ec4899;"[^>]*>)\s*(<i\s+class="fas\s+fa-lightbulb"></i>)\s*(<span\s+class="nav-label">)Cyber Tips(</span>)\s*(</div>)', re.IGNORECASE | re.DOTALL)
    
    def replacer(match):
        div_start = match.group(1)
        icon = match.group(2)
        span_start = match.group(3)
        span_end = match.group(4)
        div_end = match.group(5)
        
        # Check if onclick already exists
        if 'onclick' not in div_start:
            # Change <div ...> to <div ... onclick="window.location.href='global-threat-map/index.html'">
            div_start = div_start[:-1] + ' onclick="window.location.href=\'global-threat-map/index.html\'">'
        
        # We can also change the icon if we want, but let's stick to the prompt's request
        # Changing Cyber Tips to MAP
        return f'{div_start}\n          {icon}\n          {span_start}MAP{span_end}\n        {div_end}'

    new_content = pattern.sub(replacer, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
    else:
        # Fallback for slightly different structures (e.g. icon already changed or spacing differences)
        # Search specifically for the label Cyber Tips within a nav-label span
        label_pattern = re.compile(r'(<span\s+class="nav-label">)Cyber Tips(</span>)', re.IGNORECASE)
        new_content = label_pattern.sub(r'\1MAP\2', content)
        
        # Check if we need to add onclick to the parent div
        # Find the div that contains <span class="nav-label">MAP</span> and doesn't have onclick
        parent_pattern = re.compile(r'(<div\s+class="nav-item"[^>]*style="--i:\s*#8b5cf6;\s*--j:\s*#ec4899;"(?!.*onclick)[^>]*>)\s*(.*?<span\s+class="nav-label">MAP</span>.*?</div>)', re.DOTALL)
        new_content = parent_pattern.sub(lambda m: m.group(1)[:-1] + ' onclick="window.location.href=\'global-threat-map/index.html\'">' + m.group(2), new_content)

        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename} (fallback)")
        else:
            print(f"No changes made to {filename}")
