import statistics
n = 14

change = (EURGBP_Data["Price"] - EURGBP_Data["Price"].shift(1))

Up = change > 0
Down = abs(change < 0)

average_up = statistics.mean([1:n = 1]) #NEED to create panda of ups and downs for this to work??? what you think Reza bro?
# above I am sorting if up of if down movement (need abs value but need to know if down or up) then need list these??

average_down = statistics.mean([1:n = 1])

RS = average_up / average_down


"""
Up = [15, 9, 55, 41, 35, 20, 62, 49]
Down = [3, 6, 2, 9, 1, 15, 20, 50]

x = statistics.mean(Up)
y = statistics.mean(Down)

RS = x / y

RSI = 100 - (100 / (RS + 1))
print(RSI) """