-- database/schemas.sql
-- PostgreSQL Production Schema definitions for TalentMind AI Organizational DNA Platform

-- 1. Organization DNA Table
CREATE TABLE IF NOT EXISTS organization_dna (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL UNIQUE,
    company_type VARCHAR(50) DEFAULT 'corporate', -- startup, corporate, government
    speed NUMERIC(3,2) DEFAULT 0.50,
    ownership NUMERIC(3,2) DEFAULT 0.50,
    innovation NUMERIC(3,2) DEFAULT 0.50,
    risk NUMERIC(3,2) DEFAULT 0.50,
    hierarchy NUMERIC(3,2) DEFAULT 0.50,
    documentation NUMERIC(3,2) DEFAULT 0.50,
    leadership NUMERIC(3,2) DEFAULT 0.50,
    communication NUMERIC(3,2) DEFAULT 0.50,
    execution NUMERIC(3,2) DEFAULT 0.50,
    adaptability NUMERIC(3,2) DEFAULT 0.50,
    learning NUMERIC(3,2) DEFAULT 0.50,
    experimentation NUMERIC(3,2) DEFAULT 0.50,
    discipline NUMERIC(3,2) DEFAULT 0.50,
    process NUMERIC(3,2) DEFAULT 0.50,
    compliance NUMERIC(3,2) DEFAULT 0.50,
    teamwork NUMERIC(3,2) DEFAULT 0.50,
    collaboration NUMERIC(3,2) DEFAULT 0.50,
    creativity NUMERIC(3,2) DEFAULT 0.50,
    stability NUMERIC(3,2) DEFAULT 0.50,
    ambiguity NUMERIC(3,2) DEFAULT 0.50,
    customer_focus NUMERIC(3,2) DEFAULT 0.50,
    autonomy NUMERIC(3,2) DEFAULT 0.50,
    decision_speed NUMERIC(3,2) DEFAULT 0.50,
    accountability NUMERIC(3,2) DEFAULT 0.50,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Candidate DNA Table
CREATE TABLE IF NOT EXISTS candidate_dna (
    candidate_id VARCHAR(50) PRIMARY KEY,
    speed NUMERIC(3,2) DEFAULT 0.50,
    ownership NUMERIC(3,2) DEFAULT 0.50,
    leadership NUMERIC(3,2) DEFAULT 0.50,
    innovation NUMERIC(3,2) DEFAULT 0.50,
    learning NUMERIC(3,2) DEFAULT 0.50,
    communication NUMERIC(3,2) DEFAULT 0.50,
    risk NUMERIC(3,2) DEFAULT 0.50,
    adaptability NUMERIC(3,2) DEFAULT 0.50,
    stability NUMERIC(3,2) DEFAULT 0.50,
    creativity NUMERIC(3,2) DEFAULT 0.50,
    collaboration NUMERIC(3,2) DEFAULT 0.50,
    execution NUMERIC(3,2) DEFAULT 0.50,
    research NUMERIC(3,2) DEFAULT 0.50,
    management NUMERIC(3,2) DEFAULT 0.50,
    experimentation NUMERIC(3,2) DEFAULT 0.50,
    autonomy NUMERIC(3,2) DEFAULT 0.50,
    ambiguity NUMERIC(3,2) DEFAULT 0.50,
    customer NUMERIC(3,2) DEFAULT 0.50,
    team NUMERIC(3,2) DEFAULT 0.50,
    growth NUMERIC(3,2) DEFAULT 0.50,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Team DNA Table
CREATE TABLE IF NOT EXISTS team_dna (
    team_id VARCHAR(50) PRIMARY KEY,
    team_name VARCHAR(150) NOT NULL,
    company_name VARCHAR(150) NOT NULL,
    speed NUMERIC(3,2) DEFAULT 0.50,
    ownership NUMERIC(3,2) DEFAULT 0.50,
    leadership NUMERIC(3,2) DEFAULT 0.50,
    innovation NUMERIC(3,2) DEFAULT 0.50,
    learning NUMERIC(3,2) DEFAULT 0.50,
    communication NUMERIC(3,2) DEFAULT 0.50,
    risk NUMERIC(3,2) DEFAULT 0.50,
    adaptability NUMERIC(3,2) DEFAULT 0.50,
    stability NUMERIC(3,2) DEFAULT 0.50,
    collaboration NUMERIC(3,2) DEFAULT 0.50,
    execution NUMERIC(3,2) DEFAULT 0.50,
    research NUMERIC(3,2) DEFAULT 0.50,
    team NUMERIC(3,2) DEFAULT 0.50,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Culture Scores Table
CREATE TABLE IF NOT EXISTS culture_scores (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    company_name VARCHAR(150) NOT NULL,
    organization_match NUMERIC(3,2) NOT NULL,
    work_style_match NUMERIC(3,2) NOT NULL,
    leadership_match NUMERIC(3,2) NOT NULL,
    innovation_match NUMERIC(3,2) NOT NULL,
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Personality Profiles Table
CREATE TABLE IF NOT EXISTS personality_profiles (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    primary_persona VARCHAR(50) NOT NULL,
    secondary_persona VARCHAR(50) NOT NULL,
    tertiary_persona VARCHAR(50) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Future Growth Table
CREATE TABLE IF NOT EXISTS future_growth (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    month_6_success NUMERIC(3,2) NOT NULL,
    month_12_success NUMERIC(3,2) NOT NULL,
    month_24_success NUMERIC(3,2) NOT NULL,
    month_36_success NUMERIC(3,2) NOT NULL,
    future_role VARCHAR(150) NOT NULL,
    adaptability_forecast VARCHAR(50),
    leadership_forecast VARCHAR(50),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Compatibility Scores Table
CREATE TABLE IF NOT EXISTS compatibility_scores (
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    team_id VARCHAR(50) REFERENCES team_dna(team_id) ON DELETE CASCADE,
    compatibility NUMERIC(3,2) NOT NULL,
    conflict_probability NUMERIC(3,2) NOT NULL,
    knowledge_diversity VARCHAR(50) NOT NULL,
    synergy NUMERIC(3,2) NOT NULL,
    PRIMARY KEY (candidate_id, team_id)
);

-- 8. Innovation Profiles Table
CREATE TABLE IF NOT EXISTS innovation_profiles (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    innovation_score NUMERIC(3,2) NOT NULL,
    innovation_class VARCHAR(50) NOT NULL, -- HIGH, MODERATE, STANDARD
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 9. Leadership Profiles Table
CREATE TABLE IF NOT EXISTS leadership_profiles (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    leadership_score NUMERIC(3,2) NOT NULL,
    future_leader BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_c_dna_speed ON candidate_dna(speed);
CREATE INDEX IF NOT EXISTS idx_c_dna_learning ON candidate_dna(learning);
CREATE INDEX IF NOT EXISTS idx_culture_scores_match ON culture_scores(organization_match);
CREATE INDEX IF NOT EXISTS idx_personality_primary ON personality_profiles(primary_persona);

-- 10. Counterfactual Results Table
CREATE TABLE IF NOT EXISTS counterfactual_results (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    current_rank INT NOT NULL,
    future_rank INT NOT NULL,
    success_probability NUMERIC(3,2) NOT NULL,
    composite_score NUMERIC(5,2) NOT NULL,
    explanation TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 11. Counterfactual Paths Table
CREATE TABLE IF NOT EXISTS counterfactual_paths (
    id SERIAL PRIMARY KEY,
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    path_type VARCHAR(50) NOT NULL, -- CHEAPEST, FASTEST, HIGHEST_ROI, MAX_SCORE
    improvements TEXT[] NOT NULL,
    cost INT NOT NULL,
    months INT NOT NULL,
    score_gain NUMERIC(5,2) NOT NULL,
    roi NUMERIC(5,2) NOT NULL
);

-- 12. Counterfactual Costs Table
CREATE TABLE IF NOT EXISTS counterfactual_costs (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    estimated_cost VARCHAR(50) NOT NULL,
    estimated_months INT NOT NULL,
    difficulty_tier VARCHAR(50) DEFAULT 'Medium'
);

-- 13. Counterfactual Predictions Table
CREATE TABLE IF NOT EXISTS counterfactual_predictions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    month_6_score NUMERIC(5,2) NOT NULL,
    month_12_score NUMERIC(5,2) NOT NULL,
    month_24_score NUMERIC(5,2) NOT NULL,
    month_36_score NUMERIC(5,2) NOT NULL,
    month_60_score NUMERIC(5,2) NOT NULL
);

-- 14. Counterfactual Skills Table
CREATE TABLE IF NOT EXISTS counterfactual_skills (
    id SERIAL PRIMARY KEY,
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    difficulty VARCHAR(50) NOT NULL,
    score_gain NUMERIC(5,2) NOT NULL
);

-- 15. Counterfactual Experience Table
CREATE TABLE IF NOT EXISTS counterfactual_experience (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    required_months INT NOT NULL,
    projected_score NUMERIC(5,2) NOT NULL
);

-- 16. Counterfactual Projects Table
CREATE TABLE IF NOT EXISTS counterfactual_projects (
    id SERIAL PRIMARY KEY,
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    project_name VARCHAR(250) NOT NULL
);

-- 17. Counterfactual Leadership Table
CREATE TABLE IF NOT EXISTS counterfactual_leadership (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    mentees_required INT NOT NULL,
    lead_projects_required INT NOT NULL,
    future_leadership_score NUMERIC(3,2) NOT NULL
);

-- 18. Counterfactual Retention Table
CREATE TABLE IF NOT EXISTS counterfactual_retention (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    recommended_strategy VARCHAR(100) NOT NULL,
    projected_retention_prob NUMERIC(3,2) NOT NULL
);

-- 19. Candidate Risk Profiles Table
CREATE TABLE IF NOT EXISTS candidate_risk_profiles (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    risk_score NUMERIC(5,2) NOT NULL,
    joining_probability NUMERIC(3,2) NOT NULL,
    conflict_probability NUMERIC(3,2) NOT NULL,
    survival_probability NUMERIC(3,2) NOT NULL,
    explanation TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 20. Offer Predictions Table
CREATE TABLE IF NOT EXISTS offer_predictions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    accept_probability NUMERIC(3,2) NOT NULL,
    confidence NUMERIC(3,2) NOT NULL,
    risk_tier VARCHAR(50) NOT NULL
);

-- 21. Ghost Predictions Table
CREATE TABLE IF NOT EXISTS ghost_predictions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    ghost_probability NUMERIC(3,2) NOT NULL,
    risk_tier VARCHAR(50) NOT NULL
);

-- 22. Retention Predictions Table
CREATE TABLE IF NOT EXISTS retention_predictions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    month_3_prob NUMERIC(3,2) NOT NULL,
    month_6_prob NUMERIC(3,2) NOT NULL,
    month_12_prob NUMERIC(3,2) NOT NULL,
    month_24_prob NUMERIC(3,2) NOT NULL,
    month_36_prob NUMERIC(3,2) NOT NULL,
    month_60_prob NUMERIC(3,2) NOT NULL
);

-- 23. Promotion Predictions Table
CREATE TABLE IF NOT EXISTS promotion_predictions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    promotion_probability NUMERIC(3,2) NOT NULL
);

-- 24. Leadership Predictions Table
CREATE TABLE IF NOT EXISTS leadership_predictions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    future_leader_prob NUMERIC(3,2) NOT NULL,
    teamlead_prob NUMERIC(3,2) NOT NULL,
    manager_prob NUMERIC(3,2) NOT NULL,
    director_prob NUMERIC(3,2) NOT NULL
);

-- 25. Salary Predictions Table
CREATE TABLE IF NOT EXISTS salary_predictions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    salary_1_yr INT NOT NULL,
    salary_2_yr INT NOT NULL,
    salary_5_yr INT NOT NULL,
    salary_10_yr INT NOT NULL
);

-- 26. Burnout Predictions Table
CREATE TABLE IF NOT EXISTS burnout_predictions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    burnout_probability NUMERIC(3,2) NOT NULL,
    severity VARCHAR(50) NOT NULL
);

-- 27. Career Timelines Table
CREATE TABLE IF NOT EXISTS career_timelines (
    id SERIAL PRIMARY KEY,
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    milestone_year INT NOT NULL,
    milestone_role VARCHAR(150) NOT NULL
);

-- 28. Future Predictions Table
CREATE TABLE IF NOT EXISTS future_predictions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    success_probability NUMERIC(3,2) NOT NULL,
    classification VARCHAR(100) NOT NULL,
    resignation_probability NUMERIC(3,2) NOT NULL,
    expected_resignation_month INT NOT NULL
);

-- 29. Agent Arguments Table
CREATE TABLE IF NOT EXISTS agent_arguments (
    id SERIAL PRIMARY KEY,
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    agent_name VARCHAR(100) NOT NULL,
    argument_text TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL
);

-- 30. Agent Votes Table
CREATE TABLE IF NOT EXISTS agent_votes (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    hire_votes INT NOT NULL,
    reject_votes INT NOT NULL,
    abstain_votes INT NOT NULL
);

-- 31. Debate Rounds Table
CREATE TABLE IF NOT EXISTS debate_rounds (
    id SERIAL PRIMARY KEY,
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    round_number INT NOT NULL,
    topic VARCHAR(200) NOT NULL,
    agent_name VARCHAR(100) NOT NULL,
    message TEXT NOT NULL
);

-- 32. Consensus Scores Table
CREATE TABLE IF NOT EXISTS consensus_scores (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    consensus_percentage INT NOT NULL,
    decision VARCHAR(50) NOT NULL
);

-- 33. Judge Decisions Table
CREATE TABLE IF NOT EXISTS judge_decisions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    decision VARCHAR(50) NOT NULL,
    confidence NUMERIC(3,2) NOT NULL,
    reason TEXT NOT NULL
);

