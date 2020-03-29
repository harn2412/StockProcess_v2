"""Cac cong cu lien quan den trinh bay noi dung"""
from shutil import get_terminal_size


def separate_print(title: str, sep_char="="):
    """In dai phan cach kem tieu de vua voi kich thuc cua cua so Console

    Tu dong in day phan cach va dong thoi tra ve chuoi tuong ung

    Args:
        title (str): Ten cua tieu de
        sep_char (str): (Optional) Ky tu dung de lam giai phan cach, mac
            dinh la "="

    Returns:
        str: Chuoi ky tu dung de lam giai phan cach

    Examples:
        >>>separate_print("TITLE")
        ==============TITLE==============

        >>>separate_print("TITLE", "*")
        **************TITLE**************

    """
    text = f"{title}".center(get_terminal_size().columns, sep_char)
    print(text)
    return text
