export default class ScoreSystem {
    constructor() {
        this.baseScore = 100;
        this.deductions = {
            wrongSuspect: 20,
            wrongAttackType: 15,
            wrongEntryPoint: 15,
            missedContainment: 5, // per missed action
            wrongContainment: 5   // per unnecessary action
        };
        this.timeBonusPerSecond = 0.05; // points per remaining second
    }

    /**
     * Calculates the final score
     * @param {Object} playerSubmission 
     * @param {Object} correctSolution 
     * @param {number} timeRemaining 
     * @returns {Object} result details
     */
    evaluate(playerSubmission, correctSolution, timeRemaining) {
        let score = this.baseScore;
        let feedback = [];
        let isSuccess = true;

        if (playerSubmission.attackType !== correctSolution.attackType) {
            score -= this.deductions.wrongAttackType;
            feedback.push(`- Threat misclassification. This was a ${correctSolution.attackType} attack, not ${playerSubmission.attackType}.`);
            isSuccess = false;
        }

        if (playerSubmission.entryPoint !== correctSolution.entryPoint) {
            score -= this.deductions.wrongEntryPoint;
            feedback.push(`- Incorrect entry vector identified.`);
            isSuccess = false;
        }

        if (playerSubmission.compromisedAccount !== correctSolution.compromisedAccount) {
            score -= this.deductions.wrongSuspect;
            feedback.push(`- Wrong suspect identified. The threat actor remains in the system.`);
            isSuccess = false;
        }

        // Compare containment arrays
        let correctContainments = 0;
        correctSolution.containment.forEach(action => {
            if (playerSubmission.containment.includes(action)) {
                correctContainments++;
            } else {
                score -= this.deductions.missedContainment;
                feedback.push(`- Missed critical containment action: ${action}`);
                isSuccess = false;
            }
        });

        playerSubmission.containment.forEach(action => {
            if (!correctSolution.containment.includes(action)) {
                score -= this.deductions.wrongContainment;
                feedback.push(`- Unnecessary containment action taken: ${action}`);
            }
        });

        // Apply time bonus if successful
        if (isSuccess && timeRemaining > 0) {
            score += Math.floor(timeRemaining * this.timeBonusPerSecond);
        }

        score = Math.max(0, Math.min(score, 100)); // clamp between 0 and 100

        let rank = "Rookie";
        if (score >= 90) rank = "Elite Analyst";
        else if (score >= 75) rank = "Senior Investigator";
        else if (score >= 50) rank = "Junior Analyst";

        return {
            score,
            rank,
            feedback,
            isSuccess
        };
    }
}
