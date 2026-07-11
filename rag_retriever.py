knowledge = {
    "password": "Reset your password using the Forgot Password option.",
    "wifi": "Restart the router and reconnect to WiFi.",
    "printer": "Check the printer power and paper.",
    "email": "Check your internet connection and email settings.",
    "software": "Reinstall or update the software."
}

def retrieve(ticket):
    ticket = ticket.lower()

    for key in knowledge:
        if key in ticket:
            return knowledge[key]

    return "No matching solution found."