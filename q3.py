import numpy as np

# Define marginal probabilities
P_A = {"yes": 0.8, "no": 0.2}
P_C = {"yes": 0.5, "no": 0.5}

# Define conditional probabilities
P_G_given_A_C = {
    ("yes", "yes"): {"Good": 0.9, "OK": 0.1},
    ("yes", "no"): {"Good": 0.7, "OK": 0.3},
    ("no", "yes"): {"Good": 0.6, "OK": 0.4},
    ("no", "no"): {"Good": 0.3, "OK": 0.7},
}

P_J_given_G = {"Good": {"yes": 0.8, "no": 0.2}, "OK": {"yes": 0.2, "no": 0.8}}
P_S_given_G = {"Good": {"yes": 0.7, "no": 0.3}, "OK": {"yes": 0.3, "no": 0.7}}

# Monte Carlo simulation to estimate P(S="yes" | J="yes")
def monte_carlo_simulation(num_samples=10000):
    count_S_yes_given_J_yes = 0
    count_J_yes = 0

    for _ in range(num_samples):
        # Sample Aptitude Skills (A)
        A = "yes" if np.random.rand() < P_A["yes"] else "no"
        
        # Sample Coding Skills (C)
        C = "yes" if np.random.rand() < P_C["yes"] else "no"
        
        # Sample Grade (G) given A and C
        G_probs = P_G_given_A_C[(A, C)]
        G = "Good" if np.random.rand() < G_probs["Good"] else "OK"
        
        # Sample Go for Job (J) given G
        J_probs = P_J_given_G[G]
        J = "yes" if np.random.rand() < J_probs["yes"] else "no"
        
        # Sample Start a Startup (S) given G
        S_probs = P_S_given_G[G]
        S = "yes" if np.random.rand() < S_probs["yes"] else "no"
        
        # Check if J = "yes" and accumulate counts
        if J == "yes":
            count_J_yes += 1
            if S == "yes":
                count_S_yes_given_J_yes += 1

    # Calculate conditional probability
    if count_J_yes == 0:
        return 0  # Avoid division by zero
    return count_S_yes_given_J_yes / count_J_yes

# Run simulation
num_samples = 10000
estimated_probability = monte_carlo_simulation(num_samples)
print(f"Estimated P(S=yes | J=yes): {estimated_probability:.4f}")