-- 34. Argument Graphs Table
CREATE TABLE IF NOT EXISTS argument_graphs (
    id SERIAL PRIMARY KEY,
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    source_node VARCHAR(100) NOT NULL,
    target_node VARCHAR(100) NOT NULL,
    relation_type VARCHAR(50) NOT NULL,
    weight NUMERIC(3,2) NOT NULL
);

-- 35. Committee Results Table
CREATE TABLE IF NOT EXISTS committee_results (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    final_recommendation VARCHAR(50) NOT NULL,
    total_agents INT NOT NULL
);

-- 36. Simulation Results Table
CREATE TABLE IF NOT EXISTS simulation_results (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    hire_probability INT NOT NULL,
    reject_probability INT NOT NULL
);

-- 37. Career Paths Table
CREATE TABLE IF NOT EXISTS career_paths (
    id SERIAL PRIMARY KEY,
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    step_year INT NOT NULL,
    step_role VARCHAR(150) NOT NULL
);

-- 38. Career Velocity Table
CREATE TABLE IF NOT EXISTS career_velocity (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    velocity_rate NUMERIC(3,2) NOT NULL,
    classification VARCHAR(50) NOT NULL
);

-- 39. Promotion Predictions Table
CREATE TABLE IF NOT EXISTS promotion_predictions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    promotion_probability NUMERIC(3,2) NOT NULL,
    expected_months INT NOT NULL
);

