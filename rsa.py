import random

# Function to check prime
def is_prime(num):
    for i in range(2,int(num/2)+1):
        if(num % i == 0):
            return False
            break
    return True   

# Function to check G.C.D
def gcd(i,j):
    if(j == 0):
        return i
    else:
        return gcd(j,i%j)

# Function to find modular inverse
def modular_inverse(x,y):
    for i in range(y):
        if (x*i)%y==1:
            return i

# Function to generate random prime numbers
def generate_random_numbers():
    count = 0 
    prime_number = []
    while count < 10:
        num = random.getrandbits(16)
        if is_prime(num):
            prime_number.append(num)
            count += 1
    return prime_number

# Function to generate random public key
def generate_public_key (phi_N) -> int:
    while True:
        num = random.randint(2,phi_N)

        if (gcd(num,phi_N)==1):
            return num

# Function to generate private key
def generate_private_key (E,phi_N):
    D = modular_inverse(E,phi_N)
    return D

# Function to find modulus
def square_and_multiply(base,exp,mod):
    res = 1
    bin_exp = bin(exp)[2:]

    for i in bin_exp:
        res = (res * res) % mod

        if i == '1':
            res = (res * base) % mod
    return res

#Function to convert string as integer
def strings_to_hex_and_int(str_list):
    hex_int_list = []
    for chunk in str_list:
        hex_chunk = ""
        for char in chunk:
            hex_value = hex(ord(char))[2:]  # Convert character to hex
            hex_chunk += hex_value
        hex_int_list.append(int(hex_chunk, 16))  # Convert hex to int and add to the list
    return hex_int_list  

def encrypt_message(Plain_text,e,N):

    Plain_text_list = [(Plain_text[i:i+3]) for i in range (0,len(Plain_text),3)]

    print(Plain_text_list)

    Plain_text_int = strings_to_hex_and_int (Plain_text_list)

    Encrypted_list = []

    for i in Plain_text_int:
    
        c = square_and_multiply(i,e,N)

        Encrypted_list.append(c)

    print("\nThe Encrypted Message is: ")
        
    print(*Encrypted_list)

def decrypt_message(n, d, cipher_msg):
    cipher_int = [int(x) for x in cipher_msg.split(',')]
    x = []
    for num in cipher_int:
        x.append(hex(square_and_multiply(num, d, n))[2:].upper())
    r = []
    for word in x:
        r.append(bytes.fromhex(word).decode('utf-8'))
    print("\n",r)
    print("\nThe Decrypted Message is: ")
    for k in r:
        print(k,end="")
    print("\n")



def signature(N,private_key,Name):
    result = []
    chunks = [name[i:i + 3] for i in range(0, len(Name), 3)]
    print(chunks)
    hex_chunks = []
    for w in chunks:
        hex_chunks.append(w.encode('utf-8').hex())
    chunks = []
    for hex_num in hex_chunks:
        chunks.append(int(hex_num, 16))
    for text_num in chunks:
        x = square_and_multiply(text_num, private_key, N)
        result.append(x)
    print("\nYour Digital Signature is ")
    print(*result)


def verify_signature(n, public_key, signature, sender):
    msg = [int(x) for x in signature.split(',')]
    x = []
    for num in msg:
        x.append(square_and_multiply(num, public_key, n))
    hex_num = []
    for num in x:
        hex_num.append(hex(num)[2:].upper())
    result = []
    for word in hex_num:
        result.append(bytes.fromhex(word).decode('utf-8'))
    if "".join(result) == sender:
        print("\nTHE SIGNATURE IS VALID.")



if __name__ == "__main__":

    print("Enter (y) if you have P and Q or Enter (n): ")

    Option = input().lower()
    if (Option=='y'):
        print("Enter your P: ")
        P = int(input())
        print("\nEnter your Q: ")
        Q = int(input())
        print("\nEnter your e (public-Key):")
        e = int(input())
        N = P*Q
        print("\nValue of N: ",N)
        phi_N = (P-1)*(Q-1)
        print("\nValue of Phi(N): ",phi_N)
        private_key = generate_private_key(e, phi_N)
        print("\nYour Private Key: ",private_key)

    elif (Option == 'n'):
        prime_number = generate_random_numbers()

        print (prime_number)

        print ("Choose any two numbers and pass them as the inputs")
        print("Enter P: ")
        P = int(input())
        print("Enter Q: ")
        Q = int(input())
        N = P*Q
        print("Value of N: ",N)
        phi_N = (P-1)*(Q-1)
        print("Value of Phi(N): ",phi_N)
        e =generate_public_key(phi_N)
        print("Public Key: ",e)
        private_key = generate_private_key(e, phi_N)
        print("\nYour Private Key: ", private_key)
    
    

    print("\nEnter your Partner's N and e as (N,e): ")
    pN,pE = map(int,input().split(","))


    print("\nEncryption Process")

    print("\nEnter your message to be encrypted: ")

    Plain_text = input()

    Cipher_int = encrypt_message(Plain_text,pE,pN)

    print("\nDecryption Process")

    print("\nEnter the encrypted message from your partner: ")

    Cipher_msg = input().strip("[ ]")

    decrypt_message(N,private_key,Cipher_msg)

    print("\nSignature Process")

    print("\nEnter your name to sign: ")

    name = input()

    signature(N,private_key,name)

    print("\nVerify Signature")

    p_signature = input("\nEnter your partner's signature here: \n").strip("[]").replace(", ", ",")
    pname = input("\nEnter your partner's name here:\n")
    verify_signature(pN, pE, p_signature, pname)

exit()
























    
    




    
    
    

