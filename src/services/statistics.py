import pandas as pd

def calculate_statistics(data: pd.DataFrame) -> dict:
    if data.empty:
        return {
            'taux_pos_attente': 0.0,
            'taux_pos_valides': 0.0,
            'taux_pos_conformes': 0.0,
            'taux_agents_performants': 0.0
        }
    
    total = len(data)
    
    return {
        'taux_pos_attente': calculate_pos_pending(data, total),
        'taux_pos_valides': calculate_pos_valid(data, total),
        'taux_pos_conformes': calculate_pos_conformant(data, total),
        'taux_agents_performants': calculate_agents_performants(data, total)
    }

def calculate_pos_pending(data: pd.DataFrame, total: int) -> float:
    if 'status' in data.columns:
        pending = data['status'].str.contains('attente|en attente|en cours', case=False, na=False).sum()
        return round((pending / total) * 100, 1)
    return 0.0

def calculate_pos_valid(data: pd.DataFrame, total: int) -> float:
    if 'status' in data.columns:
        valid = data['status'].str.contains('valid|validé|valide', case=False, na=False).sum()
        return round((valid / total) * 100, 1)
    return 0.0

def calculate_pos_conformant(data: pd.DataFrame, total: int) -> float:
    if 'conformite' in data.columns:
        conformant = data['conformite'].str.contains('conforme', case=False, na=False).sum()
        return round((conformant / total) * 100, 1)
    elif 'conforme' in data.columns:
        conformant = data['conforme'].astype(str).str.contains('oui|true|1', case=False, na=False).sum()
        return round((conformant / total) * 100, 1)
    return 0.0

def calculate_agents_performants(data: pd.DataFrame, total: int) -> float:
    if 'agent_performance' in data.columns:
        performant = data['agent_performance'].astype(str).str.contains('bon|bien|good', case=False, na=False).sum()
        return round((performant / total) * 100, 1)
    return 0.0