-- 40. Salary Predictions Table
CREATE TABLE IF NOT EXISTS salary_predictions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    salary_now INT NOT NULL,
    salary_1 INT NOT NULL,
    salary_2 INT NOT NULL,
    salary_5 INT NOT NULL,
    salary_10 INT NOT NULL
);

-- 41. Leadership Predictions Table
CREATE TABLE IF NOT EXISTS leadership_predictions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    leader_now INT NOT NULL,
    leader_2 INT NOT NULL,
    leader_5 INT NOT NULL,
    leader_10 INT NOT NULL
);

-- 42. Future Roles Table
CREATE TABLE IF NOT EXISTS future_roles (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    next_role VARCHAR(150) NOT NULL,
    probability NUMERIC(3,2) NOT NULL,
    timeline VARCHAR(50) NOT NULL
);

-- 43. Future Skills Table
CREATE TABLE IF NOT EXISTS future_skills (
    id SERIAL PRIMARY KEY,
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL
);

-- 44. Career Ceiling Table
CREATE TABLE IF NOT EXISTS career_ceiling (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    ceiling_role VARCHAR(150) NOT NULL,
    confidence NUMERIC(3,2) NOT NULL
);

-- 45. Career Simulations Table
CREATE TABLE IF NOT EXISTS career_simulations (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    startup_years INT NOT NULL,
    corp_years INT NOT NULL,
    faang_years INT NOT NULL
);

