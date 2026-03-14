// The configuration for episodes acts as the backend/database state
export const EPISODE_DATA = {
    "1": {
        id: "1",
        title: "The Midnight Invoice",
        durationMinutes: 10,
        suspects: ["finance", "hr", "it"],
        labels: {
            "finance": "Finance Manager",
            "hr": "HR Intern",
            "it": "IT Administrator"
        },
        attackTypes: [
            { id: "brute-force", label: "Brute Force" },
            { id: "phishing", label: "Phishing" },
            { id: "malware", label: "Malware Infection" },
            { id: "insider", label: "Insider Threat" }
        ],
        entryPoints: [
            { id: "unpatched_server", label: "Unpatched Server" },
            { id: "fake_invoice", label: "Fake invoice email" },
            { id: "usb_drive", label: "Malicious USB Drive" },
            { id: "vpn_vuln", label: "VPN Vulnerability" }
        ],
        containmentActions: [
            { id: "disable", label: "Disable compromised account" },
            { id: "block", label: "Block malicious IP" },
            { id: "reset", label: "Reset passwords" },
            { id: "mfa", label: "Enable MFA" }
        ],
        evidenceImpact: {
            "fake_invoice": { finance: 40, hr: 10, it: 0 },
            "foreign_ip": { finance: 40, hr: 0, it: 20 },
            "tor_exit": { finance: 10, hr: 0, it: 30 }
        },
        solution: {
            attackType: "phishing",
            entryPoint: "fake_invoice",
            compromisedAccount: "finance",
            containment: ["disable", "block", "reset", "mfa"]
        }
    },
    "2": {
        id: "2",
        title: "The Silent Insider",
        durationMinutes: 10,
        suspects: ["dba", "marketing", "contractor", "it_support"],
        labels: {
            "dba": "Database Administrator",
            "marketing": "Marketing Executive",
            "contractor": "Temporary Contractor",
            "it_support": "Remote IT Support Engineer"
        },
        attackTypes: [
            { id: "malware", label: "Malware Attack" },
            { id: "phishing", label: "Phishing" },
            { id: "insider_theft", label: "Insider Data Theft" },
            { id: "network_breach", label: "Network Breach" }
        ],
        entryPoints: [], // Empty to hide this select group
        containmentActions: [
            { id: "revoke_access", label: "Revoke contractor access immediately" },
            { id: "audit_transfers", label: "Audit recent file transfers" },
            { id: "investigate_usb", label: "Investigate USB usage logs" },
            { id: "enable_dlp", label: "Enable Data Loss Prevention monitoring" }
        ],
        evidenceImpact: {
            "activity_logs": { contractor: 40, dba: 0, marketing: 0, it_support: 0 },
            "file_access": { contractor: 0, dba: 50, marketing: 0, it_support: 0 },
            "network_logs": { contractor: 40, dba: 0, marketing: 0, it_support: 10 }
        },
        solution: {
            attackType: "insider_theft",
            entryPoint: "none", // Since we rely on no entry point
            compromisedAccount: "contractor",
            containment: ["revoke_access", "audit_transfers", "investigate_usb", "enable_dlp"]
        },
        successMessage: "Threat Identified – Insider Data Exfiltration Stopped",
        failureMessage: "Investigation Failed – Insider activity continues undetected"
    }
};

export default class EpisodeManager {
    constructor(episodeId) {
        this.episodeConfig = EPISODE_DATA[episodeId];
        if (!this.episodeConfig) {
            console.error("Episode not found!");
        }

        // Track suspicion meters
        this.suspicionMeters = {};
        this.episodeConfig.suspects.forEach(s => this.suspicionMeters[s] = 0);
    }

    getEvidenceImpact(evidenceId) {
        return this.episodeConfig.evidenceImpact[evidenceId] || null;
    }

    updateSuspicion(evidenceId) {
        const impact = this.getEvidenceImpact(evidenceId);
        if (impact) {
            for (let suspect in impact) {
                if (this.suspicionMeters[suspect] !== undefined) {
                    this.suspicionMeters[suspect] += impact[suspect];
                    // Clamp to 100
                    this.suspicionMeters[suspect] = Math.min(100, this.suspicionMeters[suspect]);
                }
            }
        }
        return this.suspicionMeters;
    }

    getSolution() {
        return this.episodeConfig.solution;
    }

    getDuration() {
        return this.episodeConfig.durationMinutes;
    }
}
