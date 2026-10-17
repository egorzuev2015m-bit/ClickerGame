import pymem
import pymem.process

PROCESS_NAME = "ClickerGame.exe"
MODULE_NAME = "ClickerGame.exe"

CLICKS_OFFSET = 0x11D7E8
CRIT_OFFSET = 0x11D010

try:
    pm = pymem.Pymem(PROCESS_NAME)
    module = pymem.process.module_from_name(pm.process_handle, MODULE_NAME)
    module_base = module.lpBaseOfDll
except Exception as e:
    pm = None
    module_base = 0
    _init_error = str(e)


def set_clicks(new_clicks: int):
    if pm is None:
        return f"❌ {_init_error}", "red"
    try:
        address = module_base + CLICKS_OFFSET
        pm.write_longlong(address, new_clicks)
        return f"👆 Set to {format_number(new_clicks)} clicks", "lightgreen"
    except Exception as e:
        return f"❌ Write failed: {e}", "red"


def set_crit_100():
    if pm is None:
        return f"❌ {_init_error}", "red"
    if CRIT_OFFSET == 0x000:
        return "⚠️ CRIT_OFFSET not set (use scanner)", "yellow"
    try:
        address = module_base + CRIT_OFFSET
        pm.write_int(address, 100)
        return "💥 Crit chance set to 100%", "lightgreen"
    except Exception as e:
        return f"❌ Write failed: {e}", "red"


def format_number(num: int) -> str:
    if num < 1000:
        return str(num)
    suffixes = ["", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc"]
    magnitude = 0
    dnum = float(num)
    while abs(dnum) >= 1000.0 and magnitude < len(suffixes) - 1:
        magnitude += 1
        dnum /= 1000.0
    if dnum >= 100:
        return f"{dnum:.0f}{suffixes[magnitude]}"
    elif dnum >= 10:
        return f"{dnum:.1f}{suffixes[magnitude]}"
    else:
        return f"{dnum:.2f}{suffixes[magnitude]}"


def parse_number(text: str) -> int:
    text = text.strip().upper()
    if not text:
        return 0
    multipliers = {
        "K": 1_000,
        "M": 1_000_000,
        "B": 1_000_000_000,
        "T": 1_000_000_000_000,
        "QA": 1_000_000_000_000_000,
        "QI": 1_000_000_000_000_000_000,
    }
    for suffix, mult in sorted(multipliers.items(), key=lambda x: -len(x[0])):
        if text.endswith(suffix):
            try:
                return int(float(text[:-len(suffix)].strip()) * mult)
            except ValueError:
                raise ValueError("Invalid number format")
    return int(float(text))