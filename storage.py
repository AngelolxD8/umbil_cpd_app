import os
import pandas as pd

CPD_FILE = "cpd_log.csv"
PDP_FILE = "pdp_goals.csv"

# --- CPD ---
def load_cpd():
    if os.path.exists(CPD_FILE):
        return pd.read_csv(CPD_FILE).to_dict(orient="records")
    return []

def save_cpd(cpd_list):
    df = pd.DataFrame(cpd_list)
    df.to_csv(CPD_FILE, index=False)

# --- PDP ---
def load_pdp():
    if os.path.exists(PDP_FILE):
        return pd.read_csv(PDP_FILE).to_dict(orient="records")
    return []

def save_pdp(pdp_list):
    df = pd.DataFrame(pdp_list)
    df.to_csv(PDP_FILE, index=False)
