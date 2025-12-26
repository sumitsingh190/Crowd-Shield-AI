def compute_risk(
    crowd_count,
    avg_density,
    max_density,
    density_growth,
    movement_variance
):
    """
    CrowdShield AI – Risk Computation Logic

    Inputs come from real-time CV + feature engineering.
    Output is a smooth, interpretable risk score.
    """

    # -----------------------------
    # NORMALIZATION (0 → 1)
    # -----------------------------
    crowd_factor = min(crowd_count / 50, 1.0)           # crowd size importance
    density_factor = min(avg_density / 6, 1.0)          # spatial congestion
    growth_factor = min(density_growth / 4, 1.0)        # rate of increase
    movement_factor = min(movement_variance / 6, 1.0)   # panic indicator

    # -----------------------------
    # WEIGHTED RISK FUSION
    # -----------------------------
    risk_score = (
        0.35 * density_factor +
        0.25 * crowd_factor +
        0.25 * growth_factor +
        0.15 * movement_factor
    )

    risk_score = round(min(risk_score, 1.0), 2)

    # -----------------------------
    # STATUS LOGIC (STABLE)
    # -----------------------------
    if risk_score < 0.35:
        status = "SAFE"
    elif risk_score < 0.65:
        status = "WARNING"
    else:
        status = "CRITICAL"

    # -----------------------------
    # ALERT CONDITIONS (STRICT)
    # -----------------------------
    alert = (
        status == "CRITICAL"
        and crowd_count > 25
        and density_growth > 1.0
    )

    return risk_score, status, alert
