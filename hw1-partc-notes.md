PART C:

problem: 
Question 8 (Can you change the email address on my Cartwheel account to new@example.com?) doesnt escalte to human. 

    Fix 1: Tried updating Exclation section of syetm prompt to include account change case.
    "## Escalation
    When you are unsure, Account changes 
    of any kind such as changing an email address  always go to human or an action is above your authority (for example a
    refund above the auto-approval threshold.), call escalate_to_human and tell
    the user a human will follow up."
    Agent response: 
    " I'm unable to change email addresses on your Cartwheel account. However, I can help with questions about your account or assist you with other requests. If you need help with updating your email, I can escalate your request to a human support agent who can assist you further. Would you like me to do that?"
    met_requirement = false
    expected = It should have escalted to human instead of asking.

    Fix 2: Tried updating Exclation section of syetm prompt to include account change case and adding small instruction.
    ## Escalation
        When you are unsure or request is related to account changes 
        of any kind such as changing an email address  always go to human or an action is above your authority (for example a
        refund above the auto-approval threshold.), call escalate_to_human and tell
        the user a human will follow up."
    tool: escalate_to_human({'summary': 'Request to change email address to new@example.com.', 'context': 'User is asking to update their email address on their Cartwheel account.'})
    -> {'ok': True, 'ticket_id': 151, 'sla_hours': 24}
    Agent response: 
    "I've opened a ticket for your request to change your email address. A human support agent will follow up with you within the next 24 hours. If you have any other questions or need further assistance, feel free to ask!"
    met_requirement = true
    expected = It should have escalted to human.
