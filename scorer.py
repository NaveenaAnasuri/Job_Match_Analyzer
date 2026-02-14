def compute_fit_score(skills_percent: float, exp_contribution: int) -> float:
    """
    Final match score = skills percent + experience contribution (years)
    """
    return round(skills_percent + exp_contribution, 2)
