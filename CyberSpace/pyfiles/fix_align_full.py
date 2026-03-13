import re

html_content = """        <header class="page-header">
            <h1 class="page-title">CYBERSECURITY CAREER ROADMAP</h1>
            <p class="page-subtitle">Follow the learning journey from cybersecurity foundations to specialized career roles.</p>
        </header>

        <!-- Centered Container -->
        <div class="roadmap-container">
            <!-- Absolute Roadmap SVG inside a structured content layout -->
            <svg class="roadmap-svg" viewBox="0 0 1200 1350" preserveAspectRatio="none">
                <!-- Drop shadow filter for SVG -->
                <defs>
                    <filter id="roadGlow" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur stdDeviation="6" result="blur" />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                </defs>

                <!-- Main Path Line -->
                <path fill="none" class="road-stroke" filter="url(#roadGlow)" d="M 150,150 L 1050,150 C 1150,150 1150,450 1050,450 L 150,450 C 50,450 50,750 150,750 L 600,750" />
                
                <!-- Animated glowing dots (data flow) -->
                <path fill="none" class="road-particles" d="M 150,150 L 1050,150 C 1150,150 1150,450 1050,450 L 150,450 C 50,450 50,750 150,750 L 600,750" />
                
                <!-- Branches from Node 6 (600, 750) to Careers (y=1050) -->
                <!-- SOC Analyst -->
                <path fill="none" class="branch-line" style="stroke:var(--green);" d="M 600,750 C 600,900 200,900 200,1050" />
                <path fill="none" class="branch-particles" style="stroke:var(--green);" d="M 600,750 C 600,900 200,900 200,1050" />
                
                <!-- Pentester -->
                <path fill="none" class="branch-line" style="stroke:var(--red);" d="M 600,750 L 600,1050" />
                <path fill="none" class="branch-particles" style="stroke:var(--red);" d="M 600,750 L 600,1050" />

                <!-- Cloud Security -->
                <path fill="none" class="branch-line" style="stroke:var(--purple-l);" d="M 600,750 C 600,900 1000,900 1000,1050" />
                <path fill="none" class="branch-particles" style="stroke:var(--purple-l);" d="M 600,750 C 600,900 1000,900 1000,1050" />
            </svg>

            <!-- Foundation Skills Section -->
            <div class="section-tag" style="top: 0px;">FOUNDATION SKILLS</div>

            <!-- ROW 1 (y = 150) -->
            <div class="node step-node" style="top: 150px; left: 150px;">
                <div class="step-num">01</div>
                <i class="fas fa-power-off"></i>
                <div class="node-hud">
                    <h3>SYSTEM START</h3>
                    <p>Initialize your journey into cybersecurity.</p>
                </div>
            </div>

            <div class="node step-node" style="top: 150px; left: 600px;">
                <div class="step-num">02</div>
                <i class="fas fa-network-wired"></i>
                <div class="node-hud">
                    <h3>NETWORKING FUNDAMENTALS</h3>
                    <p>Learn OSI model, TCP/IP, and packet communication.</p>
                </div>
            </div>

            <div class="node step-node" style="top: 150px; left: 1050px;">
                <div class="step-num">03</div>
                <i class="fab fa-linux"></i>
                <div class="node-hud">
                    <h3>LINUX CORE</h3>
                    <p>Understand Linux commands, permissions, and system operations.</p>
                </div>
            </div>

            <!-- Core Security Knowledge Section -->
            <div class="section-tag" style="top: 300px;">CORE SECURITY KNOWLEDGE</div>

            <!-- ROW 2 (y = 450) -->
            <div class="node step-node" style="top: 450px; left: 1050px;">
                <div class="step-num">04</div>
                <i class="fas fa-shield-halved"></i>
                <div class="node-hud">
                    <h3>SECURITY BASICS</h3>
                    <p>Learn cryptography, authentication, and security principles.</p>
                </div>
            </div>

            <div class="node step-node" style="top: 450px; left: 600px;">
                <div class="step-num">05</div>
                <i class="fas fa-brain"></i>
                <div class="node-hud">
                    <h3>CYBER LOGIC</h3>
                    <p>Develop attacker mindset and security analysis thinking.</p>
                </div>
            </div>

            <!-- Specialization Section -->
            <div class="section-tag" style="top: 600px;">SPECIALIZATION</div>

            <!-- ROW 3 (y = 750) -->
            <div class="node step-node" id="choose-spec-node" style="top: 750px; left: 600px;">
                <div class="step-num">06</div>
                <i class="fas fa-code-branch"></i>
                <div class="node-hud">
                    <h3>CHOOSE SPECIALIZATION</h3>
                    <p>Select your cybersecurity career path.</p>
                </div>
            </div>

            <!-- Career Paths Section -->
            <div class="section-tag" style="top: 900px; background: rgba(6, 182, 212, 0.2);">CAREER PATHS</div>

            <!-- ROW 4 flex row at 1050px -->
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
        </div>"""

