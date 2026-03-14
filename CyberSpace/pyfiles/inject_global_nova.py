import os
import glob
import re

directory = r"c:\Users\deepu\Desktop\cyber space new updated\cyber space new\cyber space new"

# Search for all HTML files
html_files = glob.glob(os.path.join(directory, "*.html"))

# Regex to strip out any existing MR NOVA CSS, HTML, or JS
css_regex = re.compile(r'\s*/\*\s*MR NOVA AI Widget CSS\s*\*/.*?(?=</style>)', re.DOTALL)
html_regex = re.compile(r'\s*<!-- MR NOVA AI Floating Widget -->.*?(?=</main>|</div>\s*</div>\s*</body>)', re.DOTALL)
js_regex = re.compile(r'\s*// MR NOVA AI Smart Logic.*?(?=</script>\s*</body>)', re.DOTALL)

for file in html_files:
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean old inline Nova stuff
    cleaned_content = css_regex.sub('', content)
    cleaned_content = html_regex.sub('', cleaned_content)
    cleaned_content = js_regex.sub('', cleaned_content)
    
    # Also clean explicit old <div class="nova-widget">...</div> blocks if missed
    nova_widget_regex = re.compile(r'\s*<div class="nova-widget">.*?</div>\s*</div>\s*', re.DOTALL)
    cleaned_content = nova_widget_regex.sub('\n', cleaned_content)
    
    # Also check if another old NOVA logic exists
    old_js_regex = re.compile(r'\s*// MR NOVA AI Smart Logic.*?</script>', re.DOTALL)
    cleaned_content = old_js_regex.sub('</script>', cleaned_content)
    
    # Remove any existing mr-nova.js script tags to avoid duplicates
    cleaned_content = re.sub(r'<script src="mr-nova\.js"></script>\n?', '', cleaned_content)

    # Insert global script tag before closing </body>
    script_tag = '<script src="mr-nova.js"></script>\n'
    if "</body>" in cleaned_content:
        cleaned_content = cleaned_content.replace("</body>", f"    {script_tag}</body>")
    else:
        # If no body for some reason, just append
        cleaned_content += f"\n{script_tag}"

    with open(file, "w", encoding="utf-8") as f:
        f.write(cleaned_content)

print(f"Injected mr-nova.js into {len(html_files)} files.")
