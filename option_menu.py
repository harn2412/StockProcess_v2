"""Giup tao / kiem tra / xu ly cac menu tuy chon"""


def create_and_check(user_input, valid_choices, multi=True):
    """Lay thong tin cua nguoi dung nhap vao va tra ve danh sach cac tuy chon hop le
    cac bien dau vao:
        user_input: str : Cac tuy chon nguoi dung nhap vao,
            phan cach boi khoang trang va dau phay ", "
        valid_opts: list / tuple / set: Danh sach cac tuy chon hop le,
            cac phan tu phai la str, VD: ["1", "2", "3"] hoac ("yes", "no")
        multi: boolean: Co cho phep nhieu tuy chon cung luc khong
    ket qua:
        hop le: Tra ve danh sach cac tuy chon hop le dung dang set
        khong hop le: ValueError exception """

    # Xoa cac khoang trang
    user_input = user_input.replace(" ", "")

    # tach cac tuy chon
    user_input = user_input.split(",")

    # chuyen ve SET OBJECT de tranh truong hop cac tuy chon bi trung
    user_input = set(user_input)

    # truong hop chi cho phep mot tuy chon thoi thi se bao loi
    if (len(user_input) > 1) and (multi is not True):
        raise ValueError("Chi cho phep 1 tuy chon")

    # so sanh voi danh sach tuy chon hop le
    if not user_input.issubset(set(valid_choices)):
        raise ValueError("Co tuy chon khong hop le")
    else:
        return user_input


def get_opts(options, choices, choosed, choice_all=None):
    """Dua ra ket qua cua cac tuy chon ung voi danh sach tuy chon duoc dua vao
    cac bien dau vao:
        options: list / tuple : Cac ket qua tra ve ung voi cac lua chon
        choices: list / tuple : Cac lua chon ma nguoi dung co the chon
        choosed: list / tuple / set : Cac lua chon da duoc chon
        select_all: any : Tuy chon ma khi suat hien se tra ve tat ca ket qua
            (mac dinh la None)
        Luu y: cac phan tu cua "choices" va "choosed" phai giong nhau
    ket qua:
        hop le: Tra ve list cac ket qua
        khong hop le: ValueError exception"""

    # kiem tra xem "choices" va "options" co tuong ung khong
    if len(options) != len(choices):
        raise ValueError("So luong phan tu khong giong nhau")

    # truong hop chon tat ca
    if (choice_all is not None) and (choice_all in choosed):
        return options

    # lay cac ket qua
    result = []
    for i, option in zip(choices, options):
        if i in choosed:
            result.append(option)
    return result


def get_opts_from_input(user_input, options, valid_choices, choice_all=None, multi=True):
    """Dua ra ket qua cua cac tuy chon ung voi noi dung ma nguoi dung nhap vao
    cac bien dau vao:
        user_input: str : Lua chon cua nguoi dung duoi dang str
        options: list / tuple : Cac ket qua tra ve ung voi cac lua chon
        valid_choices: list / tuple / set : Cac tuy chon co the su dung
        choice_all: any : Ung voi viec chon tat ca cac tuy chon (mac dinh None)
        multi: boolean : Cho phep chon nhieu tuy chon hay khong
    ket qua:
        hop le: Tra ve list cac ket qua option tuong ung
        khong hop le: ValueError exception"""

    # danh sach tat ca cac tuy chon bao gom ca tuy chon tat ca
    try:
        choices = set(valid_choices) | set(choice_all)
    except TypeError:
        choices = set(valid_choices)

    # danh sach cac tuy chon nguoi dung da chon
    choosed = create_and_check(user_input=user_input,
                               valid_choices=choices,
                               multi=multi)

    # co chon tat ca cac tuy chon khong
    return get_opts(options=options,
                    choices=valid_choices,
                    choosed=choosed,
                    choice_all=choice_all)


def main():
    pass


if __name__ == '__main__':
    main()