css = """        /* Clean Centered Roadmap Layout Layout */
        .roadmap-container {
            position: relative;
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            min-height: 1400px;
            /* Remove any overlay */
            background: transparent;
        }

        .roadmap-svg {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: visible;
            background: transparent;
        }

        .road-stroke {
            fill: none !important;
            stroke: rgba(6, 182, 212, 0.4);
            stroke-width: 6;
            stroke-linecap: round;
            stroke-linejoin: round;
            box-shadow: 0 0 12px rgba(0, 255, 255, 0.4); /* Glow requested */
        }

        .road-particles {
            fill: none !important;
            stroke: #fff;
            stroke-width: 4;
            stroke-dasharray: 4, 30;
            stroke-linecap: round;
            animation: flowData 15s linear infinite;
            filter: drop-shadow(0 0 8px var(--cyan));
        }

        .branch-line {
            fill: none !important;
            stroke-width: 3;
            opacity: 0.5;
            stroke-dasharray: 6, 6;
        }
        .branch-particles {
            fill: none !important;
            stroke-width: 4;
            stroke-dasharray: 4, 25;
            stroke-linecap: round;
            animation: flowData 5s linear infinite;
            filter: drop-shadow(0 0 8px #fff);
        }

        @keyframes flowData {
            to { stroke-dashoffset: -1000; }
        }

        /* Milestone Node Configuration */
        .node {
            width: 90px;
            height: 90px;
            background: rgba(15, 23, 42, 0.95);
            border: 3px solid var(--cyan);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 20;
            cursor: pointer;
            transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease !important;
            /* Remove large box shadow that causes overlay look */
        }

        .step-node {
            position: absolute;
            transform: translate(-50%, -50%);
        }

        .node i {
            font-size: 32px;
            color: var(--cyan);
            transition: 0.4s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .node:hover i {
            color: #fff;
            text-shadow: 0 0 15px #fff;
        }
        
        /* Node Number Badge */
        .step-num {
            position: absolute;
            top: -15px;
            left: -15px;
            background: var(--bg-deep);
            color: var(--cyan);
            border: 2px solid var(--cyan);
            border-radius: 50%;
            width: 38px;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Orbitron';
            font-size: 16px;
            font-weight: bold;
            box-shadow: 0 0 10px var(--cyan);
            z-index: 30;
        }

        /* Fix Specialization Node */
        #choose-spec-node {
            width: 100px;
            height: 100px;
            animation: specPulse 2s infinite alternate;
        }
        #choose-spec-node i { font-size: 38px; }
        @keyframes specPulse {
            0% { box-shadow: 0 0 10px var(--cyan); border-color: var(--cyan); }
            100% { box-shadow: 0 0 30px #fff; border-color: #fff; }
        }

        /* Career Destinations Container */
        .career-row {
            display: flex;
            justify-content: space-evenly;
            align-items: center;
            position: absolute;
            top: 1050px;
            left: 0;
            width: 100%;
            z-index: 20;
            margin-top: 80px; /* Space off branch */
        }

        .node.career {
            width: 140px;
            height: 140px;
            border-width: 3px;
            position: relative;
            transform: none !important;
            top: auto !important; left: auto !important;
        }
        .node.career i { font-size: 50px; }
        
        .node.career.soc { border-color: var(--green); filter: drop-shadow(0 0 12px var(--green)); }
        .node.career.soc i { color: var(--green); }
        .node.career.soc:hover { box-shadow: 0 0 35px var(--green); }
        
        .node.career.pentest { border-color: var(--red); filter: drop-shadow(0 0 12px var(--red));}
        .node.career.pentest i { color: var(--red); }
        .node.career.pentest:hover { box-shadow: 0 0 35px var(--red); }
        
        .node.career.cloud { border-color: var(--purple-l); filter: drop-shadow(0 0 12px var(--purple-l));}
        .node.career.cloud i { color: var(--purple-l); }
        .node.career.cloud:hover { box-shadow: 0 0 35px var(--purple-l); }
        
        /* Hover Animation */
        .node.step-node:hover {
            transform: translate(-50%, -50%) scale(1.08) !important;
            box-shadow: 0 0 35px var(--cyan);
            border-color: #fff;
            z-index: 100;
        }
        .node.career:hover {
            transform: scale(1.08) !important;
            border-color: #fff;
            z-index: 100;
        }

        /* Text Block Clean Positioning */
        .node-hud {
            position: absolute;
            top: 110px; /* 90px circle + 20px spacing */
            left: 50%;
            transform: translateX(-50%);
            width: 220px;
            max-width: 220px;
            text-align: center;
            pointer-events: none;
            margin: auto;
        }
        
        /* Special offsets */
        .node.career .node-hud {
            top: 160px; /* 140px circle + 20px spacing */
            width: 280px;
            max-width: 280px;
        }
        #choose-spec-node .node-hud {
            top: 120px; /* 100px circle + 20px spacing */
        }

        .node-hud h3 {
            font-family: 'Orbitron';
            font-size: 16px;
            color: #fff;
            margin-bottom: 8px;
            margin-top: 20px;
            line-height: 1.4;
            text-transform: uppercase;
        }

        .node-hud p {
            font-family: 'Rajdhani';
            font-size: 14px;
            font-weight: 500;
            color: var(--text-sub);
            line-height: 1.4;
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
            left: 50%;
            font-family: 'Orbitron';
            font-size: 18px; 
            font-weight: 800;
            color: var(--cyan);
            background: rgba(6, 182, 212, 0.1);
            padding: 8px 24px;
            border: 1px solid var(--cyan);
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-top: 60px; /* Requested vertical margin */
            margin-bottom: 40px;
            z-index: 5;
            text-align: center;
        }
"""

with open("cyber-roadmap.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace main content
main_start = html.find('<header class="page-header">')
main_end = html.find('</main>', main_start)

if main_start != -1 and main_end != -1:
    html = html[:main_start] + html_content + "\n    " + html[main_end:]

# Add CSS before closing </style>
# Find the start of the roadmap specific CSS 
style_start = html.find('/* Clean Centered Roadmap Layout Layout */')
if style_start == -1:
    style_start = html.find('/* Fixed Timeline Layout Layout */')
style_end = html.find('</style>')

if style_start != -1 and style_end != -1:
    html = html[:style_start] + css + "\n    " + html[style_end:]

with open("cyber-roadmap.html", "w", encoding="utf-8") as f:
    f.write(html)
