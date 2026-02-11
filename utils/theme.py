def apply_theme(dark=True):
    if dark:
        bg = "#0f172a"
        text = "#e5e7eb"
    else:
        bg = "#f8fafc"
        text = "#0f172a"

    return f"""
    <style>
    body {{
        background-color: {bg};
        color: {text};
    }}
    .kpi {{
        border-radius: 18px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 0 18px rgba(0,255,255,0.25);
    }}
    </style>
    """