-- 46. Executive Predictions Table
CREATE TABLE IF NOT EXISTS executive_predictions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    executive_probability NUMERIC(3,2) NOT NULL
);

-- 47. Founder Predictions Table
CREATE TABLE IF NOT EXISTS founder_predictions (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    founder_probability NUMERIC(3,2) NOT NULL
);

-- 48. Career Risk Table
CREATE TABLE IF NOT EXISTS career_risk (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    burnout_index NUMERIC(3,2) NOT NULL,
    stagnation_index NUMERIC(3,2) NOT NULL,
    switching_index NUMERIC(3,2) NOT NULL
);

-- 49. Human Capital Values Table
CREATE TABLE IF NOT EXISTS human_capital_values (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    current_val INT NOT NULL,
    future_val INT NOT NULL,
    business_val INT NOT NULL
);

-- 50. Team Profiles Table
CREATE TABLE IF NOT EXISTS team_profiles (
    team_id VARCHAR(50) PRIMARY KEY,
    team_name VARCHAR(150) NOT NULL,
    department VARCHAR(100)
);

-- 51. Team DNA Table
CREATE TABLE IF NOT EXISTS team_dna (
    team_id VARCHAR(50) PRIMARY KEY REFERENCES team_profiles(team_id) ON DELETE CASCADE,
    team_size INT NOT NULL,
    backend INT NOT NULL,
    frontend INT NOT NULL,
    devops INT NOT NULL,
    avg_experience INT NOT NULL,
    leadership NUMERIC(3,2) NOT NULL,
    communication NUMERIC(3,2) NOT NULL,
    collaboration NUMERIC(3,2) NOT NULL,
    innovation NUMERIC(3,2) NOT NULL,
    mentoring NUMERIC(3,2) NOT NULL,
    risk_appetite NUMERIC(3,2) NOT NULL
);

-- 52. Organization DNA Table
CREATE TABLE IF NOT EXISTS organization_dna (
    org_id VARCHAR(50) PRIMARY KEY,
    organization_type VARCHAR(100) NOT NULL,
    risk_profile NUMERIC(3,2) NOT NULL,
    innovation_profile NUMERIC(3,2) NOT NULL,
    ownership_profile NUMERIC(3,2) NOT NULL,
    speed_profile NUMERIC(3,2) NOT NULL
);

-- 53. Communication Scores Table
CREATE TABLE IF NOT EXISTS communication_scores (
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    team_id VARCHAR(50) REFERENCES team_profiles(team_id) ON DELETE CASCADE,
    communication_fit NUMERIC(3,2) NOT NULL,
    PRIMARY KEY (candidate_id, team_id)
);

-- 54. Leadership Scores Table
CREATE TABLE IF NOT EXISTS leadership_scores (
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    team_id VARCHAR(50) REFERENCES team_profiles(team_id) ON DELETE CASCADE,
    leadership_balance NUMERIC(3,2) NOT NULL,
    leadership_conflict NUMERIC(3,2) NOT NULL,
    PRIMARY KEY (candidate_id, team_id)
);

