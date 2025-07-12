def clean_airport_name(name):
    """
    Clean and shorten airport names for better display
    """
    if not name or name == "Unknown":
        return "Unknown"
    if 'International' in name:
        parts = name.split(' International')[0]
        return parts.split()[-1] if len(parts.split()) > 1 else parts
    elif 'Airport' in name:
        parts = name.split(' Airport')[0]
        return parts.split()[-1] if len(parts.split()) > 1 else parts
    else:
        words = name.split()
        return ' '.join(words[:3]) if len(words) > 3 else name 