import pyfirmata
import time
import winsound

def main(args):
    try:
        board = pyfirmata.Arduino("")
    except:
        print("Erro na conexão")
        return -1
    print("Arduino conectado\n")
     
if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))