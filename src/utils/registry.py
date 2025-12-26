import winreg

def get_user_path():
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Environment"
    ) as key:
        try:
            value, _ = winreg.QueryValueEx(key, "PATH")
            return value
        except FileNotFoundError:
            return ""
        
def set_user_path(new_path: str):
    with winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Environment",
        0,
        winreg.KEY_SET_VALUE
    ) as key:
        winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)