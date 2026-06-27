import { useParams } from "react-router-dom";
import { 
  Download, 
  MapPin, 
  ShieldCheck, 
  Mail, 
  Zap, 
  TrendingUp, 
  AlertTriangle, 
  Users, 
  BookOpen, 
  Sparkles, 
  CheckCircle2, 
  ArrowRight,
  Clock,
  Briefcase
} from "lucide-react";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { Badge } from "../components/ui/Badge";
import { ProgressRing } from "../components/ui/ProgressRing";
import { useTalentMindStore } from "../state/useTalentMindStore";

export function CandidateDetail() {
  const { id } = useParams();
  const candidates = useTalentMindStore((state) => state.candidates);
  const candidate = candidates.find((item) => item.id === id) || candidates[0];

  if (!candidate) {
    return (
      <div className="flex h-64 items-center justify-center">
        <p className="text-lg text-muted-foreground">No candidate profile loaded</p>
      </div>
    );
  }

  // 19-Part Organizational DNA Matching Engine Data Layer & Fallbacks
  const getOrCreateDnaData = (cand) => {
    if (cand.candidate_dna && cand.dna_match) {
      return {
        candidate_dna: cand.candidate_dna,
        organization_dna: cand.organization_dna,
        dna_match: cand.dna_match,
        team_compatibility: cand.team_compatibility,
        culture_failure: cand.culture_failure,
        future_growth: cand.future_growth,
        personality: cand.personality
      };
    }
    
    // Seeded determinism based on candidate score / ID
    const seed = cand.score || 85;
    const scoreVal = seed;
    const behavioralVal = cand.behavioral || 80;
    const trustVal = cand.trust || 80;
    
    const speed = Math.round((0.5 + (seed * 0.0035) + (behavioralVal * 0.001)) * 100) / 100;
    const ownership = Math.round((0.4 + (seed * 0.0045)) * 100) / 100;
    const leadership = Math.round((0.35 + (seed * 0.005)) * 100) / 100;
    const innovation = Math.round((0.55 + (behavioralVal * 0.003)) * 100) / 100;
    const learning = Math.round((0.6 + (seed * 0.003)) * 100) / 100;
    const comm = Math.round((0.5 + (behavioralVal * 0.004)) * 100) / 100;
    const risk = Math.round((0.7 - (behavioralVal * 0.004)) * 100) / 100;
    
    const candidate_dna = {
      speed,
      ownership,
      leadership,
      innovation,
      learning,
      communication: comm,
      risk,
      adaptability: Math.round(((learning + speed) / 2) * 100) / 100,
      stability: Math.round((1 - risk) * 100) / 100,
      creativity: Math.round(((innovation + learning) / 2) * 100) / 100,
      collaboration: Math.round(((comm + ownership) / 2) * 100) / 100,
      execution: Math.round(((speed + ownership) / 2) * 100) / 100,
      research: Math.round((innovation * 0.9 + learning * 0.1) * 100) / 100,
      management: leadership,
      experimentation: innovation,
      autonomy: ownership,
      ambiguity: risk,
      customer: Math.round((comm * 0.8 + ownership * 0.2) * 100) / 100,
      team: Math.round((comm * 0.7 + learning * 0.3) * 100) / 100,
      growth: learning
    };
    
    const organization_dna = {
      speed: 0.70,
      ownership: 0.65,
      innovation: 0.55,
      risk: 0.40,
      hierarchy: 0.80,
      documentation: 0.85,
      leadership: 0.95,
      communication: 0.95,
      execution: 0.92,
      adaptability: 0.60,
      learning: 0.75,
      experimentation: 0.45,
      discipline: 0.85,
      process: 0.90,
      compliance: 0.80,
      teamwork: 0.80,
      collaboration: 0.85,
      creativity: 0.50,
      stability: 0.85,
      ambiguity: 0.40,
      customer: 0.90,
      autonomy: 0.50,
      decision_speed: 0.50,
      accountability: 0.85
    };
    
    const org_match = Math.round((0.6 + (trustVal * 0.0035)) * 100) / 100;
    const work_style_match = Math.round((0.55 + (seed * 0.0035)) * 100) / 100;
    const leadership_match = Math.round((0.5 + (behavioralVal * 0.004)) * 100) / 100;
    const innovation_match = Math.round((0.6 + (seed * 0.003)) * 100) / 100;
    
    const dna_match = {
      organization_match: org_match,
      work_style_match,
      leadership_match,
      innovation_match,
      cosine_similarity: Math.round((org_match * 0.92) * 100) / 100,
      euclidean_similarity: Math.round((org_match * 0.88) * 100) / 100,
      manhattan_similarity: Math.round((org_match * 0.85) * 100) / 100
    };
    
    const compatibility = Math.round((0.65 + (behavioralVal * 0.003)) * 100) / 100;
    const conflict_probability = Math.round((0.35 - (behavioralVal * 0.003)) * 100) / 100;
    const synergy = Math.round((compatibility * 1.05) * 100) / 100;
    
    const team_compatibility = {
      compatibility,
      conflict_probability,
      knowledge_diversity: seed > 85 ? "HIGH" : "MODERATE",
      synergy,
      personality_diversity: Math.round((0.3 + (seed * 0.003)) * 100) / 100,
      innovation_contribution: Math.round((innovation * 1.05) * 100) / 100
    };
    
    const failure_score = Math.round((0.45 - (behavioralVal * 0.004)) * 100) / 100;
    const culture_failure = {
      culture_failure: failure_score,
      risk: failure_score > 0.5 ? "HIGH" : (failure_score > 0.25 ? "MEDIUM" : "LOW"),
      resignation_risk: Math.round((failure_score * 0.9) * 100) / 100,
      burnout_risk: Math.round((failure_score * 1.15) * 100) / 100,
      conflict_risk: conflict_probability,
      culture_mismatch: Math.round((1 - org_match) * 100) / 100,
      performance_degradation: Math.round((failure_score * 0.8) * 100) / 100,
      leadership_mismatch: Math.round((1 - leadership_match) * 100) / 100
    };
    
    const future_growth = {
      "6_months": Math.round((0.65 + (seed * 0.003)) * 100) / 100,
      "12_months": Math.round((0.70 + (seed * 0.0028)) * 100) / 100,
      "24_months": Math.round((0.75 + (seed * 0.0024)) * 100) / 100,
      "36_months": Math.round((0.80 + (seed * 0.002)) * 100) / 100,
      future_role: seed > 90 ? "Engineering Manager" : (seed > 80 ? "Lead Engineer" : "Senior Developer"),
      adaptability_forecast: learning >= 0.7 ? "High" : "Medium",
      leadership_forecast: leadership >= 0.7 ? "Leader" : "Contributor",
      innovation_forecast: innovation >= 0.7 ? "Innovator" : "Operator",
      retention_forecast: (1 - risk) >= 0.6 ? "Stable" : "At-Risk"
    };
    
    const personality = {
      primary: seed > 90 ? "Builder" : (seed > 80 ? "Architect" : "Executor"),
      secondary: behavioralVal > 80 ? "Mentor" : "Innovator",
      tertiary: seed > 85 ? "Explorer" : "Operator"
    };
    
    return {
      candidate_dna,
      organization_dna,
      dna_match,
      team_compatibility,
      culture_failure,
      future_growth,
      personality
    };
  };

  const getOrCreateCounterfactualData = (cand) => {
    if (cand.counterfactual) return cand.counterfactual;
    
    const seed = cand.score || 85;
    const currentScore = seed;
    const bestScore = Math.min(99, seed + 10);
    const futureRole = seed > 90 ? "Staff AI Engineer" : "Senior DevOps Architect";
    
    return {
      current_rank: cand.rank || 2,
      future_rank: 1,
      probability: 0.87,
      composite_score: Math.round((seed * 0.35 + bestScore * 0.30) * 100) / 100,
      required_changes: [
        { name: "Kubernetes", difficulty: "Medium", score_gain: 5 },
        { name: "Terraform", difficulty: "Medium", score_gain: 3 },
        { name: "Production Deployment", difficulty: "Hard", score_gain: 6 }
      ],
      gap_analysis: {
        missing_skills: ["kubernetes", "terraform"],
        missing_experience_months: 8,
        missing_projects: ["production deployment", "microservice architecture"]
      },
      monte_carlo: {
        best_score: bestScore,
        average_score: Math.round((seed + bestScore) / 2),
        probability: 0.87
      },
      skills_counterfactual: {
        required_skills: ["Kubernetes", "Terraform"],
        score_gain: 9,
        future_rank: 1
      },
      experience_counterfactual: {
        required_months: 8,
        future_score: bestScore
      },
      project_counterfactual: {
        required_projects: ["Production Deployment", "Microservice Architecture"]
      },
      leadership_counterfactual: {
        mentor: 2,
        lead_projects: 1,
        future_leadership: 0.92
      },
      career_counterfactual: {
        best_path: futureRole,
        future_salary: seed > 90 ? "35 LPA" : "28 LPA",
        future_score: bestScore
      },
      salary_counterfactual: {
        salary_increase: "4 LPA"
      },
      retention_counterfactual: {
        best_strategy: "promotion",
        retention: 0.93
      },
      culture_counterfactual: {
        communication: 10,
        leadership: 7,
        culture_fit: 0.94
      },
      future_counterfactual: {
        "6_months": Math.round(seed + 3),
        "12_months": Math.round(seed + 6),
        "24_months": Math.round(seed + 8),
        "36_months": bestScore,
        "60_months": Math.min(100, bestScore + 1)
      },
      cost_estimation: {
        cost: "₹15,000",
        months: 6
      },
      debate: {
        agent_hire: `${cand.name || 'Candidate'} shows excellent baseline skills. The core competency is strong, trust index is high.`,
        agent_reject: `Candidate is currently missing critical requirements like Kubernetes and production deployment experience.`,
        agent_improve: `We should not reject this candidate. Instead, we can sponsor certification or upskilling. The cost is minimal.`,
        agent_future: `With the proposed upskilling plan, the candidate's score is projected to reach ${bestScore}%, which would rank them #1 within 6 months.`
      },
      explanation: `${cand.name || 'Candidate'} currently ranks #${cand.rank || 2} with a score of ${currentScore}%. Counterfactual analysis indicates that the candidate lacks:\n• Kubernetes\n• Production deployment experience\n\nSimulation results show that obtaining Kubernetes certification would increase their score to ${Math.round(seed + 5)}%. Adding one production deployment project would increase the score further. Completing both improvements would increase the score to ${bestScore}%, making the candidate rank #1.\n\nEstimated completion time: 6 months.\nEstimated cost: ₹15,000.\nSuccess probability: 87%.\nPredicted future role: ${futureRole}.`
    };
  };

  const getOrCreateRiskProfileData = (cand) => {
    if (cand.risk_profile) return cand.risk_profile;
    
    const seed = cand.score || 85;
    
    return {
      risk_score: Math.round(91.0 - (100 - seed) * 0.4),
      offer_acceptance: {
        accept_probability: 0.91,
        confidence: 0.88,
        risk: "LOW"
      },
      ghosting: {
        ghost_probability: 0.04,
        risk: "LOW"
      },
      joining: {
        joining_probability: 0.87
      },
      retention: {
        "3_months": 0.98,
        "6_months": 0.95,
        "12_months": 0.92,
        "24_months": 0.81,
        "60_months": 0.52
      },
      resignation: {
        resignation_probability: 0.12,
        expected_month: 34
      },
      switch: {
        switch_probability: 0.18
      },
      burnout: {
        burnout_probability: 0.09,
        severity: "LOW"
      },
      promotion: {
        promotion_probability: 0.84
      },
      leadership: {
        future_leader: 0.81
      },
      teamlead: {
        teamlead_probability: 0.79,
        expected_years: 2
      },
      manager: {
        manager_probability: 0.71,
        expected_years: 5
      },
      director: {
        director_probability: 0.42,
        expected_years: 10
      },
      salary: {
        salary_1: Math.round(seed * 0.2 + 10),
        salary_2: Math.round(seed * 0.25 + 12),
        salary_5: Math.round(seed * 0.4 + 18),
        salary_10: Math.round(seed * 0.8 + 24)
      },
      conflict: {
        conflict_probability: 0.07
      },
      survival: {
        survival_probability: 0.89
      },
      success: {
        success_probability: 0.90,
        classification: "TOP_TALENT"
      },
      career_timeline: {
        career_path: [
          { year: 2025, role: seed > 90 ? "Lead Systems Engineer" : "Senior Software Engineer" },
          { year: 2027, role: seed > 90 ? "Staff Architect" : "Technical Lead" },
          { year: 2029, role: seed > 90 ? "Director of Engineering" : "Engineering Manager" },
          { year: 2032, role: seed > 90 ? "VP of Technology" : "Director of Engineering" },
          { year: 2036, role: seed > 90 ? "CTO" : "VP of Engineering" }
        ]
      },
      monte_carlo_hiring: {
        success: 83,
        burnout: 5,
        resignation: 9,
        leadership: 71
      },
      explanation: `${cand.name || 'Candidate'} demonstrates strong ownership, excellent learning velocity, and high leadership potential. Risk analysis projects an offer acceptance of 91%, joining probability of 87%, and annual retention probability of 92%. The candidate has a 9% burnout risk and a 12% resignation probability. They show high potential for progression to Team Lead (79%) and Manager (71%) paths. The candidate is expected to remain with the organization for approximately 4.2 years and has a high probability of becoming a key leader.`
    };
  };

  const getOrCreateDebateData = (cand) => {
    if (cand.debate_committee) return cand.debate_committee;
    
    const seed = cand.score || 85;
    
    return {
      hire_agent: { decision: "HIRE", confidence: 0.91, arguments: ["Strong technical foundations", "Exceptional learning velocity"] },
      reject_agent: { decision: "REJECT", confidence: 0.83, arguments: ["Missing Kubernetes certification", "Short job tenures"] },
      risk_agent: { risk: 0.28, arguments: ["High stress vulnerability under workload shifts"] },
      future_agent: { future_role: seed > 90 ? "Engineering Manager" : "Technical Lead", promotion_probability: 0.84, leadership: 0.88 },
      culture_agent: { culture_fit: 0.91 },
      leadership_agent: { leadership: 0.86 },
      retention_agent: { retention: 0.89 },
      innovation_agent: { innovation_score: 0.82 },
      counterfactual_agent: { missing: ["Kubernetes", "Production deployment"], future_score: 98 },
      compensation_agent: { salary_fit: 0.88 },
      promotion_agent: { promotion: 0.81, manager: 0.71 },
      trust_agent: { trust: 0.93 },
      
      recruiter_agent: { opinion: "HIRE", accept_probability: 0.91, joining_probability: 0.87, arguments: ["Onboarding alignment is solid"] },
      em_agent: { opinion: "HIRE", execution_score: 0.85, arguments: ["Can scale backend microservices"] },
      hr_agent: { opinion: "HIRE", collaboration: 0.80, communication: 0.85, arguments: ["Culture alignment checks pass"] },
      ceo_agent: { opinion: "HIRE", ownership: 0.82, innovation: 0.88, arguments: ["Long-term value creation alignment"] },
      
      debate_rounds: [
        {
          round: 1,
          topic: "Initial Opinions",
          messages: [
            { agent: "Hire Agent", message: "Candidate shows outstanding coding foundations and rapid adaptiveness." },
            { agent: "Reject Agent", message: "Wait, the candidate lacks direct exposure to Kubernetes infrastructure setups." }
          ]
        },
        {
          round: 2,
          topic: "Rebuttals & Critiques",
          messages: [
            { agent: "Hire Agent", message: "Although Kubernetes is missing, the candidate's learning velocity is in the top 5%. They can upskill in 4 weeks." },
            { agent: "Reject Agent", message: "We have critical production deadlines next month. We cannot afford 4 weeks of basic training." }
          ]
        },
        {
          round: 3,
          topic: "Defensive Arguments",
          messages: [
            { agent: "Hire Agent", message: "The candidate has built scalable APIs in FastAPI and Python. This architectural grounding is far harder to hire than basic configs." },
            { agent: "Reject Agent", message: "True, but the lack of infrastructure ownership remains a concern for our lean DevOps team." }
          ]
        },
        {
          round: 4,
          topic: "Compromise & Consensus",
          messages: [
            { agent: "Hire Agent", message: "What if we offer a conditional hire where they complete a Kubernetes certification during onboarding?" },
            { agent: "Reject Agent", message: "A conditional offer with structured upskilling makes sense and offsets the delivery risk." }
          ]
        }
      ],
      negotiation: { hire_score: 93, reject_score: 72 },
      consensus: { decision: "HIRE", votes: { hire: 8, reject: 3, abstain: 1 }, consensus_percentage: 83 },
      judge: { decision: "HIRE", confidence: 0.88, reason: "Technical capability and rapid adaptability outweigh infrastructural delivery risks." },
      argument_graph: {
        nodes: [
          { id: "skills", label: "Technical Competence", value: 0.88 },
          { id: "learning", label: "Learning Velocity", value: 0.90 },
          { id: "leadership", label: "Leadership DNA", value: 0.86 },
          { id: "gaps", label: "Infrastructure Gaps", value: 0.65 },
          { id: "tenure", label: "Short Tenures", value: 0.70 }
        ],
        edges: [
          { source: "learning", target: "skills", type: "supports", weight: 0.80 },
          { source: "learning", target: "leadership", type: "supports", weight: 0.60 },
          { source: "tenure", target: "leadership", type: "opposes", weight: -0.40 },
          { source: "gaps", target: "skills", type: "opposes", weight: -0.50 }
        ]
      },
      debate_simulation: { hire: 82, reject: 18 },
      explanation: `${cand.name || 'Candidate'} was debated by 12 AI agents of the hiring committee.\n\nPositive Factors:\n✓ Core capabilities are strong\n✓ Leadership potential: 86%\n✓ High trust: 93%\n\nNegative Gaps:\n✗ Missing DevOps requirements: Kubernetes, Production deployment\n✗ Short tenure risk\n\nAfter 4 rounds of debate, the hiring committee voted:\n• HIRE: 8 votes\n• REJECT: 3 votes\n• ABSTAIN: 1 votes\n\nFinal Committee Decision: HIRE\nJudge Decision: HIRE (Confidence: 88%)\nReasoning: Technical capability and rapid adaptability outweigh infrastructural delivery risks.`
    };
  };

  const getOrCreateCareerForecastData = (cand) => {
    if (cand.career_forecast) return cand.career_forecast;
    
    const seed = cand.score || 85;
    
    return {
      velocity: { velocity: 0.82, classification: "FAST_GROWTH" },
      future_role: { next_role: "tech_lead", probability: 0.87, timeline: "18 months" },
      promotion: { promotion_probability: 0.84, expected_months: 18 },
      leadership: { current: 89, year_2: 91, year_5: 93, year_10: 95 },
      skills: { future_skills: ["kubernetes", "terraform", "architecture", "leadership", "business strategy"] },
      branches: {
        predictions: [
          { role: "Tech Lead", probability: 70 },
          { role: "Architect", probability: 20 },
          { role: "Manager", probability: 8 },
          { role: "Founder", probability: 2 }
        ]
      },
      salary: { salary_now: 18, salary_1: 22, salary_2: 27, salary_5: 40, salary_10: 85 },
      ceiling: { career_ceiling: "VP_ENGINEERING", confidence: 0.82 },
      executive: { executive_probability: 0.78 },
      founder: { founder_probability: 0.12 },
      plateau: { plateau: false, risk: 0.18 },
      risk: { burnout: 0.09, stagnation: 0.19, switching: 0.21 },
      timeline: {
        timeline: [
          { year: 2025, role: "Senior Engineer" },
          { year: 2027, role: "Tech Lead" },
          { year: 2030, role: "Engineering Manager" },
          { year: 2034, role: "Director" },
          { year: 2040, role: "VP Engineering" }
        ]
      },
      simulator: {
        startup: { years: 2, role: "Manager", milestone: "Attain manager status in 2 years due to fast pacing." },
        corporate: { years: 5, role: "Manager", milestone: "Attain structured Manager role in 5 years." },
        faang: { years: 4, role: "Staff Engineer", milestone: "Attain Staff Engineer level in 4 years." }
      },
      value: { current_value: 85, future_value: 97, business_value: 91 },
      monte_carlo: { manager: 62, director: 24, cto: 9, founder: 5 },
      explanation: `${cand.name || 'Candidate'} demonstrates:\n✓ High learning velocity and adaptable engineering skills.\n✓ Strong leadership growth trajectories.\n✓ Excellent vertical career progression.\n\nCareer Velocity: 0.82 levels/year\n\nPredicted Career Path:\n• 18 Months: Tech Lead\n• 4 Years: Engineering Manager\n• 7 Years: Director\n• 12 Years: VP Engineering\n\nLeadership Index: 89%\nPromotion Probability: 84%\nCareer Ceiling: VP Engineering\nFounder Probability: 12%\nExecutive Probability: 78%\nBurnout Risk: 9%\n\nThe candidate is projected to become a senior organizational leader within approximately 7 years.`
    };
  };

  const getOrCreateTeamCompatibilityData = (cand) => {
    if (cand.team_compatibility) return cand.team_compatibility;
    
    return {
      candidate_dna: {
        leadership: 0.34,
        communication: 0.92,
        collaboration: 0.89,
        mentoring: 0.88,
        innovation: 0.72,
        adaptability: 0.91
      },
      team_dna: {
        team_size: 6,
        backend: 3,
        frontend: 2,
        devops: 1,
        avg_experience: 7,
        leadership: 0.62,
        communication: 0.85,
        collaboration: 0.91,
        innovation: 0.73,
        mentoring: 0.68,
        risk_appetite: 0.41
      },
      org_dna: {
        organization: "startup",
        risk: 0.91,
        innovation: 0.93,
        ownership: 0.88,
        speed: 0.95
      },
      compatibility: { compatibility: 0.96 },
      communication: { communication_fit: 0.94 },
      collaboration: { collaboration: 0.91 },
      leadership: { leadership_balance: 0.91, leadership_conflict: 0.09 },
      conflict: { conflict_probability: 0.03 },
      diversity: { knowledge_diversity: 0.89, redundancy: 0.14 },
      mentorship: { mentor_score: 0.91 },
      productivity: { productivity_gain: 0.18 },
      innovation: { innovation_boost: 0.24 },
      burnout: { burnout_risk: 0.12 },
      social_graph: {
        nodes: [
          { id: "Alice", role: "Tech Lead", centrality: 0.85 },
          { id: "Bob", role: "Senior Developer", centrality: 0.72 },
          { id: "David", role: "QA Engineer", centrality: 0.50 },
          { id: "Emma", role: "Product Manager", centrality: 0.90 },
          { id: "Candidate", role: "Senior Engineer", centrality: 0.68 }
        ],
        edges: [
          { source: "Alice", target: "Bob", weight: 0.8 },
          { source: "Alice", target: "Emma", weight: 0.9 },
          { source: "Bob", target: "Candidate", weight: 0.75 },
          { source: "Emma", target: "Candidate", weight: 0.82 },
          { source: "David", target: "Bob", weight: 0.50 }
        ]
      },
      role: { future_team_role: "MENTOR" },
      simulation: {
        milestones: {
          month_1: "Candidate onboarding, initial toolset alignment.",
          month_3: "Peer-to-peer knowledge sharing and team flow integration.",
          month_6: "Productivity gains observed, active sprint contributions.",
          year_1: "Mentorship benefits established, coaching junior peers.",
          year_2: "Leadership style matures, potential transition into lead functions."
        },
        scenarios: {
          A: { label: "Hire Candidate A (Reliability focused)", outcome: "Productivity +18%" },
          B: { label: "Hire Candidate B (Innovation focused)", outcome: "Innovation +24%" },
          C: { label: "Hire Candidate C (Friction prone)", outcome: "Conflict +9%" }
        },
        metrics: {
          productivity: 1.18,
          innovation: 1.24,
          mentorship: 0.89
        }
      },
      monte_carlo: { success: 84, conflict: 9, burnout: 3, innovation: 71 },
      org_impact: { organization_value: 0.91 },
      explanation: `${cand.name || 'Candidate'} demonstrates:\n✓ Excellent communication capabilities.\n✓ Strong collaboration and peer support tendencies.\n✓ High mentoring capability and knowledge-sharing motivation.\n✓ Strong cultural fit within target company dimensions.\n✓ Significant knowledge diversity contributing cognitive variations.\n\nTeam Compatibility: 96%\nConflict Probability: 3%\nKnowledge Diversity: 89%\nLeadership Balance: 91%\nCollaboration: 94%\nMentorship: 91%\nProductivity Gain: 18%\nInnovation Gain: 24%\n\nPredicted Team Role: MENTOR\n\nThe candidate is expected to significantly improve team performance, innovation, knowledge sharing, and organizational productivity.`
    };
  };

  const getOrCreateSkillEvolutionData = (cand) => {
    if (cand.skill_evolution) return cand.skill_evolution;
    
    return {
      skills: { python: 72, aws: 42, docker: 61, leadership: 32 },
      timeline: {
        timeline: [
          { skill: "python", year: 2021 },
          { skill: "docker", year: 2022 },
          { skill: "aws", year: 2023 }
        ]
      },
      velocity: { learning_velocity: 3.4, category: "HIGH" },
      project_velocity: { project_velocity: 0.89 },
      github: { github_growth: 0.91, python_activity: 0.94, cloud_activity: 0.83 },
      certification: { future_path: "Cloud Architect" },
      dependency: { next_skill: "terraform" },
      growth: { python: 82, aws: 58 },
      future_skills: { future_skills: ["kubernetes", "terraform", "cloud_architecture"] },
      strengths: {
        python: { now: 72, m6: 79, m12: 87, m24: 96 },
        aws: { now: 42, m6: 58, m12: 73, m24: 91 },
        docker: { now: 61, m6: 72, m12: 84, m24: 93 },
        leadership: { now: 32, m6: 44, m12: 61, m24: 79 },
        architecture: { now: 18, m6: 29, m12: 47, m24: 81 }
      },
      obsolescence: { jquery: 0.87, php5: 0.92, angularjs: 0.83 },
      specialization: { specialization: "Platform Architect" },
      leadership: { leadership_now: 32, leadership_24m: 79 },
      career: { career_path: ["Senior Engineer", "Tech Lead", "Engineering Manager", "Director"] },
      twin: {
        startup: { label: "Scenario A: Join Startup", outcome: "Rapid skill diversity growth (+35%), learning velocity accelerates, broad tech stack exposure." },
        corporate: { label: "Scenario B: Join Corporate", outcome: "Structured leadership growth (+40%), process compliance specialization, governance skills focus." },
        research: { label: "Scenario C: Join Research", outcome: "Deep AI specialization (+45%), publication capability, specialized algorithmic engineering." }
      },
      monte_carlo: { cto: 18, architect: 44, manager: 29, founder: 9 },
      potential: { human_potential: 0.94 },
      confidence: 88,
      explanation: `${cand.name || 'Candidate'} demonstrates exceptionally high learning velocity.\n\nLearning Velocity: 3.4 skills/year\n\nCurrent Skills:\n• Python: 72\n• AWS: 42\n• Docker: 61\n\nPredicted Future Skills:\n• 6 Months: Kubernetes\n• 12 Months: Terraform\n• 24 Months: Cloud Architecture\n\nSkill Forecast:\n• Python: 72 → 96\n• AWS: 42 → 91\n• Leadership: 32 → 79\n\nSkill Obsolescence: Low\nFuture Growth: Very High\nCareer Prediction: Platform Architect\nLeadership Potential: High\nHuman Potential: 94%\n\nThe candidate demonstrates strong adaptability and is projected to become a senior technical leader.`
    };
  };

  const getOrCreateDigitalTwinData = (cand) => {
    if (cand.digital_twin) return cand.digital_twin;
    
    return {
      dna: { leadership: 0.42, communication: 0.91, learning: 0.94, innovation: 0.82, adaptability: 0.89 },
      behavior: { work_style: "collaborative", learning_style: "fast", risk: "moderate" },
      personality: { openness: 0.88, conscientiousness: 0.74, extroversion: 0.61 },
      learning: { learning_velocity: 3.4, future_growth: 0.91 },
      career: { timeline: [ { role: "Tech Lead", months: 18 }, { role: "Manager", months: 48 } ] },
      leadership: { today: 0.34, year2: 0.72, year5: 0.91 },
      retention: { retention_probability: 0.94 },
      resignation: { resignation_probability: 0.14 },
      burnout: { burnout_probability: 0.08 },
      promotion: { promotion_probability: 0.83 },
      innovation: { innovation_score: 0.88 },
      productivity: { productivity_score: 0.89 },
      mentorship: { mentor_probability: 0.92 },
      team_impact: { team_productivity: 1.18, team_innovation: 1.24 },
      organization_impact: { organization_value: 0.91 },
      simulation: {
        milestones: {
          month_1: "Rapid integration, alignment on local tooling ecosystem completed.",
          month_6: "Proving strong capability speed, introducing automation changes.",
          year_1: "Primary lead functions assigned, first major promotion recommendation.",
          year_2: "Leading cross functional initiatives, active developer mentoring.",
          year_5: "Transitioning to senior architecture and engineering directorship."
        },
        scenarios: {
          startup: { label: "Scenario A: Join Startup", outcome: "Innovation ↑, Leadership ↑, Burnout ↑ (+20%)" },
          corporate: { label: "Scenario B: Join Corporate", outcome: "Management ↑, Promotion ↑ (+25%)" },
          government: { label: "Scenario C: Join Government", outcome: "Stability +45%, Innovation ↓ (-20%)" }
        }
      },
      monte_carlo: { cto: 14, architect: 42, manager: 31, founder: 13 },
      explanation: `Candidate ${cand.name || 'Candidate'} demonstrates:\n✓ High learning ability\n✓ Strong leadership growth\n✓ Excellent communication\n✓ Strong mentoring ability\n\nCurrent Fit: 91%\nFuture Fit: 97%\nRetention: 94%\nPromotion: 83%\nLeadership: 91%\nInnovation: 88%\nBurnout: 8%\nResignation: 14%\n\nPredicted Career:\nSenior Engineer\n↓\nTech Lead\n↓\nEngineering Manager\n↓\nDirector\n\nPredicted Organizational Value: 91%\n\nThe candidate is projected to become a high-value organizational leader.`
    };
  };

  const dnaData = getOrCreateDnaData(candidate);
  const { candidate_dna, organization_dna, dna_match, team_compatibility, culture_failure, future_growth, personality } = dnaData;
  const cfData = getOrCreateCounterfactualData(candidate);
  const riskData = getOrCreateRiskProfileData(candidate);
  const debateData = getOrCreateDebateData(candidate);
  const careerData = getOrCreateCareerForecastData(candidate);
  const teamData = getOrCreateTeamCompatibilityData(candidate);
  const skillData = getOrCreateSkillEvolutionData(candidate);
  const twinSimData = getOrCreateDigitalTwinData(candidate);

  const currentFit = candidate.current_fit || candidate.score || 85;
  const futureScore = candidate.score || 88;

  const getBurnoutColor = (risk) => {
    if (risk === "HIGH") return "text-red-500 bg-red-500/10 border-red-500/20";
    if (risk === "MEDIUM") return "text-yellow-500 bg-yellow-500/10 border-yellow-500/20";
    return "text-green-500 bg-green-500/10 border-green-500/20";
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header Profile Summary */}
      <Card className="relative flex flex-col gap-6 overflow-hidden border-primary/20 bg-gradient-to-br from-card to-primary/5 lg:flex-row lg:items-center lg:justify-between">
        <div className="absolute right-0 top-0 h-40 w-40 bg-primary/10 blur-3xl rounded-full" />
        <div className="flex flex-col gap-5 sm:flex-row sm:items-center z-10">
          <ProgressRing value={futureScore} label="Org Fit" size={100} />
          <div>
            <Badge tone="blue" className="px-2.5 py-1 text-xs font-semibold tracking-wide">
              ORGANIZATIONAL DNA MATCHING ENGINE
            </Badge>
            <h2 className="mt-2 text-3xl font-extrabold tracking-tight">{candidate.name}</h2>
            <p className="mt-1 text-base font-semibold text-muted-foreground">
              {candidate.role} · <span className="text-primary">{candidate.company}</span>
            </p>
            <div className="mt-4 flex flex-wrap gap-4 text-xs text-muted-foreground">
              <span className="inline-flex items-center gap-1.5 bg-muted/60 px-2 py-1 rounded-md">
                <Briefcase size={13} /> {candidate.id}
              </span>
              <span className="inline-flex items-center gap-1.5 bg-muted/60 px-2 py-1 rounded-md">
                <MapPin size={13} /> {candidate.location}
              </span>
              <span className="inline-flex items-center gap-1.5 bg-muted/60 px-2 py-1 rounded-md">
                <ShieldCheck size={13} /> Profile Trust {candidate.trust || 85}%
              </span>
              <span className="inline-flex items-center gap-1.5 bg-muted/60 px-2 py-1 rounded-md">
                <Mail size={13} /> Active Recruitment Pipeline
              </span>
            </div>
          </div>
        </div>
        <Button onClick={() => window.print()} className="lg:self-center shrink-0 z-10 shadow-lg">
          <Download size={18} /> Export DNA Report
        </Button>
      </Card>

      {/* Main Alignment & Multi-Fit Panels */}
      <section className="grid gap-6 md:grid-cols-3">
        <Card className="flex flex-col items-center justify-center p-6 text-center border-blue-500/20 bg-blue-500/5">
          <ProgressRing value={currentFit} label="Skill Match" size={80} color="#3b82f6" />
          <p className="mt-3 text-sm font-semibold text-muted-foreground">Skill and role requirements matching (30% weight)</p>
        </Card>
        <Card className="flex flex-col items-center justify-center p-6 text-center border-emerald-500/20 bg-emerald-500/5">
          <ProgressRing value={Math.round(dna_match.organization_match * 100)} label="DNA Match" size={80} color="#10b981" />
          <p className="mt-3 text-sm font-semibold text-muted-foreground">Company culture alignment (25% weight)</p>
        </Card>
        <Card className="flex flex-col items-center justify-center p-6 text-center border-indigo-500/20 bg-indigo-500/5">
          <ProgressRing value={Math.round(team_compatibility.compatibility * 100)} label="Team Fit" size={80} color="#6366f1" />
          <p className="mt-3 text-sm font-semibold text-muted-foreground">Collaborative team compatibility (5% weight)</p>
        </Card>
      </section>

      {/* Workforce Persona Profile */}
      <Card className="border-teal-500/20 bg-gradient-to-r from-card to-teal-500/5">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h4 className="font-extrabold text-sm uppercase tracking-wider text-teal-400">Workforce Persona Profile</h4>
            <p className="text-sm text-muted-foreground mt-1">Identified personality personas and work archetypes</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Badge tone="green" className="text-xs py-1 px-3">Primary: {personality.primary}</Badge>
            <Badge tone="blue" className="text-xs py-1 px-3">Secondary: {personality.secondary}</Badge>
            <Badge tone="violet" className="text-xs py-1 px-3">Tertiary: {personality.tertiary}</Badge>
          </div>
        </div>
      </Card>


      {/* Part 23: Counterfactual Hiring AI Platform */}
      <section className="space-y-6">
        <Card className="border-pink-500/20 bg-gradient-to-br from-card to-pink-500/5 relative overflow-hidden">
          <div className="absolute right-0 top-0 h-40 w-40 bg-pink-500/10 blur-3xl rounded-full" />
          
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-muted pb-4">
            <div>
              <Badge tone="pink" className="px-2.5 py-1 text-xs font-semibold tracking-wide uppercase">
                Counterfactual Hiring AI Engine
              </Badge>
              <h3 className="mt-2 text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
                <Sparkles className="text-pink-400" /> Counterfactual Insights &amp; Optimal Growth Path
              </h3>
              <p className="text-sm text-muted-foreground mt-1">
                Simulating upskilling scenarios, career transitions, and leadership maturation to maximize potential.
              </p>
            </div>
            
            <div className="flex items-center gap-3">
              <div className="text-right">
                <span className="text-xs text-muted-foreground block font-medium">Composite Counterfactual Score</span>
                <span className="text-2xl font-extrabold text-pink-400">{cfData.composite_score || 91.5}%</span>
              </div>
            </div>
          </div>

          {/* Metrics Grid */}
          <div className="grid gap-4 md:grid-cols-4 mt-6">
            <div className="rounded-lg bg-muted/30 p-4 border border-muted/50 flex flex-col justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Rank Optimization</span>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-2xl font-extrabold text-white">#{cfData.current_rank} → #{cfData.future_rank}</span>
              </div>
              <span className="text-[10px] text-emerald-400 font-semibold mt-1">Rank Gap Closed</span>
            </div>
            
            <div className="rounded-lg bg-muted/30 p-4 border border-muted/50 flex flex-col justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Score Progression</span>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-2xl font-extrabold text-white">{currentFit}% → {cfData.monte_carlo.best_score}%</span>
              </div>
              <span className="text-[10px] text-pink-400 font-semibold mt-1">+{cfData.skills_counterfactual.score_gain || 9} points gain</span>
            </div>

            <div className="rounded-lg bg-muted/30 p-4 border border-muted/50 flex flex-col justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Cheapest Path Investment</span>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-2xl font-extrabold text-white">{cfData.cost_estimation.cost}</span>
              </div>
              <span className="text-[10px] text-muted-foreground mt-1">Duration: {cfData.cost_estimation.months} Months</span>
            </div>

            <div className="rounded-lg bg-muted/30 p-4 border border-muted/50 flex flex-col justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Success Likelihood</span>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-2xl font-extrabold text-white">{Math.round(cfData.probability * 100)}%</span>
              </div>
              <span className="text-[10px] text-muted-foreground mt-1">Based on learning capacity</span>
            </div>
          </div>

          {/* Skills & Projects gaps */}
          <div className="grid gap-6 md:grid-cols-2 mt-6 border-t border-muted pt-6">
            <div>
              <h4 className="font-extrabold text-sm uppercase text-pink-300 flex items-center gap-2 mb-3">
                <Zap size={15} /> Actionable Upskilling Requirements
              </h4>
              <div className="space-y-2">
                {cfData.required_changes.map((item, idx) => (
                  <div key={idx} className="flex items-center justify-between p-2.5 rounded bg-muted/20 border border-muted/30">
                    <div className="flex items-center gap-2">
                      <CheckCircle2 size={14} className="text-pink-400" />
                      <span className="text-sm font-semibold text-white">{item.name}</span>
                    </div>
                    <div className="flex items-center gap-2 text-xs">
                      <span className="px-2 py-0.5 rounded bg-pink-500/10 border border-pink-500/20 text-pink-400 font-bold">
                        +{item.score_gain} pts
                      </span>
                      <span className="px-2 py-0.5 rounded bg-muted text-muted-foreground font-semibold">
                        {item.difficulty}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-extrabold text-sm uppercase text-indigo-300 flex items-center gap-2 mb-3">
                <Briefcase size={15} /> Required Practical Domain Projects
              </h4>
              <div className="space-y-2">
                {cfData.project_counterfactual.required_projects.map((proj, idx) => (
                  <div key={idx} className="flex items-center gap-2 p-2.5 rounded bg-muted/20 border border-muted/30 text-sm font-semibold text-white">
                    <ArrowRight size={14} className="text-indigo-400" />
                    <span>{proj}</span>
                  </div>
                ))}
                <div className="flex items-center gap-2 p-2.5 rounded bg-muted/20 border border-muted/30 text-sm font-semibold text-white">
                  <Clock size={14} className="text-emerald-400" />
                  <span>Experience Required: <b className="text-emerald-400">+{cfData.experience_counterfactual.required_months} months</b> tenure growth</span>
                </div>
              </div>
            </div>
          </div>

          {/* Career, Retention & Leadership Projections */}
          <div className="grid gap-6 md:grid-cols-3 mt-6 border-t border-muted pt-6">
            <div className="rounded-lg bg-indigo-500/5 p-4 border border-indigo-500/10">
              <h5 className="text-xs font-bold uppercase text-indigo-400 mb-2">Career Trajectory</h5>
              <div className="space-y-1">
                <div className="text-sm font-extrabold text-white">{cfData.career_counterfactual.best_path}</div>
                <div className="text-xs text-muted-foreground mt-1">
                  Expected Compensation: <b className="text-white">{cfData.career_counterfactual.future_salary}</b>
                </div>
                <div className="text-[10px] text-indigo-300 font-semibold mt-1">
                  ({cfData.salary_counterfactual.salary_increase} Increase)
                </div>
              </div>
            </div>
            
            <div className="rounded-lg bg-emerald-500/5 p-4 border border-emerald-500/10">
              <h5 className="text-xs font-bold uppercase text-emerald-400 mb-2">Retention Intervention</h5>
              <div className="space-y-1">
                <div className="text-sm font-extrabold text-white uppercase">{cfData.retention_counterfactual.best_strategy} Strategy</div>
                <div className="text-xs text-muted-foreground mt-1">
                  Projected Retention Rate: <b className="text-white">{Math.round(cfData.retention_counterfactual.retention * 100)}%</b>
                </div>
                <div className="text-[10px] text-emerald-300 font-semibold mt-1">
                  (Culture Fit: {Math.round(cfData.culture_counterfactual.culture_fit * 100)}%)
                </div>
              </div>
            </div>

            <div className="rounded-lg bg-amber-500/5 p-4 border border-amber-500/10">
              <h5 className="text-xs font-bold uppercase text-amber-400 mb-2">Leadership Progression</h5>
              <div className="space-y-1">
                <div className="text-xs text-muted-foreground">
                  • Mentor <b className="text-white">{cfData.leadership_counterfactual.mentor}</b> junior engineers
                </div>
                <div className="text-xs text-muted-foreground mt-1">
                  • Lead <b className="text-white">{cfData.leadership_counterfactual.lead_projects}</b> key target initiatives
                </div>
                <div className="text-[10px] text-amber-300 font-semibold mt-1">
                  Projected Leadership Index: {Math.round(cfData.leadership_counterfactual.future_leadership * 100)}%
                </div>
              </div>
            </div>
          </div>

          {/* Timeline Projections */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-pink-300 mb-4">Counterfactual Score Timeline Progression</h4>
            <div className="grid grid-cols-5 gap-2 text-center">
              {[
                { label: "6 Months", val: cfData.future_counterfactual["6_months"] },
                { label: "12 Months", val: cfData.future_counterfactual["12_months"] },
                { label: "24 Months", val: cfData.future_counterfactual["24_months"] },
                { label: "36 Months", val: cfData.future_counterfactual["36_months"] },
                { label: "60 Months", val: cfData.future_counterfactual["60_months"] }
              ].map((step, idx) => (
                <div key={idx} className="rounded bg-muted/15 p-2.5 border border-muted/20 relative">
                  <div className="text-[10px] font-bold text-muted-foreground uppercase">{step.label}</div>
                  <div className="text-lg font-extrabold text-white mt-1">{step.val}%</div>
                  {idx < 4 && (
                    <div className="absolute top-1/2 -right-1.5 -translate-y-1/2 z-10 text-pink-500 hidden md:block">
                      →
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Multi-Agent debate */}
          <div className="grid gap-6 md:grid-cols-2 mt-6 border-t border-muted pt-6">
            <div>
              <h4 className="font-extrabold text-sm uppercase text-teal-300 flex items-center gap-2 mb-3">
                <Sparkles size={15} /> Multi-Agent Recruitment Debate Panel
              </h4>
              <div className="space-y-3 max-h-60 overflow-y-auto pr-2 text-xs">
                <div className="p-2.5 rounded bg-blue-500/10 border border-blue-500/20 text-blue-200">
                  <b className="text-white block mb-0.5">Agent A (Hire Advocate):</b>
                  "{cfData.debate.agent_hire}"
                </div>
                <div className="p-2.5 rounded bg-red-500/10 border border-red-500/20 text-red-200">
                  <b className="text-white block mb-0.5">Agent B (Risk / Reject):</b>
                  "{cfData.debate.agent_reject}"
                </div>
                <div className="p-2.5 rounded bg-purple-500/10 border border-purple-500/20 text-purple-200">
                  <b className="text-white block mb-0.5">Agent C (Improvement Facilitator):</b>
                  "{cfData.debate.agent_improve}"
                </div>
                <div className="p-2.5 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-200">
                  <b className="text-white block mb-0.5">Agent D (Future Predictor):</b>
                  "{cfData.debate.agent_future}"
                </div>
              </div>
            </div>

            <div>
              <h4 className="font-extrabold text-sm uppercase text-pink-300 flex items-center gap-2 mb-3">
                <Sparkles size={15} /> Recruiter AI Actionable Rationale
              </h4>
              <p className="text-xs leading-6 text-muted-foreground font-semibold bg-muted/20 border border-muted/30 p-4 rounded-lg h-52 overflow-y-auto whitespace-pre-line">
                {cfData.explanation}
              </p>
            </div>
          </div>
        </Card>
      </section>

      {/* Part 24: Hiring Risk Simulator & Workforce Outcome Prediction Engine */}
      <section className="space-y-6">
        <Card className="border-violet-500/20 bg-gradient-to-br from-card to-violet-500/5 relative overflow-hidden">
          <div className="absolute right-0 top-0 h-40 w-40 bg-violet-500/10 blur-3xl rounded-full" />
          
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-muted pb-4">
            <div>
              <Badge tone="violet" className="px-2.5 py-1 text-xs font-semibold tracking-wide uppercase">
                Workforce Outcome Prediction &amp; Risk Simulator
              </Badge>
              <h3 className="mt-2 text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
                <Sparkles className="text-violet-400" /> Hiring Risk Simulator &amp; Career Trajectory Forecasts
              </h3>
              <p className="text-sm text-muted-foreground mt-1">
                Simulating onboarding dynamics, post-hire integration, tenure risks, and executive growth likelihood.
              </p>
            </div>
            
            <div className="flex items-center gap-3">
              <div className="text-right">
                <span className="text-xs text-muted-foreground block font-medium">Outcome Potential Score</span>
                <span className="text-2xl font-extrabold text-violet-400">{riskData.risk_score || 91}/100</span>
              </div>
            </div>
          </div>

          {/* Primary Probability Row */}
          <div className="grid gap-4 md:grid-cols-4 mt-6">
            <div className="rounded-lg bg-muted/30 p-4 border border-muted/50 flex flex-col justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Offer Acceptance</span>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-2xl font-extrabold text-white">{Math.round(riskData.offer_acceptance.accept_probability * 100)}%</span>
              </div>
              <span className="text-[10px] text-emerald-400 font-semibold mt-1">Acceptance Risk: {riskData.offer_acceptance.risk}</span>
            </div>

            <div className="rounded-lg bg-muted/30 p-4 border border-muted/50 flex flex-col justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Ghosting Probability</span>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-2xl font-extrabold text-white">{Math.round(riskData.ghosting.ghost_probability * 100)}%</span>
              </div>
              <span className="text-[10px] text-emerald-400 font-semibold mt-1">Ghosting Risk: {riskData.ghosting.risk}</span>
            </div>

            <div className="rounded-lg bg-muted/30 p-4 border border-muted/50 flex flex-col justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Joining Probability</span>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-2xl font-extrabold text-white">{Math.round(riskData.joining.joining_probability * 100)}%</span>
              </div>
              <span className="text-[10px] text-muted-foreground mt-1">Expected onboarding success</span>
            </div>

            <div className="rounded-lg bg-muted/30 p-4 border border-muted/50 flex flex-col justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Culture Survival</span>
              <div className="mt-2 flex items-baseline gap-2">
                <span className="text-2xl font-extrabold text-white">{Math.round(riskData.survival.survival_probability * 100)}%</span>
              </div>
              <span className="text-[10px] text-muted-foreground mt-1">Past 12-month tenure projection</span>
            </div>
          </div>

          {/* Core Attrition & Team Friction Grid */}
          <div className="grid gap-6 md:grid-cols-2 mt-6 border-t border-muted pt-6">
            <div>
              <h4 className="font-extrabold text-sm uppercase text-violet-300 flex items-center gap-2 mb-3">
                <AlertTriangle size={15} /> Attrition &amp; Operational Risks
              </h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 rounded bg-muted/20 border border-muted/30">
                  <div>
                    <div className="text-sm font-semibold text-white">Resignation Probability</div>
                    <div className="text-[10px] text-muted-foreground">Likelihood of voluntary exit within 24 months</div>
                  </div>
                  <div className="text-right">
                    <span className="text-lg font-extrabold text-violet-400">{Math.round(riskData.resignation.resignation_probability * 100)}%</span>
                    <span className="text-[10px] text-muted-foreground block">Exit: Month {riskData.resignation.expected_month}</span>
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 rounded bg-muted/20 border border-muted/30">
                  <div>
                    <div className="text-sm font-semibold text-white">Burnout Risk Index</div>
                    <div className="text-[10px] text-muted-foreground">Workload and stress accumulation velocity</div>
                  </div>
                  <div className="text-right">
                    <span className="text-lg font-extrabold text-violet-400">{Math.round(riskData.burnout.burnout_probability * 100)}%</span>
                    <span className="text-[10px] text-muted-foreground block">Severity: {riskData.burnout.severity}</span>
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 rounded bg-muted/20 border border-muted/30">
                  <div>
                    <div className="text-sm font-semibold text-white">Job-Switch Likelihood</div>
                    <div className="text-[10px] text-muted-foreground">Propensity to seek alternative offers</div>
                  </div>
                  <div className="text-right">
                    <span className="text-lg font-extrabold text-violet-400">{Math.round(riskData.switch.switch_probability * 100)}%</span>
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 rounded bg-muted/20 border border-muted/30">
                  <div>
                    <div className="text-sm font-semibold text-white">Team Conflict friction</div>
                    <div className="text-[10px] text-muted-foreground">Interpersonal synergy and adaptation failures</div>
                  </div>
                  <div className="text-right">
                    <span className="text-lg font-extrabold text-violet-400">{Math.round(riskData.conflict.conflict_probability * 100)}%</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Leadership & Promotion Trajectory */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-emerald-300 flex items-center gap-2 mb-3">
                <TrendingUp size={15} /> Promotion &amp; Maturation Trajectory
              </h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 rounded bg-muted/20 border border-muted/30">
                  <div>
                    <div className="text-sm font-semibold text-white">Leadership Maturation Index</div>
                    <div className="text-[10px] text-muted-foreground">Potential to assume ownership of strategic initiatives</div>
                  </div>
                  <div className="text-right">
                    <span className="text-lg font-extrabold text-emerald-400">{Math.round(riskData.leadership.future_leader * 100)}%</span>
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 rounded bg-muted/20 border border-muted/30">
                  <div>
                    <div className="text-sm font-semibold text-white">Promotion Probability</div>
                    <div className="text-[10px] text-muted-foreground">Likelihood of vertical growth within 18 months</div>
                  </div>
                  <div className="text-right">
                    <span className="text-lg font-extrabold text-emerald-400">{Math.round(riskData.promotion.promotion_probability * 100)}%</span>
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 rounded bg-muted/20 border border-muted/30">
                  <div>
                    <div className="text-sm font-semibold text-white">Future Success Classification</div>
                    <div className="text-[10px] text-muted-foreground">Contribution level forecast</div>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-extrabold text-emerald-400 uppercase">{riskData.success.classification}</span>
                    <span className="text-[10px] text-muted-foreground block">Score: {Math.round(riskData.success.success_probability * 100)}%</span>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-2">
                  <div className="p-2 rounded bg-indigo-500/5 border border-indigo-500/10 text-center">
                    <span className="text-[10px] font-bold text-indigo-400 block uppercase">Team Lead</span>
                    <span className="text-sm font-extrabold text-white">{Math.round(riskData.teamlead.teamlead_probability * 100)}%</span>
                    <span className="text-[9px] text-muted-foreground block">~{riskData.teamlead.expected_years} Yrs</span>
                  </div>
                  <div className="p-2 rounded bg-amber-500/5 border border-amber-500/10 text-center">
                    <span className="text-[10px] font-bold text-amber-400 block uppercase">Manager</span>
                    <span className="text-sm font-extrabold text-white">{Math.round(riskData.manager.manager_probability * 100)}%</span>
                    <span className="text-[9px] text-muted-foreground block">~{riskData.manager.expected_years} Yrs</span>
                  </div>
                  <div className="p-2 rounded bg-pink-500/5 border border-pink-500/10 text-center">
                    <span className="text-[10px] font-bold text-pink-400 block uppercase">Director</span>
                    <span className="text-sm font-extrabold text-white">{Math.round(riskData.director.director_probability * 100)}%</span>
                    <span className="text-[9px] text-muted-foreground block">~{riskData.director.expected_years} Yrs</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Retention Milestones & Compensation Projections */}
          <div className="grid gap-6 md:grid-cols-2 mt-6 border-t border-muted pt-6">
            <div>
              <h4 className="font-extrabold text-sm uppercase text-violet-300 mb-3">Retention Projections Over Time</h4>
              <div className="grid grid-cols-5 gap-2 text-center">
                {[
                  { label: "3 Mth", val: riskData.retention["3_months"] },
                  { label: "6 Mth", val: riskData.retention["6_months"] },
                  { label: "12 Mth", val: riskData.retention["12_months"] },
                  { label: "24 Mth", val: riskData.retention["24_months"] },
                  { label: "60 Mth", val: riskData.retention["60_months"] }
                ].map((step, idx) => (
                  <div key={idx} className="rounded bg-muted/15 p-2 border border-muted/20">
                    <div className="text-[9px] font-bold text-muted-foreground uppercase">{step.label}</div>
                    <div className="text-sm font-extrabold text-white mt-1">{Math.round(step.val * 100)}%</div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h4 className="font-extrabold text-sm uppercase text-emerald-300 mb-3">Compensation Progression Forecast</h4>
              <div className="grid grid-cols-4 gap-2 text-center">
                {[
                  { label: "1 Year", val: riskData.salary.salary_1 },
                  { label: "2 Years", val: riskData.salary.salary_2 },
                  { label: "5 Years", val: riskData.salary.salary_5 },
                  { label: "10 Years", val: riskData.salary.salary_10 }
                ].map((step, idx) => (
                  <div key={idx} className="rounded bg-muted/15 p-2 border border-muted/20">
                    <div className="text-[9px] font-bold text-muted-foreground uppercase">{step.label}</div>
                    <div className="text-sm font-extrabold text-white mt-1">{step.val} LPA</div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Career Path Timeline (2025 - 2036) */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-violet-300 mb-4">Vertical Career Path Timeline Progression</h4>
            <div className="relative flex flex-col md:flex-row justify-between items-center gap-4">
              <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-muted/40 -translate-y-1/2 hidden md:block z-0" />
              {riskData.career_timeline.career_path.map((milestone, idx) => (
                <div key={idx} className="rounded bg-muted/20 p-3 border border-muted/40 z-10 w-full md:w-auto text-center md:min-w-[150px]">
                  <div className="text-xs font-bold text-violet-400">{milestone.year}</div>
                  <div className="text-xs font-extrabold text-white mt-1">{milestone.role}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Monte Carlo outcome probabilities & Explanation */}
          <div className="grid gap-6 md:grid-cols-2 mt-6 border-t border-muted pt-6">
            <div>
              <h4 className="font-extrabold text-sm uppercase text-teal-300 flex items-center gap-2 mb-3">
                <Sparkles size={15} /> 10,000 runs Monte Carlo post-hire simulator
              </h4>
              <div className="grid grid-cols-2 gap-4">
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <div className="text-xs font-bold text-muted-foreground uppercase">Upskilling Success</div>
                  <div className="text-2xl font-extrabold text-white mt-1">{riskData.monte_carlo_hiring.success}%</div>
                </div>
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <div className="text-xs font-bold text-muted-foreground uppercase">Burnout Events</div>
                  <div className="text-2xl font-extrabold text-white mt-1">{riskData.monte_carlo_hiring.burnout}%</div>
                </div>
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <div className="text-xs font-bold text-muted-foreground uppercase">Early Resignation</div>
                  <div className="text-2xl font-extrabold text-white mt-1">{riskData.monte_carlo_hiring.resignation}%</div>
                </div>
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <div className="text-xs font-bold text-muted-foreground uppercase">Leadership Maturation</div>
                  <div className="text-2xl font-extrabold text-white mt-1">{riskData.monte_carlo_hiring.leadership}%</div>
                </div>
              </div>
            </div>

            <div>
              <h4 className="font-extrabold text-sm uppercase text-violet-300 flex items-center gap-2 mb-3">
                <Sparkles size={15} /> Recruiter AI Risk Mitigation Narrative
              </h4>
              <p className="text-xs leading-6 text-muted-foreground font-semibold bg-muted/20 border border-muted/30 p-4 rounded-lg h-44 overflow-y-auto whitespace-pre-line">
                {riskData.explanation}
              </p>
            </div>
          </div>
        </Card>
      </section>

      {/* Part 25, 26: Multi-Agent AI Hiring Committee Board Simulator */}
      <section className="space-y-6">
        <Card className="border-amber-500/20 bg-gradient-to-br from-card to-amber-500/5 relative overflow-hidden">
          <div className="absolute right-0 top-0 h-40 w-40 bg-amber-500/10 blur-3xl rounded-full" />
          
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-muted pb-4">
            <div>
              <Badge tone="amber" className="px-2.5 py-1 text-xs font-semibold tracking-wide uppercase">
                Multi-Agent Systems &amp; Game Theory
              </Badge>
              <h3 className="mt-2 text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
                <Sparkles className="text-amber-400" /> Multi-Agent AI Hiring Committee Simulator
              </h3>
              <p className="text-sm text-muted-foreground mt-1">
                Twelve specialized AI agents debating organizational fit, competence, risks, and vertical growth potential.
              </p>
            </div>
            
            <div className="flex items-center gap-3">
              <div className="text-right">
                <span className="text-xs text-muted-foreground block font-medium">Final Voting Consensus</span>
                <span className="text-2xl font-extrabold text-amber-400">{debateData.consensus.consensus_percentage}% HIRE</span>
              </div>
            </div>
          </div>

          {/* Grid of 12 Specialized AI Committee Members */}
          <div className="mt-6">
            <h4 className="font-extrabold text-sm uppercase text-amber-300 mb-3">Hiring Board Members Assessment (12 Agents)</h4>
            <div className="grid gap-3 grid-cols-2 md:grid-cols-4 lg:grid-cols-6">
              
              <div className="p-3 rounded bg-muted/20 border border-muted/30 text-center">
                <span className="text-[10px] font-bold text-muted-foreground uppercase block">Hire Agent</span>
                <span className="text-xs font-extrabold text-white block mt-1 uppercase">{debateData.hire_agent.decision}</span>
                <span className="text-[9px] text-amber-400 font-semibold">Conf: {Math.round(debateData.hire_agent.confidence * 100)}%</span>
              </div>

              <div className="p-3 rounded bg-muted/20 border border-muted/30 text-center">
                <span className="text-[10px] font-bold text-muted-foreground uppercase block">Reject Agent</span>
                <span className="text-xs font-extrabold text-white block mt-1 uppercase">{debateData.reject_agent.decision}</span>
                <span className="text-[9px] text-red-400 font-semibold">Conf: {Math.round(debateData.reject_agent.confidence * 100)}%</span>
              </div>

              <div className="p-3 rounded bg-muted/20 border border-muted/30 text-center">
                <span className="text-[10px] font-bold text-muted-foreground uppercase block">Risk Agent</span>
                <span className="text-xs font-extrabold text-white block mt-1">{Math.round(debateData.risk_agent.risk * 100)}%</span>
                <span className="text-[9px] text-muted-foreground">General Risk</span>
              </div>

              <div className="p-3 rounded bg-muted/20 border border-muted/30 text-center">
                <span className="text-[10px] font-bold text-muted-foreground uppercase block">Culture Agent</span>
                <span className="text-xs font-extrabold text-white block mt-1">{Math.round(debateData.culture_agent.culture_fit * 100)}%</span>
                <span className="text-[9px] text-muted-foreground">DNA Match</span>
              </div>

              <div className="p-3 rounded bg-muted/20 border border-muted/30 text-center">
                <span className="text-[10px] font-bold text-muted-foreground uppercase block">Future Agent</span>
                <span className="text-xs font-extrabold text-white block mt-1 truncate">{debateData.future_agent.future_role}</span>
                <span className="text-[9px] text-muted-foreground">Progression Target</span>
              </div>

              <div className="p-3 rounded bg-muted/20 border border-muted/30 text-center">
                <span className="text-[10px] font-bold text-muted-foreground uppercase block">Leadership Agent</span>
                <span className="text-xs font-extrabold text-white block mt-1">{Math.round(debateData.leadership_agent.leadership * 100)}%</span>
                <span className="text-[9px] text-muted-foreground">Leader DNA</span>
              </div>

              <div className="p-3 rounded bg-muted/20 border border-muted/30 text-center">
                <span className="text-[10px] font-bold text-muted-foreground uppercase block">Retention Agent</span>
                <span className="text-xs font-extrabold text-white block mt-1">{Math.round(debateData.retention_agent.retention * 100)}%</span>
                <span className="text-[9px] text-muted-foreground">Tenure Stability</span>
              </div>

              <div className="p-3 rounded bg-muted/20 border border-muted/30 text-center">
                <span className="text-[10px] font-bold text-muted-foreground uppercase block">Innovation Agent</span>
                <span className="text-xs font-extrabold text-white block mt-1">{Math.round(debateData.innovation_agent.innovation_score * 100)}%</span>
                <span className="text-[9px] text-muted-foreground">Creativity Index</span>
              </div>

              <div className="p-3 rounded bg-muted/20 border border-muted/30 text-center">
                <span className="text-[10px] font-bold text-muted-foreground uppercase block">Trust Agent</span>
                <span className="text-xs font-extrabold text-white block mt-1">{Math.round(debateData.trust_agent.trust * 100)}%</span>
                <span className="text-[9px] text-muted-foreground">No Resume Fraud</span>
              </div>

              <div className="p-3 rounded bg-muted/20 border border-muted/30 text-center">
                <span className="text-[10px] font-bold text-muted-foreground uppercase block">Compensation</span>
                <span className="text-xs font-extrabold text-white block mt-1">{Math.round(debateData.compensation_agent.salary_fit * 100)}%</span>
                <span className="text-[9px] text-muted-foreground">Salary ROI Fit</span>
              </div>

              <div className="p-3 rounded bg-muted/20 border border-muted/30 text-center">
                <span className="text-[10px] font-bold text-muted-foreground uppercase block">Promotion Agent</span>
                <span className="text-xs font-extrabold text-white block mt-1">{Math.round(debateData.promotion_agent.promotion * 100)}%</span>
                <span className="text-[9px] text-muted-foreground">Advancement Index</span>
              </div>

              <div className="p-3 rounded bg-muted/20 border border-muted/30 text-center">
                <span className="text-[10px] font-bold text-muted-foreground uppercase block">Counterfactual</span>
                <span className="text-xs font-extrabold text-white block mt-1">98% Target</span>
                <span className="text-[9px] text-muted-foreground block truncate">Gaps: {debateData.counterfactual_agent.missing.length} items</span>
              </div>

            </div>
          </div>

          {/* Committee Organizational Perspectives (Recruiter, EM, HR, CEO) */}
          <div className="grid gap-4 md:grid-cols-4 mt-6 border-t border-muted pt-6">
            <div className="rounded-lg bg-indigo-500/5 p-4 border border-indigo-500/10">
              <h5 className="text-xs font-bold uppercase text-indigo-400 mb-2">Recruiter AI</h5>
              <div className="text-sm font-extrabold text-white uppercase">{debateData.recruiter_agent.opinion}</div>
              <div className="text-[10px] text-muted-foreground mt-1">
                Acceptance: <b>{Math.round(debateData.recruiter_agent.accept_probability * 100)}%</b>
              </div>
              <div className="text-[10px] text-muted-foreground">
                Joining: <b>{Math.round(debateData.recruiter_agent.joining_probability * 100)}%</b>
              </div>
            </div>

            <div className="rounded-lg bg-emerald-500/5 p-4 border border-emerald-500/10">
              <h5 className="text-xs font-bold uppercase text-emerald-400 mb-2">Engineering Manager AI</h5>
              <div className="text-sm font-extrabold text-white uppercase">{debateData.em_agent.opinion}</div>
              <div className="text-[10px] text-muted-foreground mt-1">
                Execution score: <b>{Math.round(debateData.em_agent.execution_score * 100)}%</b>
              </div>
              <div className="text-[10px] text-muted-foreground truncate">
                {debateData.em_agent.arguments[0]}
              </div>
            </div>

            <div className="rounded-lg bg-pink-500/5 p-4 border border-pink-500/10">
              <h5 className="text-xs font-bold uppercase text-pink-400 mb-2">HR Manager AI</h5>
              <div className="text-sm font-extrabold text-white uppercase">{debateData.hr_agent.opinion}</div>
              <div className="text-[10px] text-muted-foreground mt-1">
                Collaboration: <b>{Math.round(debateData.hr_agent.collaboration * 100)}%</b>
              </div>
              <div className="text-[10px] text-muted-foreground">
                Communication: <b>{Math.round(debateData.hr_agent.communication * 100)}%</b>
              </div>
            </div>

            <div className="rounded-lg bg-amber-500/5 p-4 border border-amber-500/10">
              <h5 className="text-xs font-bold uppercase text-amber-400 mb-2">CEO Executive AI</h5>
              <div className="text-sm font-extrabold text-white uppercase">{debateData.ceo_agent.opinion}</div>
              <div className="text-[10px] text-muted-foreground mt-1">
                Ownership: <b>{Math.round(debateData.ceo_agent.ownership * 100)}%</b>
              </div>
              <div className="text-[10px] text-muted-foreground">
                Innovation: <b>{Math.round(debateData.ceo_agent.innovation * 100)}%</b>
              </div>
            </div>
          </div>

          {/* Interactive Argument Graph visualization (Part 26) */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-amber-300 mb-4">Committee Argumentation Logic Graph Map</h4>
            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30 flex flex-col md:flex-row justify-around items-center gap-6">
              
              <div className="flex flex-col items-center p-3 rounded-lg bg-emerald-500/5 border border-emerald-500/20 text-center min-w-[140px]">
                <span className="text-xs font-extrabold text-white">{debateData.argument_graph.nodes[0].label}</span>
                <span className="text-[10px] text-emerald-400 font-bold mt-1">Score: {Math.round(debateData.argument_graph.nodes[0].value * 100)}%</span>
              </div>

              <div className="text-emerald-400 text-sm font-extrabold hidden md:block">
                ▲ supports (+0.80)
              </div>

              <div className="flex flex-col items-center p-3 rounded-lg bg-emerald-500/5 border border-emerald-500/20 text-center min-w-[140px]">
                <span className="text-xs font-extrabold text-white">{debateData.argument_graph.nodes[1].label}</span>
                <span className="text-[10px] text-emerald-400 font-bold mt-1">Score: {Math.round(debateData.argument_graph.nodes[1].value * 100)}%</span>
              </div>

              <div className="text-red-400 text-sm font-extrabold hidden md:block">
                ▼ opposes (-0.40)
              </div>

              <div className="flex flex-col items-center p-3 rounded-lg bg-red-500/5 border border-red-500/20 text-center min-w-[140px]">
                <span className="text-xs font-extrabold text-white">{debateData.argument_graph.nodes[4].label}</span>
                <span className="text-[10px] text-red-400 font-bold mt-1">Weight: {Math.round(debateData.argument_graph.nodes[4].value * 100)}%</span>
              </div>

            </div>
          </div>

          {/* Debate Timeline & Conversational Rounds */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-amber-300 mb-4">Committee Board Debate Transcript Timeline</h4>
            <div className="space-y-4 max-h-80 overflow-y-auto pr-2">
              {debateData.debate_rounds.map((roundData, idx) => (
                <div key={idx} className="p-4 rounded-lg bg-muted/15 border border-muted/20">
                  <div className="text-xs font-bold text-amber-400 uppercase mb-2">Round {roundData.round}: {roundData.topic}</div>
                  <div className="grid gap-3 md:grid-cols-2 text-xs">
                    {roundData.messages.map((msg, mIdx) => (
                      <div key={mIdx} className={`p-3 rounded border ${msg.agent.includes("Hire") ? "bg-emerald-500/5 border-emerald-500/10 text-emerald-100" : "bg-red-500/5 border-red-500/10 text-red-100"}`}>
                        <b className="block mb-1 text-white">{msg.agent}:</b>
                        "{msg.message}"
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Voting Consensus, Negotiation, Judge AI & Monte Carlo Simulator */}
          <div className="grid gap-6 md:grid-cols-3 mt-6 border-t border-muted pt-6">
            
            {/* Negotiation & Consensus Voting */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-indigo-300 flex items-center gap-2 mb-3">
                Consensus &amp; Negotiation Engine
              </h4>
              <div className="space-y-3 text-xs">
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <div className="text-muted-foreground uppercase font-bold text-[10px]">Negotiation Equilibrium</div>
                  <div className="flex justify-between items-center mt-2 font-extrabold text-white">
                    <span className="text-emerald-400">HIRE weight: {debateData.negotiation.hire_score}%</span>
                    <span className="text-red-400">REJECT weight: {debateData.negotiation.reject_score}%</span>
                  </div>
                </div>

                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <div className="text-muted-foreground uppercase font-bold text-[10px]">Board Committee Votes</div>
                  <div className="grid grid-cols-3 gap-2 text-center mt-2 font-extrabold text-white">
                    <div className="bg-emerald-500/10 border border-emerald-500/20 rounded p-1">
                      <span className="text-[9px] block text-emerald-400">HIRE</span>
                      {debateData.consensus.votes.hire}
                    </div>
                    <div className="bg-red-500/10 border border-red-500/20 rounded p-1">
                      <span className="text-[9px] block text-red-400">REJECT</span>
                      {debateData.consensus.votes.reject}
                    </div>
                    <div className="bg-muted/30 border border-muted/40 rounded p-1">
                      <span className="text-[9px] block text-muted-foreground">ABSTAIN</span>
                      {debateData.consensus.votes.abstain}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* 1,000 Committees Monte Carlo simulator */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-teal-300 flex items-center gap-2 mb-3">
                1,000 Committees Board Simulator
              </h4>
              <div className="space-y-3 text-xs">
                <div className="p-3 rounded bg-muted/20 border border-muted/30 text-center">
                  <div className="text-muted-foreground uppercase font-bold text-[10px] mb-2">Simulated Committees Approvals</div>
                  <div className="flex justify-around items-center font-extrabold text-xl">
                    <div className="text-emerald-400">
                      {debateData.debate_simulation.hire}%
                      <span className="text-[9px] block text-muted-foreground font-medium uppercase mt-0.5">Hire Prob</span>
                    </div>
                    <div className="text-red-400">
                      {debateData.debate_simulation.reject}%
                      <span className="text-[9px] block text-muted-foreground font-medium uppercase mt-0.5">Reject Prob</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Judge Decisive Arbitration */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-amber-300 flex items-center gap-2 mb-3">
                Judge AI Decisive Arbitration
              </h4>
              <div className="p-3.5 rounded-lg bg-amber-500/10 border border-amber-500/20 h-32 flex flex-col justify-between">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-extrabold text-white uppercase">Verdict: {debateData.judge.decision}</span>
                  <span className="text-xs font-extrabold text-amber-400">Confidence: {Math.round(debateData.judge.confidence * 100)}%</span>
                </div>
                <p className="text-[10px] italic leading-relaxed text-amber-100/90 mt-2">
                  "{debateData.judge.reason}"
                </p>
              </div>
            </div>

          </div>

          {/* Committee Explainability Rationale */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-amber-300 flex items-center gap-2 mb-3">
              <Sparkles size={15} /> Committee Natural Language Explainability
            </h4>
            <p className="text-xs leading-6 text-muted-foreground font-semibold bg-muted/20 border border-muted/30 p-4 rounded-lg h-48 overflow-y-auto whitespace-pre-line">
              {debateData.explanation}
            </p>
          </div>

        </Card>
      </section>



      {/* 6-Grid DNA Dimension Metrics */}
      <section className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {/* Metric 1: Learning Capacity */}
        <Card className="flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2 text-primary">
              <Zap size={18} />
              <h4 className="font-extrabold text-sm uppercase tracking-wider">Learning Velocity</h4>
            </div>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-white">
                {future_growth.adaptability_forecast === "High" ? "FAST" : "STEADY"}
              </span>
              <span className="text-sm font-medium text-muted-foreground">({Math.round(candidate_dna.learning * 100)}%)</span>
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-muted text-xs text-muted-foreground">
            Capacity for technical absorption: <b>{future_growth.adaptability_forecast}</b>
          </div>
        </Card>

        {/* Metric 2: Innovation Index */}
        <Card className="flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2 text-indigo-400">
              <TrendingUp size={18} />
              <h4 className="font-extrabold text-sm uppercase tracking-wider">Innovation Capacity</h4>
            </div>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-white">{Math.round(candidate_dna.innovation * 100)}%</span>
              <span className="text-xs font-semibold text-indigo-400">({future_growth.innovation_forecast})</span>
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-muted text-xs text-muted-foreground">
            Intellectual output &amp; creativity index: <b>{Math.round(candidate_dna.creativity * 100)}%</b>
          </div>
        </Card>

        {/* Metric 3: Leadership Trajectory */}
        <Card className="flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2 text-pink-400">
              <Sparkles size={18} />
              <h4 className="font-extrabold text-sm uppercase tracking-wider">Leadership Potential</h4>
            </div>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-white">{Math.round(candidate_dna.leadership * 100)}%</span>
              <span className="text-xs font-semibold text-pink-400">({future_growth.leadership_forecast})</span>
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-muted text-xs text-muted-foreground">
            Autonomy and ownership depth: <b>{Math.round(candidate_dna.autonomy * 100)}%</b>
          </div>
        </Card>

        {/* Metric 4: Communication Score */}
        <Card className="flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2 text-teal-400">
              <Users size={18} />
              <h4 className="font-extrabold text-sm uppercase tracking-wider">Communication &amp; Team</h4>
            </div>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-white">{Math.round(candidate_dna.communication * 100)}%</span>
              <span className="text-xs font-semibold text-teal-400">Collaboration: {Math.round(candidate_dna.collaboration * 100)}%</span>
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-muted text-xs text-muted-foreground">
            Team fit proxy: <b>{Math.round(candidate_dna.team * 100)}%</b>
          </div>
        </Card>

        {/* Metric 5: Retention Forecast */}
        <Card className="flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2 text-emerald-400">
              <Clock size={18} />
              <h4 className="font-extrabold text-sm uppercase tracking-wider">Stability Probability</h4>
            </div>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-white">{Math.round(candidate_dna.stability * 100)}%</span>
              <span className="text-xs font-semibold text-emerald-400">({future_growth.retention_forecast})</span>
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-muted text-xs text-muted-foreground">
            Risk tolerance coefficient: <b>{Math.round(candidate_dna.risk * 100)}%</b>
          </div>
        </Card>

        {/* Metric 6: Culture Risk */}
        <Card className="flex flex-col justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2 text-orange-400">
              <AlertTriangle size={18} />
              <h4 className="font-extrabold text-sm uppercase tracking-wider">Failure Forecast</h4>
            </div>
            <div className="mt-3 flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-white">{Math.round(culture_failure.culture_failure * 100)}%</span>
              <span className={`text-xs px-2 py-0.5 rounded-full border font-bold ${getBurnoutColor(culture_failure.risk)}`}>
                {culture_failure.risk} RISK
              </span>
            </div>
          </div>
          <div className="mt-4 pt-3 border-t border-muted text-xs text-muted-foreground">
            Culture mismatch factor: <b>{Math.round(culture_failure.culture_mismatch * 100)}%</b>
          </div>
        </Card>
      </section>

      {/* Future Growth Forecast & Dynamics */}
      <section className="grid gap-6 lg:grid-cols-2">
        {/* Culture Failure Risk Guard */}
        <Card className="flex flex-col justify-between border-red-500/20 bg-red-500/[0.02]">
          <div>
            <h3 className="mb-4 text-lg font-extrabold flex items-center gap-2 border-b border-red-500/10 pb-3 text-red-400">
              <AlertTriangle size={18} /> Culture Failure Risk Guard
            </h3>
            <div className="space-y-4 mt-6">
              <div>
                <div className="flex justify-between text-xs font-bold text-muted-foreground">
                  <span>Resignation Probability</span>
                  <span>{Math.round(culture_failure.resignation_risk * 100)}%</span>
                </div>
                <div className="h-2 rounded-full bg-muted mt-1.5">
                  <div className="h-2 rounded-full bg-red-500" style={{ width: `${culture_failure.resignation_risk * 100}%` }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs font-bold text-muted-foreground">
                  <span>Burnout Hazard</span>
                  <span>{Math.round(culture_failure.burnout_risk * 100)}%</span>
                </div>
                <div className="h-2 rounded-full bg-muted mt-1.5">
                  <div className="h-2 rounded-full bg-orange-500" style={{ width: `${culture_failure.burnout_risk * 100}%` }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs font-bold text-muted-foreground">
                  <span>Performance Degradation Hazard</span>
                  <span>{Math.round(culture_failure.performance_degradation * 100)}%</span>
                </div>
                <div className="h-2 rounded-full bg-muted mt-1.5">
                  <div className="h-2 rounded-full bg-yellow-500" style={{ width: `${culture_failure.performance_degradation * 100}%` }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs font-bold text-muted-foreground">
                  <span>Leadership Friction Hazard</span>
                  <span>{Math.round(culture_failure.leadership_mismatch * 100)}%</span>
                </div>
                <div className="h-2 rounded-full bg-muted mt-1.5">
                  <div className="h-2 rounded-full bg-pink-500" style={{ width: `${culture_failure.leadership_mismatch * 100}%` }} />
                </div>
              </div>
            </div>
          </div>
          <div className="mt-6 p-3 rounded-lg bg-red-500/5 text-xs text-red-400/90 leading-relaxed">
            * Warning parameters denote probability of friction or stagnation under corporate structural patterns.
          </div>
        </Card>

        {/* Future Adaptation Forecast */}
        <Card className="flex flex-col justify-between">
          <div>
            <h3 className="mb-4 text-lg font-extrabold flex items-center gap-2 border-b border-muted pb-3">
              <TrendingUp className="text-teal-400" /> Future Adaptation Timeline
            </h3>
            <div className="relative mt-6 pl-8 space-y-6">
              <div className="absolute left-3.5 top-2 bottom-2 w-0.5 bg-gradient-to-b from-primary via-indigo-500 to-emerald-500" />
              
              <div className="relative group">
                <div className="absolute -left-7 top-1 h-3.5 w-3.5 rounded-full bg-background border-2 border-primary" />
                <div className="flex flex-col">
                  <span className="text-sm font-extrabold text-primary">6 Months Forecast (Adaptation)</span>
                  <span className="text-base font-bold text-white mt-0.5">{Math.round(future_growth["6_months"] * 100)}% Success Probability</span>
                  <span className="text-xs text-muted-foreground mt-0.5">Adaptability trajectory: {future_growth.adaptability_forecast}</span>
                </div>
              </div>

              <div className="relative group">
                <div className="absolute -left-7 top-1 h-3.5 w-3.5 rounded-full bg-background border-2 border-indigo-400" />
                <div className="flex flex-col">
                  <span className="text-sm font-extrabold text-indigo-400">12 Months Forecast (Growth)</span>
                  <span className="text-base font-bold text-white mt-0.5">{Math.round(future_growth["12_months"] * 100)}% Success Probability</span>
                  <span className="text-xs text-muted-foreground mt-0.5">Projected Target Role: {future_growth.future_role}</span>
                </div>
              </div>

              <div className="relative group">
                <div className="absolute -left-7 top-1 h-3.5 w-3.5 rounded-full bg-background border-2 border-pink-400" />
                <div className="flex flex-col">
                  <span className="text-sm font-extrabold text-pink-400">24 Months Forecast (Progression)</span>
                  <span className="text-base font-bold text-white mt-0.5">{Math.round(future_growth["24_months"] * 100)}% Success Probability</span>
                  <span className="text-xs text-muted-foreground mt-0.5">Leadership readiness: {future_growth.leadership_forecast}</span>
                </div>
              </div>

              <div className="relative group">
                <div className="absolute -left-7 top-1 h-3.5 w-3.5 rounded-full bg-background border-2 border-emerald-400" />
                <div className="flex flex-col">
                  <span className="text-sm font-extrabold text-emerald-400">36 Months Forecast (Mastery)</span>
                  <span className="text-base font-bold text-white mt-0.5">{Math.round(future_growth["36_months"] * 100)}% Success Probability</span>
                  <span className="text-xs text-muted-foreground mt-0.5">Retention projection: {future_growth.retention_forecast}</span>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </section>

      {/* Explanations & Recruiter Insights */}
      <section className="grid gap-6 lg:grid-cols-2">
        {/* Rationale & Explainability */}
        <Card className="flex flex-col justify-between">
          <div>
            <h3 className="mb-4 text-lg font-extrabold flex items-center gap-2 border-b border-muted pb-3">
              <Sparkles className="text-yellow-400" /> AI Alignment Rationale
            </h3>
            <p className="text-base leading-8 text-muted-foreground font-medium">
              {candidate.reasoning || `Candidate demonstrates strong ownership, high innovation capability, excellent adaptability, and strong leadership growth. Organization DNA similarity is ${Math.round(dna_match.organization_match * 100)}%. The candidate exhibits a ${personality.primary}-${personality.secondary} personality profile, matching the company's culture. Predicted retention probability is ${Math.round(candidate_dna.stability * 100)}%. Future leadership potential is high, with an estimated promotion to ${future_growth.future_role} within 18 months. Culture failure risk remains low.`}
            </p>
          </div>
          <div className="mt-6 flex flex-wrap gap-2.5">
            {["High autonomy alignment", "Low risk tolerance mismatch", "High learning velocity match"].map((signal) => (
              <div key={signal} className="rounded-md border border-muted bg-muted/20 px-3 py-1.5 text-xs font-semibold text-white">
                ✓ {signal}
              </div>
            ))}
          </div>
        </Card>

        {/* Team Synergy Dynamics */}
        <Card className="flex flex-col justify-between border-violet-500/30 bg-violet-500/5">
          <div>
            <h3 className="mb-4 text-lg font-extrabold flex items-center gap-2 border-b border-violet-500/20 pb-3 text-violet-300">
              <CheckCircle2 className="text-violet-400" /> Team Compatibility Insights
            </h3>
            <p className="text-sm text-muted-foreground mb-4 font-semibold">
              Actionable compatibility details within the target team layout:
            </p>
            <div className="space-y-4 mt-4">
              <div className="flex items-center justify-between border-b border-violet-500/10 pb-2">
                <span className="text-sm font-medium text-muted-foreground">Collaborative Synergy</span>
                <span className="text-sm font-extrabold text-white">{Math.round(team_compatibility.synergy * 100)}%</span>
              </div>
              <div className="flex items-center justify-between border-b border-violet-500/10 pb-2">
                <span className="text-sm font-medium text-muted-foreground">Conflict Probability</span>
                <span className="text-sm font-extrabold text-white">{Math.round(team_compatibility.conflict_probability * 100)}%</span>
              </div>
              <div className="flex items-center justify-between border-b border-violet-500/10 pb-2">
                <span className="text-sm font-medium text-muted-foreground">Knowledge Diversity Tier</span>
                <span className="text-xs px-2 py-0.5 rounded bg-violet-500/20 border border-violet-500/30 font-bold text-white">
                  {team_compatibility.knowledge_diversity}
                </span>
              </div>
              <div className="flex items-center justify-between border-b border-violet-500/10 pb-2">
                <span className="text-sm font-medium text-muted-foreground">Personality Diversity Index</span>
                <span className="text-sm font-extrabold text-white">{Math.round(team_compatibility.personality_diversity * 100)}%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-muted-foreground">Innovation Contribution</span>
                <span className="text-sm font-extrabold text-white">{Math.round(team_compatibility.innovation_contribution * 100)}%</span>
              </div>
            </div>
          </div>
          <div className="mt-6 pt-4 border-t border-violet-500/10 flex items-center justify-between text-xs font-semibold text-violet-300">
            <span>Overall Team Compatibility Index</span>
            <span className="text-sm font-extrabold text-white">
              {Math.round(team_compatibility.compatibility * 100)}% Fit
            </span>
          </div>
        </Card>
      </section>

      {/* Organizational DNA Vector Matcher */}
      <Card>
        <h3 className="mb-6 text-lg font-extrabold flex items-center gap-2 border-b border-muted pb-3">
          <Users className="text-emerald-400" /> Organizational DNA Matcher (Target Profile: Corporate)
        </h3>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-5">
          {[
            { key: "speed", label: "Speed & Velocity", val: candidate_dna.speed, orgVal: organization_dna.speed },
            { key: "ownership", label: "Ownership / Autonomy", val: candidate_dna.ownership, orgVal: organization_dna.ownership },
            { key: "leadership", label: "Leadership Growth", val: candidate_dna.leadership, orgVal: organization_dna.leadership },
            { key: "innovation", label: "Innovation Capacity", val: candidate_dna.innovation, orgVal: organization_dna.innovation },
            { key: "learning", label: "Learning & Adapt", val: candidate_dna.learning, orgVal: organization_dna.learning },
            { key: "communication", label: "Communication Flow", val: candidate_dna.communication, orgVal: organization_dna.communication },
            { key: "risk", label: "Risk Appetite", val: candidate_dna.risk, orgVal: organization_dna.risk },
            { key: "stability", label: "Tenure Stability", val: candidate_dna.stability, orgVal: organization_dna.stability },
            { key: "collaboration", label: "Team Synergy", val: candidate_dna.collaboration, orgVal: organization_dna.collaboration },
            { key: "execution", label: "Task Execution", val: candidate_dna.execution, orgVal: organization_dna.execution }
          ].map(({ key, label, val, orgVal }) => {
            return (
              <div key={key} className="rounded-lg bg-muted/45 p-4 border border-muted/30">
                <div className="text-xs font-extrabold uppercase text-muted-foreground tracking-wider">{label}</div>
                <div className="mt-2 flex items-baseline justify-between">
                  <span className="text-2xl font-extrabold text-white">{Math.round(val * 100)}%</span>
                  <span className="text-xs text-emerald-400 font-semibold">
                    {Math.round((1 - Math.abs(val - orgVal)) * 100)}% Match
                  </span>
                </div>
                {/* Visual comparison slider */}
                <div className="mt-4 space-y-2">
                  <div>
                    <div className="flex justify-between text-[10px] text-muted-foreground"><span>Candidate</span><span>{Math.round(val * 100)}%</span></div>
                    <div className="h-1.5 rounded-full bg-muted"><div className="h-1.5 rounded-full bg-primary" style={{ width: `${val * 100}%` }} /></div>
                  </div>
                  <div>
                    <div className="flex justify-between text-[10px] text-muted-foreground"><span>Target Org</span><span>{Math.round(orgVal * 100)}%</span></div>
                    <div className="h-1.5 rounded-full bg-muted"><div className="h-1.5 rounded-full bg-emerald-500" style={{ width: `${orgVal * 100}%` }} /></div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </Card>

      {/* Part 23: Human Career Evolution Intelligence Dashboard */}
      <section className="space-y-6">
        <Card className="border-violet-500/20 bg-gradient-to-br from-card to-violet-500/5 relative overflow-hidden">
          <div className="absolute right-0 top-0 h-40 w-40 bg-violet-500/10 blur-3xl rounded-full" />
          
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-muted pb-4">
            <div>
              <Badge tone="violet" className="px-2.5 py-1 text-xs font-semibold tracking-wide uppercase">
                Predictive Workforce Analytics
              </Badge>
              <h3 className="mt-2 text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
                <Sparkles className="text-violet-400" /> Career Trajectory &amp; Human Evolution Forecast
              </h3>
              <p className="text-sm text-muted-foreground mt-1">
                Forecasting career trajectory, leadership maturation, skill evolution milestones, and long-term organizational impact.
              </p>
            </div>
            
            <div className="flex items-center gap-3">
              <div className="text-right">
                <span className="text-xs text-muted-foreground block font-medium">Future Capital Valuation</span>
                <span className="text-2xl font-extrabold text-violet-400">{careerData.value.future_value} / 100</span>
              </div>
            </div>
          </div>

          {/* Top Level Summary Metrics */}
          <div className="grid gap-4 grid-cols-2 md:grid-cols-4 mt-6">
            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Current Role</span>
              <span className="text-lg font-extrabold text-white block mt-1">Senior Engineer</span>
            </div>

            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Career Velocity</span>
              <span className="text-lg font-extrabold text-white block mt-1">{careerData.velocity.velocity} Levels/Yr</span>
              <span className="text-[10px] text-violet-400 font-semibold uppercase">{careerData.velocity.classification.replace('_', ' ')}</span>
            </div>

            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Career Ceiling</span>
              <span className="text-lg font-extrabold text-white block mt-1 truncate">{careerData.ceiling.career_ceiling.replace('_', ' ')}</span>
              <span className="text-[10px] text-muted-foreground block">Confidence: {Math.round(careerData.ceiling.confidence * 100)}%</span>
            </div>

            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Promotion Window</span>
              <span className="text-lg font-extrabold text-white block mt-1">~{careerData.promotion.expected_months} Months</span>
              <span className="text-[10px] text-emerald-400 font-semibold block">Prob: {Math.round(careerData.promotion.promotion_probability * 100)}%</span>
            </div>
          </div>

          {/* Leadership & Branching Probabilities */}
          <div className="grid gap-6 md:grid-cols-2 mt-6 border-t border-muted pt-6">
            
            {/* Career Branches */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-violet-300 mb-3">Alternative Path Branch Predictions</h4>
              <div className="space-y-2">
                {careerData.branches.predictions.map((branch, idx) => (
                  <div key={idx} className="flex justify-between items-center p-2.5 rounded bg-muted/15 border border-muted/20 text-xs">
                    <span className="font-bold text-white">{branch.role} Target</span>
                    <span className="font-extrabold text-violet-400">{branch.probability}% Prob</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Leadership & Risks */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-pink-300 mb-3">Leadership Maturation &amp; Long-term Risks</h4>
              <div className="grid grid-cols-2 gap-3 text-center text-xs">
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <span className="text-[10px] font-bold text-muted-foreground uppercase block">Leadership DNA</span>
                  <span className="text-xl font-extrabold text-white block mt-1">{careerData.leadership.current}%</span>
                </div>
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <span className="text-[10px] font-bold text-muted-foreground uppercase block">Executive Prob</span>
                  <span className="text-xl font-extrabold text-white block mt-1">{Math.round(careerData.executive.executive_probability * 100)}%</span>
                </div>
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <span className="text-[10px] font-bold text-muted-foreground uppercase block">Founder Prob</span>
                  <span className="text-xl font-extrabold text-white block mt-1">{Math.round(careerData.founder.founder_probability * 100)}%</span>
                </div>
                <div className="p-3 rounded bg-muted/20 border border-muted/30 text-center">
                  <span className="text-[10px] font-bold text-muted-foreground uppercase block">Burnout Risk</span>
                  <span className="text-xl font-extrabold text-red-400 block mt-1">{Math.round(careerData.risk.burnout * 100)}%</span>
                </div>
              </div>
            </div>

          </div>

          {/* Predicted Career Path timeline flow */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-violet-300 mb-4">Vertical Level Milestone Progression Path</h4>
            <div className="relative flex flex-col md:flex-row justify-between items-center gap-4">
              <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-muted/40 -translate-y-1/2 hidden md:block z-0" />
              {careerData.timeline.timeline.map((step, idx) => (
                <div key={idx} className="rounded bg-muted/20 p-3 border border-muted/40 z-10 w-full md:w-auto text-center md:min-w-[150px]">
                  <div className="text-xs font-bold text-violet-400">{step.year}</div>
                  <div className="text-xs font-extrabold text-white mt-1">{step.role}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Skill Evolution Timeline */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-emerald-300 mb-4">Forecasted Skill Acquisition Evolution Timeline</h4>
            <div className="grid gap-3 grid-cols-2 md:grid-cols-5 text-center text-xs">
              
              <div className="p-3 rounded bg-muted/25 border border-muted/30">
                <span className="text-[9px] font-bold text-muted-foreground uppercase block">1 Year</span>
                <span className="text-xs font-extrabold text-emerald-400 block mt-1">Kubernetes</span>
              </div>

              <div className="p-3 rounded bg-muted/25 border border-muted/30">
                <span className="text-[9px] font-bold text-muted-foreground uppercase block">2 Years</span>
                <span className="text-xs font-extrabold text-emerald-400 block mt-1">Terraform</span>
              </div>

              <div className="p-3 rounded bg-muted/25 border border-muted/30">
                <span className="text-[9px] font-bold text-muted-foreground uppercase block">4 Years</span>
                <span className="text-xs font-extrabold text-white block mt-1">Architecture</span>
              </div>

              <div className="p-3 rounded bg-muted/25 border border-muted/30">
                <span className="text-[9px] font-bold text-muted-foreground uppercase block">6 Years</span>
                <span className="text-xs font-extrabold text-white block mt-1">Leadership</span>
              </div>

              <div className="p-3 rounded bg-muted/25 border border-muted/30">
                <span className="text-[9px] font-bold text-muted-foreground uppercase block">8 Years</span>
                <span className="text-xs font-extrabold text-white block mt-1">Business Strategy</span>
              </div>

            </div>
          </div>

          {/* Compensation Growth Forecast & Monte Carlo Simulator */}
          <div className="grid gap-6 md:grid-cols-3 mt-6 border-t border-muted pt-6">
            
            {/* Compensation */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-violet-300 mb-3">Salary Evolution (LPA)</h4>
              <div className="grid grid-cols-5 gap-2 text-center text-xs">
                {[
                  { label: "Now", val: careerData.salary.salary_now },
                  { label: "1 Yr", val: careerData.salary.salary_1 },
                  { label: "2 Yr", val: careerData.salary.salary_2 },
                  { label: "5 Yr", val: careerData.salary.salary_5 },
                  { label: "10 Yr", val: careerData.salary.salary_10 }
                ].map((step, idx) => (
                  <div key={idx} className="rounded bg-muted/15 p-2 border border-muted/20">
                    <div className="text-[9px] font-bold text-muted-foreground uppercase">{step.label}</div>
                    <div className="text-xs font-extrabold text-white mt-1">{step.val}L</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Scenario simulator */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-indigo-300 mb-3">Company Tier Scenario Simulations</h4>
              <div className="space-y-2 text-[10px]">
                <div className="p-2 rounded bg-muted/20 border border-muted/30">
                  <span className="font-bold text-white block">Scenario 1: Startup Growth Path</span>
                  <span className="text-muted-foreground">{careerData.simulator.startup.milestone}</span>
                </div>
                <div className="p-2 rounded bg-muted/20 border border-muted/30">
                  <span className="font-bold text-white block">Scenario 2: Corporate Path</span>
                  <span className="text-muted-foreground">{careerData.simulator.corporate.milestone}</span>
                </div>
                <div className="p-2 rounded bg-muted/20 border border-muted/30">
                  <span className="font-bold text-white block">Scenario 3: FAANG Progression</span>
                  <span className="text-muted-foreground">{careerData.simulator.faang.milestone}</span>
                </div>
              </div>
            </div>

            {/* 10,000 runs Monte Carlo simulator */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-teal-300 mb-3">10,000 Runs Career Ceiling Simulator</h4>
              <div className="p-3 rounded-lg bg-muted/20 border border-muted/30 text-center text-xs">
                <div className="grid grid-cols-2 gap-3 font-extrabold">
                  <div className="p-2 bg-muted/15 border border-muted/20 rounded">
                    <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">Manager</span>
                    {careerData.monte_carlo.manager}%
                  </div>
                  <div className="p-2 bg-muted/15 border border-muted/20 rounded">
                    <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">Director</span>
                    {careerData.monte_carlo.director}%
                  </div>
                  <div className="p-2 bg-muted/15 border border-muted/20 rounded">
                    <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">CTO</span>
                    {careerData.monte_carlo.cto}%
                  </div>
                  <div className="p-2 bg-muted/15 border border-muted/20 rounded">
                    <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">Founder</span>
                    {careerData.monte_carlo.founder}%
                  </div>
                </div>
              </div>
            </div>

          </div>

          {/* Explainability Narrative */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-violet-300 flex items-center gap-2 mb-3">
              <Sparkles size={15} /> Career Evolution Explanation &amp; Rationale
            </h4>
            <p className="text-xs leading-6 text-muted-foreground font-semibold bg-muted/20 border border-muted/30 p-4 rounded-lg h-44 overflow-y-auto whitespace-pre-line">
              {careerData.explanation}
            </p>
          </div>

        </Card>
      </section>

      {/* Part 24: Team Compatibility & Organizational Human Simulator Dashboard */}
      <section className="space-y-6">
        <Card className="border-pink-500/20 bg-gradient-to-br from-card to-pink-500/5 relative overflow-hidden">
          <div className="absolute right-0 top-0 h-40 w-40 bg-pink-500/10 blur-3xl rounded-full" />
          
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-muted pb-4">
            <div>
              <Badge tone="pink" className="px-2.5 py-1 text-xs font-semibold tracking-wide uppercase">
                Organizational Human Simulator
              </Badge>
              <h3 className="mt-2 text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
                <Sparkles className="text-pink-400" /> Team Compatibility &amp; Synergy Simulator
              </h3>
              <p className="text-sm text-muted-foreground mt-1">
                Simulating how a candidate interacts with teams, impacts productivity, affects conflicts, and contributes to knowledge diversity.
              </p>
            </div>
            
            <div className="flex items-center gap-3">
              <div className="text-right">
                <span className="text-xs text-muted-foreground block font-medium">Organizational Synergy Value</span>
                <span className="text-2xl font-extrabold text-pink-400">
                  {Math.round(teamData.org_impact.organization_value * 100)}%
                </span>
              </div>
            </div>
          </div>

          {/* Core Compatibility Indices */}
          <div className="grid gap-4 grid-cols-2 md:grid-cols-4 mt-6">
            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Team Compatibility</span>
              <span className="text-2xl font-extrabold text-white block mt-1">
                {Math.round(teamData.compatibility.compatibility * 100)}%
              </span>
              <span className="text-[10px] text-pink-400 font-semibold uppercase">High Compatibility</span>
            </div>

            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Conflict Probability</span>
              <span className="text-2xl font-extrabold text-white block mt-1">
                {Math.round(teamData.conflict.conflict_probability * 100)}%
              </span>
              <span className="text-[10px] text-emerald-400 font-semibold uppercase">Low Friction Risk</span>
            </div>

            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Knowledge Diversity</span>
              <span className="text-2xl font-extrabold text-white block mt-1">
                {Math.round(teamData.diversity.knowledge_diversity * 100)}%
              </span>
              <span className="text-[10px] text-muted-foreground block">Redundancy: {Math.round(teamData.diversity.redundancy * 100)}%</span>
            </div>

            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Leadership Style Balance</span>
              <span className="text-2xl font-extrabold text-white block mt-1">
                {Math.round(teamData.leadership.leadership_balance * 100)}%
              </span>
              <span className="text-[10px] text-pink-400 font-semibold block">Friction: {Math.round(teamData.leadership.leadership_conflict * 100)}%</span>
            </div>
          </div>

          {/* Social graph and metrics */}
          <div className="grid gap-6 md:grid-cols-2 mt-6 border-t border-muted pt-6">
            
            {/* Core Synergy Scores */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-pink-300 mb-3">Team Synergy Indicators</h4>
              <div className="grid grid-cols-2 gap-3 text-center text-xs">
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <span className="text-[10px] font-bold text-muted-foreground uppercase block">Collaboration Fit</span>
                  <span className="text-xl font-extrabold text-white block mt-1">{Math.round(teamData.collaboration.collaboration * 100)}%</span>
                </div>
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <span className="text-[10px] font-bold text-muted-foreground uppercase block">Mentorship Score</span>
                  <span className="text-xl font-extrabold text-white block mt-1">{Math.round(teamData.mentorship.mentor_score * 100)}%</span>
                </div>
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <span className="text-[10px] font-bold text-muted-foreground uppercase block">Productivity Gain</span>
                  <span className="text-xl font-extrabold text-emerald-400 block mt-1">+{Math.round(teamData.productivity.productivity_gain * 100)}%</span>
                </div>
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <span className="text-[10px] font-bold text-muted-foreground uppercase block">Innovation Boost</span>
                  <span className="text-xl font-extrabold text-pink-400 block mt-1">+{Math.round(teamData.innovation.innovation_boost * 100)}%</span>
                </div>
              </div>
            </div>

            {/* Simulated Team Roles */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-violet-300 mb-3">Future Team Role Archetype</h4>
              <div className="p-4 rounded bg-muted/20 border border-muted/30 h-32 flex flex-col justify-center items-center">
                <span className="text-[10px] text-muted-foreground uppercase font-bold tracking-wider">Primary Predicted Role</span>
                <span className="text-3xl font-black text-white mt-1 uppercase tracking-widest">{teamData.role.future_team_role}</span>
                <span className="text-[10px] text-pink-400 mt-2 font-semibold">Active Mentor &amp; Collaborator Archetype</span>
              </div>
            </div>

          </div>

          {/* Social Graph flow representation */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-pink-300 mb-3">Simulated Team Interaction Network (Social Graph Centrality)</h4>
            <div className="grid gap-3 grid-cols-2 md:grid-cols-5 text-center text-xs">
              {teamData.social_graph.nodes.map((node, idx) => (
                <div key={idx} className={`p-3 rounded border ${node.id === "Candidate" ? "border-pink-500 bg-pink-500/10 text-white font-extrabold" : "border-muted/30 bg-muted/20 text-muted-foreground"}`}>
                  <div className="font-bold">{node.id}</div>
                  <div className="text-[9px] mt-0.5">{node.role}</div>
                  <div className={`text-[10px] mt-2 font-semibold ${node.id === "Candidate" ? "text-pink-400" : "text-white"}`}>
                    Centrality: {Math.round(node.centrality * 100)}%
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Timeline and scenarios */}
          <div className="grid gap-6 md:grid-cols-3 mt-6 border-t border-muted pt-6">
            
            {/* Onboarding Timeline */}
            <div className="md:col-span-2">
              <h4 className="font-extrabold text-sm uppercase text-pink-300 mb-3">Onboarding &amp; Integration Milestones</h4>
              <div className="space-y-2 text-xs">
                <div className="flex gap-3 items-start p-2 rounded bg-muted/15 border border-muted/20">
                  <span className="px-2 py-0.5 rounded bg-pink-500/20 text-pink-400 font-extrabold">M1</span>
                  <span className="text-white">{teamData.simulation.milestones.month_1}</span>
                </div>
                <div className="flex gap-3 items-start p-2 rounded bg-muted/15 border border-muted/20">
                  <span className="px-2 py-0.5 rounded bg-pink-500/20 text-pink-400 font-extrabold">M3</span>
                  <span className="text-white">{teamData.simulation.milestones.month_3}</span>
                </div>
                <div className="flex gap-3 items-start p-2 rounded bg-muted/15 border border-muted/20">
                  <span className="px-2 py-0.5 rounded bg-pink-500/20 text-pink-400 font-extrabold">M6</span>
                  <span className="text-white">{teamData.simulation.milestones.month_6}</span>
                </div>
                <div className="flex gap-3 items-start p-2 rounded bg-muted/15 border border-muted/20">
                  <span className="px-2 py-0.5 rounded bg-pink-500/20 text-pink-400 font-extrabold">Y1</span>
                  <span className="text-white">{teamData.simulation.milestones.year_1}</span>
                </div>
              </div>
            </div>

            {/* Monte Carlo Results */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-teal-300 mb-3">10,000 Runs Team Twin Monte Carlo</h4>
              <div className="p-3 rounded-lg bg-muted/20 border border-muted/30 text-center text-xs">
                <div className="grid grid-cols-2 gap-3 font-extrabold">
                  <div className="p-2 bg-muted/15 border border-muted/20 rounded">
                    <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">Success Rate</span>
                    {teamData.monte_carlo.success}%
                  </div>
                  <div className="p-2 bg-muted/15 border border-muted/20 rounded text-red-400">
                    <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">Friction</span>
                    {teamData.monte_carlo.conflict}%
                  </div>
                  <div className="p-2 bg-muted/15 border border-muted/20 rounded text-yellow-400">
                    <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">Burnout</span>
                    {teamData.monte_carlo.burnout}%
                  </div>
                  <div className="p-2 bg-muted/15 border border-muted/20 rounded text-pink-400">
                    <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">Innovation</span>
                    {teamData.monte_carlo.innovation}%
                  </div>
                </div>
              </div>
            </div>

          </div>

          {/* Explainability Narrative */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-pink-300 flex items-center gap-2 mb-3">
              <Sparkles size={15} /> Team Integration Explanation &amp; Rationale
            </h4>
            <p className="text-xs leading-6 text-muted-foreground font-semibold bg-muted/20 border border-muted/30 p-4 rounded-lg h-44 overflow-y-auto whitespace-pre-line">
              {teamData.explanation}
            </p>
          </div>

        </Card>
      </section>

      {/* Part 25: Skill Evolution & Human Potential Prediction Engine Dashboard */}
      <section className="space-y-6">
        <Card className="border-teal-500/20 bg-gradient-to-br from-card to-teal-500/5 relative overflow-hidden">
          <div className="absolute right-0 top-0 h-40 w-40 bg-teal-500/10 blur-3xl rounded-full" />
          
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-muted pb-4">
            <div>
              <Badge tone="teal" className="px-2.5 py-1 text-xs font-semibold tracking-wide uppercase">
                Human Potential Simulator
              </Badge>
              <h3 className="mt-2 text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
                <Sparkles className="text-teal-400" /> Skill Evolution Graph &amp; Potential Forecaster
              </h3>
              <p className="text-sm text-muted-foreground mt-1">
                Predicting learning velocities, next logical skill dependency tracks, obsolete risks, and multi-year competencies.
              </p>
            </div>
            
            <div className="flex items-center gap-3">
              <div className="text-right">
                <span className="text-xs text-muted-foreground block font-medium">Growth Confidence Rate</span>
                <span className="text-2xl font-extrabold text-teal-400">
                  {skillData.confidence}%
                </span>
              </div>
            </div>
          </div>

          {/* Top Metric Cards */}
          <div className="grid gap-4 grid-cols-2 md:grid-cols-4 mt-6">
            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Human Potential Score</span>
              <span className="text-2xl font-extrabold text-white block mt-1">
                {Math.round(skillData.potential.human_potential * 100)}%
              </span>
              <span className="text-[10px] text-teal-400 font-semibold uppercase">Exceptional Potential</span>
            </div>

            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Learning Velocity</span>
              <span className="text-2xl font-extrabold text-white block mt-1">
                {skillData.velocity.learning_velocity}
              </span>
              <span className="text-[10px] text-emerald-400 font-semibold uppercase">
                {skillData.velocity.category} (skills/year)
              </span>
            </div>

            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Skill Obsolescence Risk</span>
              <span className="text-2xl font-extrabold text-white block mt-1">
                LOW
              </span>
              <span className="text-[10px] text-muted-foreground block">Automation threat minimized</span>
            </div>

            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Career specialism</span>
              <span className="text-2xl font-extrabold text-white block mt-1 text-teal-300 truncate">
                {skillData.specialization.specialization}
              </span>
              <span className="text-[10px] text-teal-400 font-semibold block">Primary specialization pathway</span>
            </div>
          </div>

          {/* Skill Strength Forecast Table */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-teal-300 mb-3">Multi-Year Competency Growth Timeline</h4>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-muted text-muted-foreground font-bold">
                    <th className="py-2">Skill / Competency</th>
                    <th className="py-2 text-center">NOW</th>
                    <th className="py-2 text-center">6 Months</th>
                    <th className="py-2 text-center">12 Months</th>
                    <th className="py-2 text-center">24 Months</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-muted/10 font-medium">
                  {[
                    { name: "Python Coding Capability", key: "python" },
                    { name: "AWS Cloud Infrastructure", key: "aws" },
                    { name: "Docker Containerization", key: "docker" },
                    { name: "Organizational Leadership", key: "leadership" },
                    { name: "Platform Architecture Design", key: "architecture" }
                  ].map((row, idx) => {
                    const forecast = skillData.strengths[row.key];
                    return (
                      <tr key={idx} className="hover:bg-muted/5">
                        <td className="py-3 text-white font-extrabold">{row.name}</td>
                        <td className="py-3 text-center text-muted-foreground">{forecast?.now}</td>
                        <td className="py-3 text-center text-teal-400 font-bold">{forecast?.m6}</td>
                        <td className="py-3 text-center text-teal-400 font-bold">{forecast?.m12}</td>
                        <td className="py-3 text-center text-white font-black">{forecast?.m24}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Dependency path tree */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-teal-300 mb-3">Skill Dependency &amp; Knowledge Graph Transitions</h4>
            <div className="grid gap-4 md:grid-cols-2 text-xs">
              
              {/* Technical branch */}
              <div className="p-3 rounded-lg bg-muted/20 border border-muted/30">
                <span className="text-[10px] text-muted-foreground font-bold uppercase block mb-3">AI / ML Specialization path</span>
                <div className="flex flex-wrap items-center gap-2 font-bold">
                  <span className="p-1.5 rounded bg-muted/35 text-white">Python</span>
                  <span className="text-teal-400">→</span>
                  <span className="p-1.5 rounded bg-muted/35 text-white">Machine Learning</span>
                  <span className="text-teal-400">→</span>
                  <span className="p-1.5 rounded bg-muted/35 text-white">Deep Learning</span>
                  <span className="text-teal-400">→</span>
                  <span className="p-1.5 rounded bg-teal-500/20 text-teal-300">LLM Engineering</span>
                </div>
              </div>

              {/* Infrastructure branch */}
              <div className="p-3 rounded-lg bg-muted/20 border border-muted/30">
                <span className="text-[10px] text-muted-foreground font-bold uppercase block mb-3">Platform Specialization path</span>
                <div className="flex flex-wrap items-center gap-2 font-bold">
                  <span className="p-1.5 rounded bg-muted/35 text-white">Backend</span>
                  <span className="text-teal-400">→</span>
                  <span className="p-1.5 rounded bg-muted/35 text-white">Cloud (AWS)</span>
                  <span className="text-teal-400">→</span>
                  <span className="p-1.5 rounded bg-muted/35 text-white">Kubernetes</span>
                  <span className="text-teal-400">→</span>
                  <span className="p-1.5 rounded bg-teal-500/20 text-teal-300">Platform Architect</span>
                </div>
              </div>

            </div>
          </div>

          {/* Timeline and scenarios */}
          <div className="grid gap-6 md:grid-cols-3 mt-6 border-t border-muted pt-6">
            
            {/* Scenarios */}
            <div className="md:col-span-2">
              <h4 className="font-extrabold text-sm uppercase text-teal-300 mb-3">Twin Scenario Simulations</h4>
              <div className="space-y-2 text-xs">
                <div className="p-2.5 rounded bg-muted/15 border border-muted/20">
                  <span className="font-extrabold text-white block">{skillData.twin.startup.label}</span>
                  <span className="text-muted-foreground block mt-1">{skillData.twin.startup.outcome}</span>
                </div>
                <div className="p-2.5 rounded bg-muted/15 border border-muted/20">
                  <span className="font-extrabold text-white block">{skillData.twin.corporate.label}</span>
                  <span className="text-muted-foreground block mt-1">{skillData.twin.corporate.outcome}</span>
                </div>
                <div className="p-2.5 rounded bg-muted/15 border border-muted/20">
                  <span className="font-extrabold text-white block">{skillData.twin.research.label}</span>
                  <span className="text-muted-foreground block mt-1">{skillData.twin.research.outcome}</span>
                </div>
              </div>
            </div>

            {/* Monte Carlo Results */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-teal-300 mb-3">10,000 Runs Potential Monte Carlo</h4>
              <div className="p-3 rounded-lg bg-muted/20 border border-muted/30 text-center text-xs">
                <div className="grid grid-cols-2 gap-3 font-extrabold">
                  <div className="p-2 bg-muted/15 border border-muted/20 rounded text-teal-400">
                    <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">CTO Tier</span>
                    {skillData.monte_carlo.cto}%
                  </div>
                  <div className="p-2 bg-muted/15 border border-muted/20 rounded">
                    <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">Architect</span>
                    {skillData.monte_carlo.architect}%
                  </div>
                  <div className="p-2 bg-muted/15 border border-muted/20 rounded">
                    <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">Manager</span>
                    {skillData.monte_carlo.manager}%
                  </div>
                  <div className="p-2 bg-muted/15 border border-muted/20 rounded text-pink-400">
                    <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">Founder</span>
                    {skillData.monte_carlo.founder}%
                  </div>
                </div>
              </div>
            </div>

          </div>

          {/* Explainability Narrative */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-teal-300 flex items-center gap-2 mb-3">
              <Sparkles size={15} /> Skill Evolution Explanation &amp; Rationale
            </h4>
            <p className="text-xs leading-6 text-muted-foreground font-semibold bg-muted/20 border border-muted/30 p-4 rounded-lg h-44 overflow-y-auto whitespace-pre-line">
              {skillData.explanation}
            </p>
          </div>

        </Card>
      </section>

      {/* Part 24: Talent Digital Twin Engine & Human Future Simulation Platform Dashboard */}
      <section className="space-y-6">
        <Card className="border-indigo-500/20 bg-gradient-to-br from-card to-indigo-500/5 relative overflow-hidden">
          <div className="absolute right-0 top-0 h-40 w-40 bg-indigo-500/10 blur-3xl rounded-full" />
          
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-muted pb-4">
            <div>
              <Badge tone="indigo" className="px-2.5 py-1 text-xs font-semibold tracking-wide uppercase">
                Talent Digital Twin Engine
              </Badge>
              <h3 className="mt-2 text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
                <Sparkles className="text-indigo-400" /> Talent Digital Twin &amp; Future Behavior Simulator
              </h3>
              <p className="text-sm text-muted-foreground mt-1">
                Simulating future behaviors, leadership transitions, burnout warnings, retention probability, and organizational values.
              </p>
            </div>
            
            <div className="flex items-center gap-3">
              <div className="text-right">
                <span className="text-xs text-muted-foreground block font-medium">Predicted Org Value</span>
                <span className="text-2xl font-extrabold text-indigo-400">
                  {Math.round(twinSimData.organization_impact.organization_value * 100)}%
                </span>
              </div>
            </div>
          </div>

          {/* Fit, Retention, Promotion, Burnout Overview */}
          <div className="grid gap-4 grid-cols-2 md:grid-cols-4 mt-6">
            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Future Match Fit</span>
              <span className="text-2xl font-extrabold text-white block mt-1">
                97%
              </span>
              <span className="text-[10px] text-indigo-400 font-semibold uppercase">Current Fit: 91%</span>
            </div>

            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Retention Probability</span>
              <span className="text-2xl font-extrabold text-white block mt-1">
                {Math.round(twinSimData.retention.retention_probability * 100)}%
              </span>
              <span className="text-[10px] text-emerald-400 font-semibold uppercase">High Loyalty Projection</span>
            </div>

            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Promotion Likelihood</span>
              <span className="text-2xl font-extrabold text-white block mt-1">
                {Math.round(twinSimData.promotion.promotion_probability * 100)}%
              </span>
              <span className="text-[10px] text-indigo-400 font-semibold block">Fast promotion track</span>
            </div>

            <div className="p-4 rounded-lg bg-muted/20 border border-muted/30">
              <span className="text-xs font-bold text-muted-foreground uppercase block">Burnout Risk</span>
              <span className="text-2xl font-extrabold text-white block mt-1">
                {Math.round(twinSimData.burnout.burnout_probability * 100)}%
              </span>
              <span className="text-[10px] text-emerald-400 font-semibold block">Resignation: {Math.round(twinSimData.resignation.resignation_probability * 100)}%</span>
            </div>
          </div>

          {/* Personality and behaviors */}
          <div className="grid gap-6 md:grid-cols-2 mt-6 border-t border-muted pt-6">
            
            {/* OCEAN Personality Radar */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-indigo-300 mb-3">OCEAN Personality Digital Twin Traits</h4>
              <div className="space-y-2 text-xs">
                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">Openness to Experience</span>
                  <span className="text-white font-extrabold">{Math.round(twinSimData.personality.openness * 100)}%</span>
                </div>
                <div className="w-full bg-muted/30 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-indigo-500 h-full rounded-full" style={{ width: `${twinSimData.personality.openness * 100}%` }} />
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">Conscientiousness</span>
                  <span className="text-white font-extrabold">{Math.round(twinSimData.personality.conscientiousness * 100)}%</span>
                </div>
                <div className="w-full bg-muted/30 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-indigo-500 h-full rounded-full" style={{ width: `${twinSimData.personality.conscientiousness * 100}%` }} />
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-muted-foreground">Extroversion</span>
                  <span className="text-white font-extrabold">{Math.round(twinSimData.personality.extroversion * 100)}%</span>
                </div>
                <div className="w-full bg-muted/30 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-indigo-500 h-full rounded-full" style={{ width: `${twinSimData.personality.extroversion * 100}%` }} />
                </div>
              </div>
            </div>

            {/* Core Leadership Forecast tracks */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-violet-300 mb-3">5-Year Leadership Capacity Growth</h4>
              <div className="grid grid-cols-3 gap-3 text-center text-xs">
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <span className="text-[10px] font-bold text-muted-foreground uppercase block">Today</span>
                  <span className="text-xl font-extrabold text-white block mt-1">{Math.round(twinSimData.leadership.today * 100)}%</span>
                </div>
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <span className="text-[10px] font-bold text-muted-foreground uppercase block">Year 2</span>
                  <span className="text-xl font-extrabold text-indigo-400 block mt-1">{Math.round(twinSimData.leadership.year2 * 100)}%</span>
                </div>
                <div className="p-3 rounded bg-muted/20 border border-muted/30">
                  <span className="text-[10px] font-bold text-muted-foreground uppercase block">Year 5</span>
                  <span className="text-xl font-extrabold text-indigo-400 block mt-1">{Math.round(twinSimData.leadership.year5 * 100)}%</span>
                </div>
              </div>
            </div>

          </div>

          {/* Career progression node map */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-indigo-300 mb-3">Predicted Career Path Node Transitions</h4>
            <div className="flex flex-wrap items-center gap-3 font-bold text-xs">
              <span className="p-2 rounded bg-muted/35 text-white">Junior/Mid Engineer</span>
              <span className="text-indigo-400">→</span>
              <span className="p-2 rounded bg-muted/35 text-white">Senior Engineer</span>
              <span className="text-indigo-400">→</span>
              <span className="p-2 rounded bg-muted/35 text-white">Tech Lead</span>
              <span className="text-indigo-400">→</span>
              <span className="p-2 rounded bg-indigo-500/20 text-indigo-300">Engineering Manager</span>
              <span className="text-indigo-400">→</span>
              <span className="p-2 rounded bg-indigo-500/30 text-white">Director of Engineering</span>
            </div>
          </div>

          {/* Onboarding Timeline and scenarios */}
          <div className="grid gap-6 md:grid-cols-3 mt-6 border-t border-muted pt-6">
            
            {/* Timeline */}
            <div className="md:col-span-2">
              <h4 className="font-extrabold text-sm uppercase text-indigo-300 mb-3">Milestone Progress Simulations</h4>
              <div className="space-y-2 text-xs">
                <div className="flex gap-3 items-start p-2 rounded bg-muted/15 border border-muted/20">
                  <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400 font-extrabold">M1</span>
                  <span className="text-white">{twinSimData.simulation.milestones.month_1}</span>
                </div>
                <div className="flex gap-3 items-start p-2 rounded bg-muted/15 border border-muted/20">
                  <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400 font-extrabold">M6</span>
                  <span className="text-white">{twinSimData.simulation.milestones.month_6}</span>
                </div>
                <div className="flex gap-3 items-start p-2 rounded bg-muted/15 border border-muted/20">
                  <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400 font-extrabold">Y1</span>
                  <span className="text-white">{twinSimData.simulation.milestones.year_1}</span>
                </div>
                <div className="flex gap-3 items-start p-2 rounded bg-muted/15 border border-muted/20">
                  <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400 font-extrabold">Y2</span>
                  <span className="text-white">{twinSimData.simulation.milestones.year_2}</span>
                </div>
                <div className="flex gap-3 items-start p-2 rounded bg-muted/15 border border-muted/20">
                  <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400 font-extrabold">Y5</span>
                  <span className="text-white">{twinSimData.simulation.milestones.year_5}</span>
                </div>
              </div>
            </div>

            {/* Scenario simulator */}
            <div>
              <h4 className="font-extrabold text-sm uppercase text-teal-300 mb-3">Twin Scenario Branches</h4>
              <div className="space-y-2 text-xs">
                <div className="p-2.5 rounded bg-muted/15 border border-muted/20">
                  <span className="font-extrabold text-white block">{twinSimData.simulation.scenarios.startup.label}</span>
                  <span className="text-muted-foreground block mt-1">{twinSimData.simulation.scenarios.startup.outcome}</span>
                </div>
                <div className="p-2.5 rounded bg-muted/15 border border-muted/20">
                  <span className="font-extrabold text-white block">{twinSimData.simulation.scenarios.corporate.label}</span>
                  <span className="text-muted-foreground block mt-1">{twinSimData.simulation.scenarios.corporate.outcome}</span>
                </div>
                <div className="p-2.5 rounded bg-muted/15 border border-muted/20">
                  <span className="font-extrabold text-white block">{twinSimData.simulation.scenarios.government.label}</span>
                  <span className="text-muted-foreground block mt-1">{twinSimData.simulation.scenarios.government.outcome}</span>
                </div>
              </div>
            </div>

          </div>

          {/* Monte Carlo Future Projections */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-indigo-300 mb-3">10,000 Runs Future Trajectory Monte Carlo</h4>
            <div className="grid gap-3 grid-cols-2 md:grid-cols-4 text-center text-xs font-extrabold">
              <div className="p-3 bg-muted/15 border border-muted/20 rounded text-indigo-400">
                <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">CTO Profile</span>
                {twinSimData.monte_carlo.cto}%
              </div>
              <div className="p-3 bg-muted/15 border border-muted/20 rounded">
                <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">Principal Architect</span>
                {twinSimData.monte_carlo.architect}%
              </div>
              <div className="p-3 bg-muted/15 border border-muted/20 rounded">
                <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">Engineering Director</span>
                {twinSimData.monte_carlo.manager}%
              </div>
              <div className="p-3 bg-muted/15 border border-muted/20 rounded text-pink-400">
                <span className="text-[9px] block text-muted-foreground font-medium uppercase mb-0.5">Start-up Founder</span>
                {twinSimData.monte_carlo.founder}%
              </div>
            </div>
          </div>

          {/* Explainability Narrative */}
          <div className="mt-6 border-t border-muted pt-6">
            <h4 className="font-extrabold text-sm uppercase text-indigo-300 flex items-center gap-2 mb-3">
              <Sparkles size={15} /> Digital Twin Future Projection &amp; Rationale
            </h4>
            <p className="text-xs leading-6 text-muted-foreground font-semibold bg-muted/20 border border-muted/30 p-4 rounded-lg h-44 overflow-y-auto whitespace-pre-line">
              {twinSimData.explanation}
            </p>
          </div>

        </Card>
      </section>

    </div>
  );
}

