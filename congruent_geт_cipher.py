message = int(input())

a = 1023
b = 517
c = 523300
z = 777
iterations = 30

#
for i in range(25):
    z = (a * z + b) % c

cipher = z ^ message
print(cipher)
message = cipher ^ z
print(message)


