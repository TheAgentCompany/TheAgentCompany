PASSWORDS = {
    "mark_johnson": "aaa123456789",
    "sarah_johnson": "Tr@ff1cL1ght99",
    "li_ming": "Dragon2024@Fly",
    "zhang_wei": "Cl0ud#Danc3r15",
    "mike_chen": "MikeChen123"
}

def create_passwords_file():
    with open("passwords.txt", "w") as f:
        for user, password in PASSWORDS.items():
            f.write(f"{user}: {password}\n")
    return


if __name__ == "__main__":
    create_passwords_file()