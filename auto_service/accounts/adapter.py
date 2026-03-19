from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return True
    
    def generate_unique_username(self, usernames):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        username = usernames[0] if usernames else "user"
        if '@' in username:
            username = username.split('@')[0]
        
        username = ''.join(c for c in username if c.isalnum() or c in ['_', '-'])
        
        if User.objects.filter(username=username).exists():
            import random
            username = f"{username}{random.randint(100, 999)}"
        
        return username