-- 55. Conflict Scores Table
CREATE TABLE IF NOT EXISTS conflict_scores (
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    team_id VARCHAR(50) REFERENCES team_profiles(team_id) ON DELETE CASCADE,
    conflict_probability NUMERIC(3,2) NOT NULL,
    PRIMARY KEY (candidate_id, team_id)
);

-- 56. Knowledge Diversity Scores Table
CREATE TABLE IF NOT EXISTS knowledge_diversity_scores (
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    team_id VARCHAR(50) REFERENCES team_profiles(team_id) ON DELETE CASCADE,
    knowledge_diversity NUMERIC(3,2) NOT NULL,
    redundancy NUMERIC(3,2) NOT NULL,
    PRIMARY KEY (candidate_id, team_id)
);

-- 57. Mentorship Scores Table
CREATE TABLE IF NOT EXISTS mentorship_scores (
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    team_id VARCHAR(50) REFERENCES team_profiles(team_id) ON DELETE CASCADE,
    mentor_score NUMERIC(3,2) NOT NULL,
    PRIMARY KEY (candidate_id, team_id)
);

-- 58. Productivity Scores Table
CREATE TABLE IF NOT EXISTS productivity_scores (
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    team_id VARCHAR(50) REFERENCES team_profiles(team_id) ON DELETE CASCADE,
    productivity_gain NUMERIC(3,2) NOT NULL,
    PRIMARY KEY (candidate_id, team_id)
);

-- 59. Innovation Scores Table
CREATE TABLE IF NOT EXISTS innovation_scores (
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    team_id VARCHAR(50) REFERENCES team_profiles(team_id) ON DELETE CASCADE,
    innovation_boost NUMERIC(3,2) NOT NULL,
    PRIMARY KEY (candidate_id, team_id)
);

-- 60. Burnout Scores Table
CREATE TABLE IF NOT EXISTS burnout_scores (
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    team_id VARCHAR(50) REFERENCES team_profiles(team_id) ON DELETE CASCADE,
    burnout_risk NUMERIC(3,2) NOT NULL,
    PRIMARY KEY (candidate_id, team_id)
);

-- 61. Social Graphs Table
CREATE TABLE IF NOT EXISTS social_graphs (
    team_id VARCHAR(50) PRIMARY KEY REFERENCES team_profiles(team_id) ON DELETE CASCADE,
    graph_json TEXT NOT NULL
);

-- 62. Team Simulations Table
CREATE TABLE IF NOT EXISTS team_simulations (
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    team_id VARCHAR(50) REFERENCES team_profiles(team_id) ON DELETE CASCADE,
    productivity_index NUMERIC(3,2) NOT NULL,
    innovation_index NUMERIC(3,2) NOT NULL,
    mentorship_index NUMERIC(3,2) NOT NULL,
    PRIMARY KEY (candidate_id, team_id)
);

-- 63. Monte Carlo Results Table
CREATE TABLE IF NOT EXISTS monte_carlo_results (
    candidate_id VARCHAR(50) REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    team_id VARCHAR(50) REFERENCES team_profiles(team_id) ON DELETE CASCADE,
    success_percentage INT NOT NULL,
    conflict_percentage INT NOT NULL,
    burnout_percentage INT NOT NULL,
    innovation_percentage INT NOT NULL,
    PRIMARY KEY (candidate_id, team_id)
);

-- 64. Skill Timelines Table
CREATE TABLE IF NOT EXISTS skill_timelines (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    timeline_json TEXT NOT NULL
);

-- 65. Skill Graphs Table
CREATE TABLE IF NOT EXISTS skill_graphs (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    graph_json TEXT NOT NULL
);

-- 66. Skill Forecasts Table
CREATE TABLE IF NOT EXISTS skill_forecasts (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    forecast_json TEXT NOT NULL
);

-- 67. Skill Dependencies Table
CREATE TABLE IF NOT EXISTS skill_dependencies (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    dependencies_json TEXT NOT NULL
);

-- 68. Learning Velocity Metrics Table
CREATE TABLE IF NOT EXISTS learning_velocity_metrics (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    learning_velocity NUMERIC(3,2) NOT NULL,
    velocity_category VARCHAR(50) NOT NULL
);

-- 69. GitHub Metrics Table
CREATE TABLE IF NOT EXISTS github_metrics (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    github_growth NUMERIC(3,2) NOT NULL,
    python_activity NUMERIC(3,2) NOT NULL,
    cloud_activity NUMERIC(3,2) NOT NULL
);

-- 70. Project Metrics Table
CREATE TABLE IF NOT EXISTS project_metrics (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    project_velocity NUMERIC(3,2) NOT NULL
);

-- 71. Future Skills Table
CREATE TABLE IF NOT EXISTS future_skills (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    skills_json TEXT NOT NULL
);

-- 72. Obsolescence Scores Table
CREATE TABLE IF NOT EXISTS obsolescence_scores (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    scores_json TEXT NOT NULL
);

