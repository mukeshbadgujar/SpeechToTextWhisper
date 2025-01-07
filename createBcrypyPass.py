import bcrypt
password = "Pass@123"
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
print(hashed_password)
