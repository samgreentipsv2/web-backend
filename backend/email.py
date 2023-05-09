from djoser import email

class PasswordResetEmail(email.PasswordResetEmail):
    template_name = 'backend/password_reset.html'
    
    
    
    
class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = 'backend/password_changed_confirmation.html'
    

class ConfirmationEmail(email.ConfirmationEmail):
    template_name = 'backend/confirmation.html'
    