-- 73. Specialization Paths Table
CREATE TABLE IF NOT EXISTS specialization_paths (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    specialization_path VARCHAR(150) NOT NULL
);

-- 74. Skill Career Forecasts Table
CREATE TABLE IF NOT EXISTS skill_career_forecasts (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    path_json TEXT NOT NULL
);

-- 75. Skill Leadership Forecasts Table
CREATE TABLE IF NOT EXISTS skill_leadership_forecasts (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    leadership_now INT NOT NULL,
    leadership_24m INT NOT NULL
);

-- 76. Human Potential Scores Table
CREATE TABLE IF NOT EXISTS human_potential_scores (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    potential_score NUMERIC(3,2) NOT NULL
);

-- 77. Skill Simulation Results Table
CREATE TABLE IF NOT EXISTS skill_simulation_results (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    simulations_json TEXT NOT NULL
);

-- 78. Twin Behavior Profiles Table
CREATE TABLE IF NOT EXISTS twin_behavior_profiles (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    work_style VARCHAR(50) NOT NULL,
    collaboration_style VARCHAR(100) NOT NULL,
    communication_style VARCHAR(100) NOT NULL,
    leadership_style VARCHAR(100) NOT NULL,
    decision_style VARCHAR(100) NOT NULL,
    risk_style VARCHAR(100) NOT NULL,
    learning_style VARCHAR(100) NOT NULL,
    stress_response VARCHAR(100) NOT NULL
);

-- 79. Twin Personality Profiles Table
CREATE TABLE IF NOT EXISTS twin_personality_profiles (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    openness NUMERIC(3,2) NOT NULL,
    conscientiousness NUMERIC(3,2) NOT NULL,
    extroversion NUMERIC(3,2) NOT NULL,
    agreeableness NUMERIC(3,2) NOT NULL,
    neuroticism NUMERIC(3,2) NOT NULL
);

-- 80. Twin Learning Profiles Table
CREATE TABLE IF NOT EXISTS twin_learning_profiles (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    learning_velocity NUMERIC(3,2) NOT NULL,
    future_growth NUMERIC(3,2) NOT NULL
);

-- 81. Twin Career Forecasts Table
CREATE TABLE IF NOT EXISTS twin_career_forecasts (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    timeline_json TEXT NOT NULL
);

-- 82. Twin Leadership Forecasts Table
CREATE TABLE IF NOT EXISTS twin_leadership_forecasts (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    today_score NUMERIC(3,2) NOT NULL,
    year2_score NUMERIC(3,2) NOT NULL,
    year5_score NUMERIC(3,2) NOT NULL
);

-- 83. Twin Promotion Scores Table
CREATE TABLE IF NOT EXISTS twin_promotion_scores (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    promotion_probability NUMERIC(3,2) NOT NULL
);

-- 84. Twin Retention Scores Table
CREATE TABLE IF NOT EXISTS twin_retention_scores (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    retention_probability NUMERIC(3,2) NOT NULL
);

-- 85. Twin Burnout Scores Table
CREATE TABLE IF NOT EXISTS twin_burnout_scores (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    burnout_probability NUMERIC(3,2) NOT NULL
);

-- 86. Twin Innovation Scores Table
CREATE TABLE IF NOT EXISTS twin_innovation_scores (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    innovation_score NUMERIC(3,2) NOT NULL
);

-- 87. Twin Team Impacts Table
CREATE TABLE IF NOT EXISTS twin_team_impacts (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    team_productivity NUMERIC(3,2) NOT NULL,
    team_innovation NUMERIC(3,2) NOT NULL
);

-- 88. Twin Organization Impacts Table
CREATE TABLE IF NOT EXISTS twin_organization_impacts (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    organization_value NUMERIC(3,2) NOT NULL
);

-- 89. Twin Digital Twins Table
CREATE TABLE IF NOT EXISTS twin_digital_twins (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    twin_json TEXT NOT NULL
);

-- 90. Twin Future Simulations Table
CREATE TABLE IF NOT EXISTS twin_future_simulations (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    simulations_json TEXT NOT NULL
);

-- 91. Twin Monte Carlo Results Table
CREATE TABLE IF NOT EXISTS twin_monte_carlo_results (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    cto_prob INT NOT NULL,
    architect_prob INT NOT NULL,
    manager_prob INT NOT NULL,
    founder_prob INT NOT NULL
);

-- 92. Recruiter States Table
CREATE TABLE IF NOT EXISTS recruiter_states (
    state_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    experience INT NOT NULL,
    skills TEXT NOT NULL, -- JSON list
    salary NUMERIC(10,2) NOT NULL,
    joining INT NOT NULL,
    leadership NUMERIC(3,2) NOT NULL,
    future_potential NUMERIC(3,2) NOT NULL,
    retention NUMERIC(3,2) NOT NULL,
    risk NUMERIC(3,2) NOT NULL
);

