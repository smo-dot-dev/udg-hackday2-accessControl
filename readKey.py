import RPi.GPIO as GPIO
from time import sleep
import sqlite3

GPIO.setwarnings(False)
pines = [[37,35,33,31],[40,38,36,32]]
GPIO.setmode(GPIO.BOARD)
resultado = [['X','7','4','1'],['N','8','5','2'],['N','9','6','3'],['V','N','N','0']]
def write():
    for i in range(4):
        GPIO.setup(pines[0][i], GPIO.OUT)
        GPIO.setup(pines[1][i], GPIO.IN)
    for i in range(4):
        GPIO.output(pines[0][i], GPIO.HIGH);
    x = 5;
    while x == 5:
        for i in range(4):
            p = GPIO.input(pines[1][i]);
            if p == 1:
                x = i;
                break;

    for i in range(4):
        GPIO.setup(pines[1][i], GPIO.OUT)
        GPIO.setup(pines[0][i], GPIO.IN)

    for i in range(4):
        GPIO.output(pines[1][i], GPIO.HIGH);
    y = 5; 
    while y == 5:
        for i in range(4):
            p = GPIO.input(pines[0][i]);
            if p == 1:
                y = i;
    return resultado[x][y];

def verifyWrite():
    last = 0;
    while 1:
        p = write()
        if p==last:
            break;
        last = p
        sleep(0.01)
    while 1:
        numero = 0;
        for i in range(4):
            numero = numero + GPIO.input(pines[0][i]);
        if numero==0:
            break
    return last



conn = sqlite3.connect("/var/www/html/basededatos.sql");
c = conn.cursor()
GPIO.setup(16,GPIO.OUT);#Verde
GPIO.setup(18,GPIO.OUT);#Rojo
GPIO.setup(29,GPIO.OUT);#Usuario activo
while 1:
    sleep(1);
    GPIO.output(16, GPIO.LOW);
    GPIO.output(18, GPIO.LOW);
    GPIO.output(29, GPIO.LOW);
    salir = 0;
    user = ""
    while 1:
        cha = verifyWrite()
        if cha == 'V':
            if len(cha)==0:
                continue
            break
        elif cha == 'X':
            salir =1;
            break
        elif cha != 'N':
            user = user + cha

    if salir == 1:
        continue

    print "user "+user
    passwd = c.execute("SELECT pass FROM usuaris WHERE id ="+user+";").fetchall()

    if len(passwd) == 0:
        GPIO.output(18, GPIO.HIGH);
        sleep(1)
        continue

    GPIO.output(29, GPIO.HIGH);
    passwd = passwd[0][0]
    print "pass "+passwd
    size = len(passwd)
    print size
    contra = ""
    cha = ""
    while size != 0: 
        cha = verifyWrite()
        if cha == 'V':
            break
        elif cha == 'X':
            salir =1;
            break
        elif cha != 'N':
            contra = contra + cha
            size = size - 1
    if salir == 1:
        continue
    print contra
    print passwd
    if contra == passwd:
        GPIO.output(16, GPIO.HIGH);
        c.execute("INSERT INTO autenticacio VALUES(DATETIME('now'),"+user+",1)");
    else:
        GPIO.output(18, GPIO.HIGH);
        c.execute("INSERT INTO autenticacio VALUES(DATETIME('now'),"+user+",0)");
    conn.commit();
    sleep(5)

resu = 0;
print verifyWrite()
GPIO.cleanup()

