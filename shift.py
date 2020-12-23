import sys

def binDigits(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)

def binaryToDecimal(n): 
    return int(n,2) 

def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0: 
        val = val - (1 << bits)        
    return val                         

def addBin(x,y):
    sum = bin(int(x,2) + int(y,2))
    return sum[2:len(sum)]

def shiftmul(x,y):
    print("Shift and Add Multiplication")
    yLen = len(bin(y))-2
    xLen = len(bin(x))-2
    if(yLen < xLen):
        q = binDigits(y, xLen)
        aa = binDigits(x, xLen)
    else:
        q = binDigits(y, yLen)
        aa = binDigits(x, yLen)
    a = ""
    for w in q:
        a += "0"
    
    c = 0
    aLen = len(a)
    firstadd = False
    print("C\tA\t\tQ\t\tStep")
    print("==================================================================")
    for index, z in enumerate(q):
        if(q[len(q)-1] == "0"):
            print("\t" + a + "\t\t" + q + "\t\t(N=%d), Q0 = 0, don't add anything" % (len(q)-index))
            print("%d\t" % c + a + "\t\t" + q + "\t\tShift number right")
            print("------------------------------------------------------------------")
            q = a[len(a)-1] + q
            q = q[0:len(q)-1]
            if(firstadd and x<0):
                c = 1
            a = str(c) + a
            a = a[0:len(a)-1]
            c = 0
        else:
            print("\t" + a + "\t\t" + q + "\t\t(N=%d), Q0 = 1, Add A + %d" % ((len(q)-index), x))
            print("+\t" + aa)
            a = addBin(a,aa)
            if(len(a) > aLen):
                c = int(a[0])
                a=a[1:len(a)]
            else:
                for p in range(aLen-len(a)):
                    a = "0" + a
            print("%d\t" % c + a + "\t\t" + q + "\t\tShift number right")
            print("------------------------------------------------------------------")
            q = a[len(a)-1] + q
            q = q[0:len(q)-1]
            firstadd = True
            if(firstadd and x<0):
                c = 1
            a = str(c) + a
            a = a[0:len(a)-1]
            c = 0
    # Handles N = 0
    if(y>0):
        if x>0:
            print("\t" + a + "\t\t" + q + "\t\tFinal Answer: %d x %d = %d" %(x,y,binaryToDecimal(a+q)))
            if binaryToDecimal(a+q) != x*y:
                print("ERROR")
        else:
            print("\t" + a + "\t\t" + q + "\t\tFinal Answer: %d x %d = %d" %(x,y,twos_comp(int(a+q,2),len(a)+len(q))))
            if twos_comp(int(a+q,2),len(a)+len(q)) != x*y:
                print("ERROR")
        return
    else:
        print("\t" + a + "\t\t" + q + "\t\t(N=0) Subtract A-X (b/c X < 0)")
        x2Comp = binDigits(-1*x, len(a))
        print("+\t" + x2Comp)
        a = addBin(a,x2Comp)
        if(len(a) > aLen):
            c = int(a[0])
            a=a[1:len(a)]
        if x<0:
            print("\t" + a + "\t\t" + q + "\t\tFinal Answer: %d x %d = %d" %(x,y,binaryToDecimal(a+q)))
            if binaryToDecimal(a+q) != x*y:
                print("ERROR")
        else:
            print("\t" + a + "\t\t" + q + "\t\tFinal Answer: %d x %d = %d" %(x,y,twos_comp(int(a+q,2),len(a)+len(q))))
            if twos_comp(int(a+q,2),len(a)+len(q)) != x*y:
                print("ERROR")        
        return

def resdiv(x,y):
    print("Restoring Division")
    yLen = len(bin(y))-2
    xLen = len(bin(x))-2
    if(yLen < xLen):
        q = binDigits(x, xLen)
        aa = binDigits(y, xLen)
    else:
        q = binDigits(x, yLen)
        aa = binDigits(y, yLen)
    a = ""
    for w in range(len(q)+1):
        a += "0"
    aLen = len(a)
    aa2Comp = binDigits(-1*y, len(a))
    print("\tCA\t\t\tQ\t\tStep")
    print("==================================================================")
    for index, z in enumerate(q):
        print("\t" + a + "\t\t" + q + "\t\t(N=%d)" % ((len(q)-index)))
        a = a + q[0]
        a = a[1:len(a)]
        q = q[1:len(q)]
        q = q + "-"
        print("\t" + a + "\t\t" + q + "\t\tShift number left")
        print("+\t" + aa2Comp + "\t\t\t\tAC+2'sComp(M)")
        aTemp = addBin(a, aa2Comp)
        if len(aTemp) > aLen:
            aTemp = aTemp[1:len(aTemp)]
        if aTemp[0] == "1":
            print("\t" + aTemp + "\t\t" + q + "\t\tMSB = True")
            q = q[0:len(q)-1]
            q += "0"
        else:
            print("\t" + aTemp + "\t\t" + q + "\t\tMSB = False")
            q = q[0:len(q)-1]
            q += "1"
            a = aTemp
        print("------------------------------------------------------------------")
    # Handles N = 0
    print("\t" + a + "\t\t" + q + "\t\t(N=%d), Remainder = %d, Answer = %d" % (0,binaryToDecimal(a),binaryToDecimal(q)))

def main():
    if(len(sys.argv) < 3):
        try:
            x = int(input("Enter first numbers: "))
        except:
            x = 0
        try:
            y = int(input("Enter second numbers: "))
        except:
            y = 0
    else:
        x = int(sys.argv[1])
        y = int(sys.argv[2])

    while(True):
        if(len(sys.argv) == 4):
            op = int(sys.argv[3])
            break
        else:
            try:
                op = int(input("\nEnter operation:\n1. Shift and Add Multiplication\n2. Restoring Division\nChoice: "))
                if (op == 1 or op == 2):
                    print
                    break
                else:
                    print("Operation invalid")
            except:
                print("\nOperation invalid")

    if op == 1:
        shiftmul(x,y)
    elif op == 2:
        resdiv(x,y)

if __name__ == "__main__":
    main()