import statistics
n = 14

change = (EURGBP_Data["Price"] - EURGBP_Data["Price"].shift(1))

Up = change > 0
Down = abs(change < 0)

average_up = statistics.mean([1:n = 1]) #NEED to create panda of ups and downs for this to work??? what you think Reza bro?
# above I am sorting if up of if down movement (need abs value but need to know if down or up) then need list these??
#Firstly, I guess we need to pull the EURGBP_Data from what I downloaded - you got idea on how to do this?

for i in range(n+1):
    average_up_2 = (average_up[i-1]*(n-1) + up[i])/n

#hmm not sure about the above for loop, trying to make sure it continues to calc it... would need to repeat for down.

average_down = statistics.mean([1:n = 1])

RS = average_up / average_down

RSI = 100 - (100 / (RS + 1))


"""
Up = [15, 9, 55, 41, 35, 20, 62, 49]
Down = [3, 6, 2, 9, 1, 15, 20, 50]

x = statistics.mean(Up)
y = statistics.mean(Down)

RS = x / y

RSI = 100 - (100 / (RS + 1))
print(RSI) """