import sys
import uvicorn
from app.main import app

if __name__ == "__main__":

    # Lista dei parametri consentiti in fase di esecuzione
    default_args: dict[str, str] = {"--port": "8000", "--host": "127.0.0.1", "--help": ""}

    # Lista dei parametri della riga di comando
    args = sys.argv[1:]
    args_params = [arg for arg in args if arg.startswith("--")]

    # Controllo della validità dei parametri
    invalid_args = [arg_param for arg_param in args_params 
                    if arg_param not in default_args]
    if invalid_args:
        print("Parametri non validi. Usare --help per il funzionamento.")
        sys.exit(1)

    # Se è stato richiesta la guida
    if "--help" in args:
        print("Utilizzo: test [options]")
        print("Options:")
        print("--port <port>     Porta su cui eseguire il server. Default: 8000")
        print("--host <host>     Host su cui eseguire il server. Default: 127.0.0.1")
        sys.exit(0)

    # Verifica che ogni parametro abbia un valore
    if len(args) % 2 != 0:
        print("Ogni parametro deve avere un valore. Usare --help per il funzionamento.")
        sys.exit(1)

    # Override dei parametri di default, se sono stati forniti nuovi valori
    for i in range(0, len(args), 2):
        default_args[args[i]] = args[i + 1]

    # avvio del server
    uvicorn.run(app, host=str(default_args["--host"]), port=int(default_args["--port"]))