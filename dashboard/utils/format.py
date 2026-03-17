def format_change(change):
    emoji = "🚀" if change > 0 else "🪐"
    return f"{emoji} Cambio 24h: {change:.2f}%"
