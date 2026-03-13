import re

with open("cyber-roadmap.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. CSS Injection
css_fixes = """
        /* Update Node Circle Sizes */
        .node {
            width: 90px;
            height: 90px;
            transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease !important;
        }
        .node i {
            font-size: 32px;
        }
        .step-num {
            font-size: 18px;
            font-weight: bold;
            width: 38px;
            height: 38px;
            top: -18px;
            left: -18px;
        }

        /* Career Destinations */
        .node.career {
            width: 140px;
            height: 140px;
            border-width: 3px;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
            /* Reset absolute pos since we use flex container */
            position: relative;
            transform: none !important;
            top: auto !important; left: auto !important;
        }
        .node.career i {
            font-size: 50px;
        }

        /* Hover Animation */
        .node.step-node:hover, .node.future-path:hover {
            transform: translate(-50%, -50%) scale(1.08) !important;
            box-shadow: 0 0 35px var(--cyan);
            z-index: 100;
        }
        .node.career:hover {
            transform: scale(1.08) !important;
            box-shadow: 0 0 45px var(--cyan);
            z-index: 100;
        }

        /* Fix Specialization Node */
        #choose-spec-node {
            width: 100px;
            height: 100px;
            animation: specPulse 2s infinite alternate;
        }
        @keyframes specPulse {
            0% { box-shadow: 0 0 10px var(--cyan); border-color: var(--cyan); }
            100% { box-shadow: 0 0 30px #fff; border-color: #fff; }
        }

        /* Clean Node HUD Text */
        .node-hud {
            position: absolute;
            top: 110px; /* Below the node */
            left: 50%;
            transform: translateX(-50%);
            width: 280px;
            text-align: center;
            pointer-events: none;
            max-width: 220px;
            margin: auto;
        }
        /* HUD alignment for flex items (careers) */
        .node.career .node-hud {
            top: 160px;
        }
        /* HUD alignment for larger specialization box */
        #choose-spec-node .node-hud {
            top: 120px;
        }

        .node-hud h3 {
            font-family: 'Orbitron';
            font-size: 16px;
            color: #fff;
            margin-top: 16px;
            margin-bottom: 10px;
            line-height: 1.5;
            text-transform: uppercase;
        }

        .node-hud p {
            font-family: 'Rajdhani';
            font-size: 14px;
            font-weight: 500;
            color: var(--text-sub);
            line-height: 1.5;
            margin: 0;
        }

        /* Larger Career Labels */
        .node.career .node-hud h3 {
            font-size: 20px;
            font-weight: bold;
            margin-top: 10px;
        }
        .node.career .node-hud p {
            font-size: 14px;
            opacity: 0.8;
        }

        /* Section Titles Alignments */
        .section-tag {
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
            text-shadow: 0 0 10px var(--cyan);
            transform: translateX(-50%);
            position: absolute;
            font-family: 'Orbitron';
            font-size: 16px;
            font-weight: 800;
            color: var(--cyan);
            background: rgba(6, 182, 212, 0.1);
            padding: 8px 24px;
            border: 1px solid var(--cyan);
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 40px;
            z-index: 5;
        }
        .section-tag-foundation { top: 30px; left: 50%; }
        .section-tag-core { top: 310px; left: 50%; }
        .section-tag-specialization { top: 610px; left: 50%; }
        .section-tag-careers { top: 880px; left: 50%; background: rgba(6, 182, 212, 0.2); }

        /* Career Flex Container */
        .career-row {
            display: flex;
            justify-content: space-evenly;
            align-items: center;
            position: absolute;
            top: 1050px;
            left: 0;
            width: 100%;
            z-index: 20;
        }

        /* Future Path Flex Container */
        .future-row {
            display: flex;
            justify-content: space-evenly;
            align-items: center;
            position: absolute;
            top: 1400px;
            left: 20%;
            width: 60%;
            z-index: 20;
        }
        .node.future-path {
            position: relative;
            transform: none !important;
            top: auto !important; left: auto !important;
        }
"""

html = html.replace("/* Zig-Zag Specific CSS */", css_fixes + "\\n        /* Zig-Zag Specific CSS */")

# Remove inline styles from node-hud elements that conflict
html = re.sub(r'<div class="node-hud" style="[^"]+">', '<div class="node-hud">', html)
html = re.sub(r'<h3 style="[^"]+">', '<h3>', html)
html = re.sub(r'<p style="[^"]+">', '<p>', html)

# Identify Specialization Node
html = html.replace('<div class="node step-node" style="top: 750px; left: 650px;">', '<div class="node step-node" id="choose-spec-node" style="top: 750px; left: 650px;">')

# Wrap Career paths in flex row
careers_html = """
            <!-- Career Paths Section -->
            <div class="section-tag section-tag-careers">CAREER PATHS</div>

            <div class="career-row">
                <!-- SOC ANALYST -->
                <div class="node career soc">
                    <i class="fas fa-user-shield"></i>
                    <div class="node-hud">
                        <h3>SOC ANALYST ✨</h3>
                        <p>Enterprise Defense Specialist</p>
                    </div>
                </div>

                <!-- PENTESTER -->
                <div class="node career pentest">
                    <i class="fas fa-user-ninja"></i>
                    <div class="node-hud">
                        <h3>PENTESTER ✨</h3>
                        <p>Offensive Operations Specialist</p>
                    </div>
                </div>

                <!-- CLOUD SECURITY -->
                <div class="node career cloud">
                    <i class="fas fa-cloud-lock"></i>
                    <div class="node-hud">
                        <h3>CLOUD SECURITY ENGINEER ✨</h3>
                        <p>Cloud Infrastructure Specialist</p>
                    </div>
                </div>
            </div>

            <!-- FUTURE PATHS -->
            <div class="future-row">
                <div class="node future-path">
                    <i class="fas fa-dna"></i>
                    <div class="node-hud">
                        <h3>MALWARE ANALYST</h3>
                        <p>Coming Soon</p>
                    </div>
                </div>

                <div class="node future-path">
                    <i class="fas fa-crosshairs"></i>
                    <div class="node-hud">
                        <h3>THREAT HUNTER</h3>
                        <p>Coming Soon</p>
                    </div>
                </div>
            </div>
        </div>"""

# Safely replace careers
pattern = r'<!-- Career Paths Section -->.*</div>\s*</div>\s*</div>'
html = re.sub(pattern, careers_html, html, flags=re.DOTALL)

with open("cyber-roadmap.html", "w", encoding="utf-8") as f:
    f.write(html)
