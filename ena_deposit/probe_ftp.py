#!/usr/bin/env python3
"""Sonde FTP Webin — dialogue complet avec le serveur.

Contourne curl et parle directement le protocole FTP, ce qui permet de voir
la reponse exacte du serveur et d'ecarter tout probleme de quoting.
Ne transfere aucun fichier. Le mot de passe est saisi au clavier.
"""
import ftplib, getpass, socket, sys

USER = input("Identifiant Webin : ").strip()
PASS = getpass.getpass("Mot de passe Webin : ")

print()
print(f"identifiant : {USER!r} ({len(USER)} car.)")
print(f"mot de passe: {len(PASS)} caracteres")
special = [c for c in PASS if not c.isalnum()]
if special:
    print(f"  caracteres non alphanumeriques : {' '.join(repr(c) for c in special)}")
print()

def essai(host, tls):
    label = "FTPS (chiffre)" if tls else "FTP (clair)"
    print(f"--- {host} / {label} ---")
    try:
        cls = ftplib.FTP_TLS if tls else ftplib.FTP
        f = cls()
        f.set_debuglevel(0)
        banner = f.connect(host, 21, timeout=30)
        print(f"  banniere : {banner.strip()}")
        if tls:
            f.auth()
            print("  TLS negocie")
        try:
            rep = f.login(USER, PASS)
            print(f"  LOGIN OK : {rep.strip()}")
            if tls:
                f.prot_p()
            try:
                items = f.nlst()
                print(f"  contenu du dropbox : {len(items)} entree(s)")
                for i in items[:5]:
                    print(f"    {i}")
            except Exception as e:
                print(f"  listing impossible : {e}")
            f.quit()
            return True
        except ftplib.error_perm as e:
            print(f"  REFUS : {e}")
        except Exception as e:
            print(f"  erreur : {type(e).__name__}: {e}")
        try: f.close()
        except Exception: pass
    except (socket.timeout, OSError) as e:
        print(f"  connexion impossible : {type(e).__name__}: {e}")
    return False

ok = False
for host in ("webin2.ebi.ac.uk", "webin.ebi.ac.uk"):
    for tls in (True, False):
        if essai(host, tls):
            ok = True
        print()

print("=" * 60)
if ok:
    print("Au moins une combinaison fonctionne : le transfert est possible.")
else:
    print("Aucune combinaison ne passe.")
    print("Le compte est valide (l'API delivre un jeton), donc soit le dropbox FTP")
    print("n'est pas encore provisionne, soit le mot de passe contient un caractere")
    print("que le service FTP gere mal. Voir les recommandations.")
