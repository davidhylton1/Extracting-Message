import re

def extract_values_for_open_signal(msg):
    patterns = {
        "trade_pair": r"^\s*([A-Za-z/]+)\s+(Short|Long)",
        "position_type": r"\b(Short|Long)\b",
        "open_price": r"Open Price:\s*([\d.]+)",
        "sl": r"SL:\s*([\d.]+)",
        "sl_pips": r"SL:\s*[\d.]+\s*\((\d+)pips\)",
        "start_exit_zone_tp": r"Start Exit Zone TP:\s*([\d.]+)",
        "one_to_one_risk_reward_tp": r"1:1 Risk:Reward TP:\s*([\d.]+)",
        "end_exit_zone_tp": r"End Exit Zone TP:\s*([\d.]+)",
        "ref_number": r"Ref#:\s*([A-Z]+[\d.]+)",
    }
    
    extracted_values = {key: re.search(pattern, msg).group(1) if re.search(pattern, msg) else None for key, pattern in patterns.items()}
    
    trade_pair = extracted_values['trade_pair'] if extracted_values['trade_pair'] is not None else ""
    position_type = extracted_values['position_type'].upper() if extracted_values['position_type'] is not None else ""
    open_price = float(extracted_values['open_price']) if extracted_values['open_price'] is not None else 0
    sl = float(extracted_values['sl']) if extracted_values['sl'] is not None else 0
    sl_pips = int(extracted_values['sl_pips']) if extracted_values['sl_pips'] is not None else 0
    start_exit_zone_tp = float(extracted_values['start_exit_zone_tp']) if extracted_values['start_exit_zone_tp'] is not None else 0
    one_to_one_risk_reward_tp = float(extracted_values['one_to_one_risk_reward_tp']) if extracted_values['one_to_one_risk_reward_tp'] is not None else 0
    end_exit_zone_tp = float(extracted_values['end_exit_zone_tp']) if extracted_values['end_exit_zone_tp'] is not None else 0
    ref_number = extracted_values['ref_number'] if extracted_values['ref_number'] is not None else ""

    if position_type == 'SHORT':
        sl_percent = (sl - open_price) * 100 / open_price
        tp_percent = (open_price - end_exit_zone_tp) * 100 / open_price
    else:
        sl_percent = (open_price - sl) * 100 / open_price
        tp_percent = (end_exit_zone_tp - open_price) * 100 / open_price

    return {
        "trade_pair": trade_pair,
        "position_type": position_type,
        "open_price": open_price,
        "sl": sl,
        "sl_pips": sl_pips,
        "start_exit_zone_tp": start_exit_zone_tp,
        "one_to_one_risk_reward_tp": one_to_one_risk_reward_tp,
        "end_exit_zone_tp": end_exit_zone_tp,
        "ref_number": ref_number,
        "sl_percent": sl_percent,
        "tp_percent": tp_percent,
    }