def format_phone(phone):
    if not phone:
        return None
    phone = ''.join(filter(str.isdigit, str(phone)))
    if len(phone) == 11:  # Formato brasileiro com DDD
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    return phone