-- 93. Weight States Table
CREATE TABLE IF NOT EXISTS weight_states (
    state_id INTEGER PRIMARY KEY REFERENCES recruiter_states(state_id) ON DELETE CASCADE,
    skill_weight NUMERIC(3,2) NOT NULL,
    experience_weight NUMERIC(3,2) NOT NULL,
    leadership_weight NUMERIC(3,2) NOT NULL,
    future_weight NUMERIC(3,2) NOT NULL,
    retention_weight NUMERIC(3,2) NOT NULL,
    risk_weight NUMERIC(3,2) NOT NULL
);

-- 94. Constraint States Table
CREATE TABLE IF NOT EXISTS constraint_states (
    state_id INTEGER PRIMARY KEY REFERENCES recruiter_states(state_id) ON DELETE CASCADE,
    salary_max NUMERIC(10,2) NOT NULL,
    notice_max INT NOT NULL,
    retention_min NUMERIC(3,2) NOT NULL
);

-- 95. Scenario States Table
CREATE TABLE IF NOT EXISTS scenario_states (
    scenario_id VARCHAR(50) PRIMARY KEY,
    label VARCHAR(100) NOT NULL,
    weights_json TEXT NOT NULL,
    description TEXT
);

-- 96. Candidate Movements Table
CREATE TABLE IF NOT EXISTS candidate_movements (
    movement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_id VARCHAR(50) NOT NULL,
    old_rank INT NOT NULL,
    new_rank INT NOT NULL,
    delta INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 97. Ranking Snapshots Table
CREATE TABLE IF NOT EXISTS ranking_snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ranking_json TEXT NOT NULL
);

-- 98. Stability Scores Table
CREATE TABLE IF NOT EXISTS stability_scores (
    candidate_id VARCHAR(50) PRIMARY KEY,
    stability_score NUMERIC(3,2) NOT NULL
);

-- 99. Sensitivity Scores Table
CREATE TABLE IF NOT EXISTS sensitivity_scores (
    variable_name VARCHAR(50) PRIMARY KEY,
    sensitivity_percentage NUMERIC(5,2) NOT NULL
);

-- 100. Counterfactual Results Table
CREATE TABLE IF NOT EXISTS counterfactual_results (
    candidate_id VARCHAR(50) PRIMARY KEY,
    target_rank INT NOT NULL,
    conditions_json TEXT NOT NULL
);

-- 101. Simulation Results Table
CREATE TABLE IF NOT EXISTS simulation_results (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    winner_candidate_id VARCHAR(50) NOT NULL,
    parameters_json TEXT NOT NULL
);

-- 102. Optimization Results Table
CREATE TABLE IF NOT EXISTS optimization_results (
    optimization_type VARCHAR(50) PRIMARY KEY,
    candidate_id VARCHAR(50) NOT NULL,
    score NUMERIC(5,2) NOT NULL
);

-- 103. MOHO Optimization Objectives
CREATE TABLE IF NOT EXISTS optimization_objectives (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    quality NUMERIC(5,2) NOT NULL,
    future NUMERIC(5,2) NOT NULL,
    leadership NUMERIC(5,2) NOT NULL,
    innovation NUMERIC(5,2) NOT NULL,
    retention NUMERIC(5,2) NOT NULL,
    learning NUMERIC(5,2) NOT NULL,
    salary NUMERIC(10,2) NOT NULL,
    joining INT NOT NULL
);

-- 104. MOHO Optimization Constraints
CREATE TABLE IF NOT EXISTS optimization_constraints (
    constraint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    salary_max NUMERIC(10,2) NOT NULL,
    joining_max INT NOT NULL,
    experience_min INT NOT NULL,
    required_skills_json TEXT
);

-- 105. MOHO Pareto Frontiers Table
CREATE TABLE IF NOT EXISTS pareto_frontiers (
    frontier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    frontier_json TEXT NOT NULL
);

-- 106. MOHO Genetic Populations Table
CREATE TABLE IF NOT EXISTS genetic_populations (
    population_id INTEGER PRIMARY KEY AUTOINCREMENT,
    generation_number INT NOT NULL,
    chromosomes_json TEXT NOT NULL
);

-- 107. MOHO Tradeoff Results Table
CREATE TABLE IF NOT EXISTS tradeoff_results (
    tradeoff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    matrix_json TEXT NOT NULL
);

-- 108. MOHO Scenario Results Table
CREATE TABLE IF NOT EXISTS scenario_results (
    scenario_id VARCHAR(50) PRIMARY KEY,
    recommended_candidate_id VARCHAR(50) NOT NULL,
    score NUMERIC(5,2) NOT NULL
);

-- 109. MOHO Future Value Scores Table
CREATE TABLE IF NOT EXISTS future_value_scores (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    current_value NUMERIC(5,2) NOT NULL,
    future_value NUMERIC(5,2) NOT NULL,
    leadership_value NUMERIC(5,2) NOT NULL,
    innovation_value NUMERIC(5,2) NOT NULL
);

