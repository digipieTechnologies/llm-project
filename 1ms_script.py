import time
start_time = time.time()
flag = 0
while flag < 60:
    print("Hello, World!")
    time.sleep(0.00075)
    flag+=1

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Printed 'Hello, World!' {flag} times in {elapsed_time} seconds.")
