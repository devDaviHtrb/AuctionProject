
from myapp.setup.authMng.InitLoginManager import login_manager
@login_manager.user_loader
def load_user(user_id):
    return "sdfsdfsd" 