-- 110. MOHO Risk Scores Table
CREATE TABLE IF NOT EXISTS risk_scores (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    attrition_risk NUMERIC(5,2) NOT NULL,
    burnout_risk NUMERIC(5,2) NOT NULL,
    ghosting_risk NUMERIC(5,2) NOT NULL
);

-- 111. MOHO Team Scores Table
CREATE TABLE IF NOT EXISTS team_scores (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    happiness NUMERIC(5,2) NOT NULL,
    productivity NUMERIC(5,2) NOT NULL,
    knowledge_sharing NUMERIC(5,2) NOT NULL
);

-- 112. MOHO Organization Scores Table
CREATE TABLE IF NOT EXISTS organization_scores (
    candidate_id VARCHAR(50) PRIMARY KEY REFERENCES candidate_dna(candidate_id) ON DELETE CASCADE,
    business_value NUMERIC(5,2) NOT NULL,
    innovation NUMERIC(5,2) NOT NULL,
    retention NUMERIC(5,2) NOT NULL
);

-- 113. RMG Recruiter Memory Activity Logs
CREATE TABLE IF NOT EXISTS recruiter_memory (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recruiter_id VARCHAR(50) NOT NULL,
    candidate_id VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata_json TEXT
);

-- 114. RMG Recruiter Preferences Table
CREATE TABLE IF NOT EXISTS recruiter_preferences (
    recruiter_id VARCHAR(50) PRIMARY KEY,
    communication NUMERIC(3,2) NOT NULL,
    leadership NUMERIC(3,2) NOT NULL,
    github NUMERIC(3,2) NOT NULL,
    opensource NUMERIC(3,2) NOT NULL,
    learning NUMERIC(3,2) NOT NULL,
    stability NUMERIC(3,2) NOT NULL
);

-- 115. RMG Recruiter Graph Relations Cache
CREATE TABLE IF NOT EXISTS recruiter_graph (
    source_id VARCHAR(50) NOT NULL,
    target_id VARCHAR(50) NOT NULL,
    relation_type VARCHAR(50) NOT NULL,
    weight NUMERIC(5,2) DEFAULT 1.0,
    PRIMARY KEY (source_id, target_id, relation_type)
);

-- 116. RMG Recruiter Behavior Table
CREATE TABLE IF NOT EXISTS recruiter_behavior (
    recruiter_id VARCHAR(50) PRIMARY KEY,
    risk_tolerance NUMERIC(3,2) NOT NULL,
    cost_sensitivity NUMERIC(3,2) NOT NULL,
    speed_preference NUMERIC(3,2) NOT NULL,
    innovation_preference NUMERIC(3,2) NOT NULL,
    future_potential_preference NUMERIC(3,2) NOT NULL
);

-- 117. RMG Recruiter DNA Profiles Table
CREATE TABLE IF NOT EXISTS recruiter_dna (
    recruiter_id VARCHAR(50) PRIMARY KEY,
    dna_vector_json TEXT NOT NULL,
    metrics_json TEXT NOT NULL
);

-- 118. RMG Recruiter Preference Patterns
CREATE TABLE IF NOT EXISTS recruiter_patterns (
    pattern_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recruiter_id VARCHAR(50) NOT NULL,
    pattern_type VARCHAR(50) NOT NULL,
    confidence NUMERIC(3,2) NOT NULL,
    description TEXT
);

-- 119. RMG Recruiter Predictions Table
CREATE TABLE IF NOT EXISTS recruiter_predictions (
    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recruiter_id VARCHAR(50) NOT NULL,
    candidate_id VARCHAR(50) NOT NULL,
    hire_prob NUMERIC(3,2) NOT NULL,
    shortlist_prob NUMERIC(3,2) NOT NULL,
    interview_prob NUMERIC(3,2) NOT NULL,
    reject_prob NUMERIC(3,2) NOT NULL
);

-- 120. RMG Recruiter Recommendations Table
CREATE TABLE IF NOT EXISTS recruiter_recommendations (
    recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recruiter_id VARCHAR(50) NOT NULL,
    candidate_id VARCHAR(50) NOT NULL,
    match_reason TEXT NOT NULL
);

-- 121. RMG Recruiter Embeddings Table
CREATE TABLE IF NOT EXISTS recruiter_embeddings (
    recruiter_id VARCHAR(50) PRIMARY KEY,
    embedding_json TEXT NOT NULL
);

-- 122. RMG Recruiter Feedback Table
CREATE TABLE IF NOT EXISTS recruiter_feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recruiter_id VARCHAR(50) NOT NULL,
    candidate_id VARCHAR(50) NOT NULL,
    feedback_type VARCHAR(50) NOT NULL,
    score_adjustment NUMERIC(5,2) NOT NULL
);

-- 123. RMG Recruiter Hiring History
CREATE TABLE IF NOT EXISTS recruiter_hiring_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recruiter_id VARCHAR(50) NOT NULL,
    candidate_id VARCHAR(50) NOT NULL,
    hire_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    retention_status VARCHAR(50) DEFAULT 'active'
);










