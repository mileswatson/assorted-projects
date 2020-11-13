from random import randint

##############################################################

#[username,[password, public_key, identifier, [account_name1,account_balance1,], first_name, second_name, is_open, tries]]

#username password 161417
#administrator bank 709609
#DrWatson321 lost51 88807
#############################################################
customer_data = ['new', ['account'], 'recover', ['password'], 'username', ['29ga 5qw5 1ng7 37z 294u 688v 2e64 6ia0', 208553, 417091, ['37z 5qw5 28w7 5q7a 2e64', '5x0u'], '1ng7 688v 198y 1ng7', '6eci 5qw5 5q7a 2k5t', True, 0]]
current_data = []
location = 0
user = "new"
logged_in = False
current_password = ""

##############################################################
def is_int(integer):
  try: 
    int(integer)
    return True
  except ValueError:
    return False

def baseN(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
  return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def login():
  global location
  global user
  global current_password
  global customer_data
  user = input("User: ")
  if user in customer_data:
    user_found = True
    location = customer_data.index(user)
  else:
    user_found = False
    location = 0
    password = input("Password: ")
    account_status = False
  if user != "new" and user != "recover" and user_found:
    account_status = customer_data[location+1][6]
    if account_status:
      password = input("Password: ")
      encrypted_password = (customer_data[location + 1])[0]
      public_key = (customer_data[location + 1])[1]
      identifier = (customer_data[location + 1])[2]
      while not ((user_found == True) and (encrypt(password, public_key, identifier) == encrypted_password)):
        clear()
        if user_found:
          customer_data[location + 1][7] += 1
          print(customer_data[location + 1][7])
        print("Incorrect username/password.")
        customer_data[location + 1][7] += 1
        user = input("User: ")
        password = input("Password: ")
        if user in customer_data:
          user_found = True
          location = customer_data.index(user)
        else:
          user_found = False
          location = 0
      current_password = password
      return True
    else:
      clear()
      print(customer_data[location + 1][7])
      print("Username/Password is incorrect.")
      customer_data[location + 1][7] += 1
  else:
    clear()
    password = ""
    if user == "recover" or user == "new":
      return True
    elif user_found:
      customer_data[location + 1][7] += 1
      print(customer_data[location + 1][7])
    print("Incorrect username/password.")
    current_password = password

def create_account():
  global customer_data
  create_user = ""
  create_password1 = "1"
  create_password2 = "2"
  create_user = "new"
  while create_user in customer_data:
    create_user = input("What would you like your username to be? ")
  while create_password1 != create_password2:
    create_password1 = input("Enter your password: ")
    create_password2 = input("Re-enter your password: ")
  create_name1 = input("What is your first name? ")
  create_name2 = input("What is your second name? ")
  vault_name = input("What would you like to call your default vault?")
  keys = get_keys()
  private_key = keys[2]
  public_key = keys[0]
  identifier = keys[1]
  balance = "0"
  create_password1 = encrypt(create_password1,public_key,identifier)
  create_name1 = encrypt(create_name1, public_key, identifier)
  create_name2 = encrypt(create_name2, public_key, identifier)
  vault_name = encrypt(vault_name,public_key,identifier)
  balance = encrypt(balance, public_key, identifier)
  print("IMPORTANT! YOUR USERNAME IS " + str(create_user) + ", YOUR PASSWORD IS THE ONE YOU SET AND YOUR PRIVATE KEY IS " + str(private_key) + ". DO NOT FORGET THESE DETAILS!")
  continue1 = input("Do you want to continue? Y/N")
  if continue1 == "Y" or continue1 == "y":
    customer_data.append(create_user)
    customer_data.append([create_password1, public_key, identifier, [vault_name, balance], create_name1, create_name2, True, 0])
    create_user = ""
    create_password1 = ""
    create_password2 = ""
    create_name1 = ""
    create_name2 = ""
    keys = ""
    private_key = ""
    public_key = ""
    identifier = ""
    print("Goodbye.")
    logged_in = False
    user = ""
  else:
    print("Values wiped.")
    create_user = ""
    create_password1 = ""
    create_password2 = ""
    create_name1 = ""
    create_name2 = ""
    keys = ""
    private_key = ""
    public_key = ""
    identifier = ""
    print("Goodbye.")
    logged_in = False
    user = ""

def get_prime(start_num):
  start_num -= 2
  prime_num = 5
  if start_num % 2 == 0:
    start_num = start_num + 1
  found = False
  test_num = start_num
  while found == False:
    test_num += 2
    limit = round(test_num ** 0.5)
    test_for = 1
    prime = True
    while test_for <= limit:
      test_for += 2
      if test_num % test_for == 0:
        prime = False
        test_for = limit + 1
    if prime == True:
      prime_num = test_num
      found = True
  return(prime_num)
  
def get_keys():
  area_specific_value = randint(111,999)
  p = get_prime(area_specific_value)
  area_specific_value = randint(111,999)
  q = get_prime(area_specific_value)
  n = p * q
  totient_n = (p-1) * (q-1)
  area_specific_value = round(n / 2)
  e = get_prime(area_specific_value)
  loop = True
  d = 1
  while loop == True:
    x = (e * d - 1) % totient_n
    if x == 0:
      loop = False
    else:
      d += 1
  return [e,n,d]
  
def encrypt(string, key,identifier,):
  numbers = []
  string = list(string)
  length = len(string)
  per_letter = 100 / length
  percent = 0
  print("Please wait whilst we authenticate/encrypt your data...")
  print("0%")
  for i in range (0,length):
    numbers.append(baseN((((int(ord(string[i]))+(i + 1)) ** key) % identifier), 36))
    percent = round(percent + per_letter)
    clear()
    print("Please wait whilst we authenticate/encrypt your data...")
    print(str(percent) + "%")
  clear()
  return " ".join(numbers)

def decrypt(string, key, identifier):
  numbers = []
  string = string.split()
  length = len(string)
  per_letter = 100 / length
  percent = 0
  print("Please wait whilst we retrieve/decrypt your data...")
  print("0%")
  for i in range (0,length):
    numbers.append(chr(int(((((int(string[i], 36)) ** int(key)) % int(identifier)) - (i+1)))))
    percent = round(percent + per_letter)   
    clear()
    print("Please wait whilst we retrieve/decrypt your data...")
    print(str(percent) + "%")
  clear()
  return "".join(numbers)

def get_private_key():
  private_key = input("Enter your private key: ")
  while not is_int(private_key):
    clear()
    print("That is not an integer.")
    private_key = input("Enter your private key: ")
  return int(private_key)

def num_after_point(x):
    s = str(x)
    if not '.' in s:
        return 0
    return len(s) - s.index('.') - 1

def clear():
  print("\n" * 50)

def line():
  print()
###############################################################

while True:
  clear()
  if login():
    logged_in = True
    while logged_in == True:
      if user == "new":
        continue1 = input("Are you sure you want to create a new account? Y/N")
        if continue1 == "Y" or continue1 == "y":
          create_account()
          logged_in = False
        else:
          logged_in = False
          user = ""
      elif user == "administrator":
        print("ADMIN")
        input()
      elif user == "recover":
        test_user = input("Enter your username: ")
        while test_user == "new" or test_user == "recover" or test_user == "admin" or not test_user in customer_data:
          print("That user does not exist.")
          test_user = input("Enter your username: ")
        location = customer_data.index(test_user)
        encrypted_password = (customer_data[location + 1])[0]
        identifier = (customer_data[location + 1])[2]
        private_key = get_private_key()
        decrypted_password = decrypt(encrypted_password, private_key, identifier)
        print("Your password is " + decrypted_password)
        input()
        logged_in = False
        user = ""
      else:
        balance = customer_data[location+1][3]
        public_key = int(customer_data[location+1][1])
        identifier = int(customer_data[location+1][2])
        decrypted_password = 0
        print(customer_data[location + 1][7])
        private_key = get_private_key()
        decrypted_password = decrypt(customer_data[location+1][0], private_key, identifier)
        while decrypted_password != current_password:
          customer_data[location + 1][7] += 1
          print(customer_data[location + 1][7])
          private_key = get_private_key()
          decrypted_password = decrypt(customer_data[location+1][0], private_key, identifier)
        logged_in = True
        while logged_in == True:
          clear()
          print("Would you like to: ")
          print(" 1. View your vaults")
          print(" 2. Enter a top-up code")
          print(" 3. Logout")
          answer = input()
          if answer == "1":
            encrypted_vault_data = customer_data[location+1][3]
            number_of_vaults = len(encrypted_vault_data)
            decrypted_vault_data = []
            for i in range(0,number_of_vaults):
              decrypted_vault_data.append(decrypt(encrypted_vault_data[i],private_key,identifier))
            for i in range(0,int(len(encrypted_vault_data) / 2)):
              balance = decrypted_vault_data[(i * 2)+1]
              balance = float(balance)
              if num_after_point(balance) == 1:
                balance = str(balance) + "0"
              else:
                balance = str(balance)
              print(str(i + 1) + ". " + decrypted_vault_data[i * 2] + " - £" + balance)
            input()
          elif answer == "2":
            clear()
            answer = input("Enter your top-up code: ")
          elif answer == "3":
            logged_in = False