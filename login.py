import bcrypt as bcrypt


def acceso(pasw):
    #passw = u"josetello"
    #password = bcrypt.hashpw(passw.encode('utf8'), bcrypt.gensalt(14))
    password = b'$2b$14$lfs4Pa3EkXMB2IOer7WmOeZzzytJYczWw5uU8fYZjrjVwJkgupwRq'
    #print(password)
    to_check = str(pasw)
    if bcrypt.checkpw(to_check.encode('utf8'), password):
        return True
    else:
        return False