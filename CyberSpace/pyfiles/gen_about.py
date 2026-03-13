import re
import os

html_path = r'c:\Users\deepu\Desktop\cyber space new updated\cyber space new\cyber space new\cyberspace.html'
out_path = r'c:\Users\deepu\Desktop\cyber space new updated\cyber space new\cyber space new\about.html'

with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace <main class="main"> ... </main><!-- /main -->
about_content = r"""<main class="main" style="grid-template-columns: 1fr; display: flex; flex-direction: column; gap: 30px; margin-top: 20px;">
      
      <!-- PAGE TITLE -->
      <div style="text-align: center; margin-bottom: 10px;">
        <h1 style="font-family: 'Orbitron', sans-serif; font-size: 3.2rem; font-weight: 900; color: #fff; text-shadow: 0 0 25px rgba(139, 92, 246, 0.7); letter-spacing: 0.05em; margin-bottom: 10px;">About Nyx Nexus</h1>
        <p style="font-family: 'Rajdhani', sans-serif; font-size: 1.25rem; font-weight: 600; color: var(--text-sub); text-transform: uppercase; letter-spacing: 0.1em;">Meet the team behind the Nyx Nexus learning platform.</p>
      </div>

      <!-- SECTION 1 – PLATFORM DESCRIPTION -->
      <div class="neon-border" style="width: 100%;">
        <div class="box-content" style="padding: 30px; text-align: center;">
          <p style="font-family: 'Rajdhani', sans-serif; font-size: 1.2rem; color: var(--text-main); line-height: 1.6; margin-bottom: 15px;">
            <strong style="color: #fff;">Nyx Nexus</strong> is a gamified cybersecurity learning platform designed to make learning security concepts interactive and engaging.
            Users explore different cyber labs, complete challenges, gain XP, unlock achievements, and follow guided career roadmaps such as SOC Analyst, Pentester, and Cloud Security Engineer.
          </p>
          <p style="font-family: 'Rajdhani', sans-serif; font-size: 1.2rem; color: var(--text-main); line-height: 1.6;">
            The platform combines cybersecurity training with a game-like environment to help learners develop real-world security skills.
          </p>
        </div>
      </div>

      <!-- SECTION 2 – OUR TEAM -->
      <h2 style="font-family: 'Orbitron', sans-serif; font-size: 2.2rem; font-weight: 800; color: #fff; text-shadow: 0 0 20px rgba(6, 182, 212, 0.6); text-align: center; margin-top: 10px;">Our Team</h2>
      
      <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; width: 100%;">
        
        <!-- TEAM MEMBER 1 -->
        <div class="game-card-small neon-border" style="overflow: visible; transition: transform 0.4s; z-index: 10;">
          <div class="box-content" style="padding: 24px 16px; display: flex; flex-direction: column; gap: 12px; height: 100%; align-items: center; text-align: center;">
            <div style="width: 70px; height: 70px; border-radius: 50%; background: linear-gradient(135deg, #7c3aed, #ec4899); display: flex; align-items: center; justify-content: center; font-size: 1.8rem; box-shadow: 0 0 20px rgba(139, 92, 246, 0.6); margin-bottom: 8px;">
              <i class="fas fa-laptop-code" style="color: white; animation: floatBreath 3s infinite ease-in-out;"></i>
            </div>
            <h3 style="font-family: 'Rajdhani', sans-serif; font-size: 1.4rem; font-weight: 800; color: #fff;">Deepthi V S</h3>
            <div style="color: #e879f9; font-family: 'Orbitron', sans-serif; font-size: 0.75rem; font-weight: 700; background: rgba(232, 121, 249, 0.1); padding: 5px 12px; border-radius: 12px; border: 1px solid rgba(232, 121, 249, 0.3);">Frontend Developer</div>
            <p style="font-family: 'Rajdhani', sans-serif; font-size: 0.95rem; color: var(--text-sub); line-height: 1.5; margin-top: 8px;">
              Responsible for designing and building the user interface of the platform. Developed the interactive dashboards, roadmap visuals, gamified UI elements, and overall user experience.
            </p>
          </div>
        </div>

        <!-- TEAM MEMBER 2 -->
        <div class="game-card-small neon-border" style="overflow: visible; transition: transform 0.4s; z-index: 10;">
          <div class="box-content" style="padding: 24px 16px; display: flex; flex-direction: column; gap: 12px; height: 100%; align-items: center; text-align: center;">
            <div style="width: 70px; height: 70px; border-radius: 50%; background: linear-gradient(135deg, #f97316, #ef4444); display: flex; align-items: center; justify-content: center; font-size: 1.8rem; box-shadow: 0 0 20px rgba(249, 115, 22, 0.6); margin-bottom: 8px;">
              <i class="fas fa-gamepad" style="color: white; animation: floatBreath 3s infinite ease-in-out; animation-delay: 0.5s;"></i>
            </div>
            <h3 style="font-family: 'Rajdhani', sans-serif; font-size: 1.4rem; font-weight: 800; color: #fff;">G Murali Krishnan</h3>
            <div style="color: #fb923c; font-family: 'Orbitron', sans-serif; font-size: 0.75rem; font-weight: 700; background: rgba(249, 115, 22, 0.1); padding: 5px 12px; border-radius: 12px; border: 1px solid rgba(249, 115, 22, 0.3);">Game Mechanics</div>
            <p style="font-family: 'Rajdhani', sans-serif; font-size: 0.95rem; color: var(--text-sub); line-height: 1.5; margin-top: 8px;">
              Designed the interactive cybersecurity game environments and learning labs. Responsible for building engaging challenges and game logic to make cybersecurity learning fun and immersive.
            </p>
          </div>
        </div>

        <!-- TEAM MEMBER 3 -->
        <div class="game-card-small neon-border" style="overflow: visible; transition: transform 0.4s; z-index: 10;">
          <div class="box-content" style="padding: 24px 16px; display: flex; flex-direction: column; gap: 12px; height: 100%; align-items: center; text-align: center;">
            <div style="width: 70px; height: 70px; border-radius: 50%; background: linear-gradient(135deg, #3b82f6, #06b6d4); display: flex; align-items: center; justify-content: center; font-size: 1.8rem; box-shadow: 0 0 20px rgba(59, 130, 246, 0.6); margin-bottom: 8px;">
              <i class="fas fa-robot" style="color: white; animation: floatBreath 3s infinite ease-in-out; animation-delay: 1s;"></i>
            </div>
            <h3 style="font-family: 'Rajdhani', sans-serif; font-size: 1.4rem; font-weight: 800; color: #fff;">Manasvi V</h3>
            <div style="color: #60a5fa; font-family: 'Orbitron', sans-serif; font-size: 0.75rem; font-weight: 700; background: rgba(59, 130, 246, 0.1); padding: 5px 12px; border-radius: 12px; border: 1px solid rgba(59, 130, 246, 0.3);">AI & Backend</div>
            <p style="font-family: 'Rajdhani', sans-serif; font-size: 0.95rem; color: var(--text-sub); line-height: 1.5; margin-top: 8px;">
              Developed the backend logic and integrated intelligent features like the MR NOVA AI assistant. Handles data processing, system functionality, and AI-driven guidance across the platform.
            </p>
          </div>
        </div>

        <!-- TEAM MEMBER 4 -->
        <div class="game-card-small neon-border" style="overflow: visible; transition: transform 0.4s; z-index: 10;">
          <div class="box-content" style="padding: 24px 16px; display: flex; flex-direction: column; gap: 12px; height: 100%; align-items: center; text-align: center;">
            <div style="width: 70px; height: 70px; border-radius: 50%; background: linear-gradient(135deg, #22c55e, #10b981); display: flex; align-items: center; justify-content: center; font-size: 1.8rem; box-shadow: 0 0 20px rgba(34, 197, 94, 0.6); margin-bottom: 8px;">
              <i class="fas fa-shield-alt" style="color: white; animation: floatBreath 3s infinite ease-in-out; animation-delay: 1.5s;"></i>
            </div>
            <h3 style="font-family: 'Rajdhani', sans-serif; font-size: 1.4rem; font-weight: 800; color: #fff;">Thanusha P</h3>
            <div style="color: #4ade80; font-family: 'Orbitron', sans-serif; font-size: 0.75rem; font-weight: 700; background: rgba(34, 197, 94, 0.1); padding: 5px 12px; border-radius: 12px; border: 1px solid rgba(34, 197, 94, 0.3);">Challenge Dev</div>
            <p style="font-family: 'Rajdhani', sans-serif; font-size: 0.95rem; color: var(--text-sub); line-height: 1.5; margin-top: 8px;">
              Worked on designing cybersecurity challenges and gamified learning mechanics. Focused on creating engaging tasks and interactive gameplay elements within the platform.
            </p>
          </div>
        </div>

      </div>

      <!-- SECTION 3 – PROJECT GOAL -->
      <div class="neon-border" style="width: 100%; margin-top: 10px;">
        <div class="box-content" style="padding: 30px; text-align: center;">
          <h2 style="font-family: 'Orbitron', sans-serif; font-size: 2.2rem; font-weight: 800; color: #fff; margin-bottom: 15px; text-shadow: 0 0 20px rgba(249, 115, 22, 0.6);">Our Mission</h2>
          <p style="font-family: 'Rajdhani', sans-serif; font-size: 1.2rem; color: var(--text-main); line-height: 1.6; margin-bottom: 10px;">
            Our goal is to make cybersecurity learning accessible, interactive, and engaging through gamification and intelligent guidance.
          </p>
          <p style="font-family: 'Rajdhani', sans-serif; font-size: 1.2rem; color: var(--text-main); line-height: 1.6;">
            Nyx Nexus transforms traditional learning into an immersive digital experience where users can explore, practice, and master cybersecurity skills.
          </p>
        </div>
      </div>
      
    </main>"""

# Using regex to find the `<main class="main">` boundary
new_text = re.sub(r'<main class="main">.*?</main><!-- /main -->', about_content, text, flags=re.DOTALL)

# Add active nav link matching handling if needed? We will just update the title
new_text = new_text.replace('<title>Nyx Nexus - The Digital Realm</title>', '<title>About Nyx Nexus</title>')

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Generated about.html successfully.")
