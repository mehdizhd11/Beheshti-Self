from Back import *

food = 'کباب-نیم پرس'

print(food)

if food.find('-نیم پرس'):
    
    food = food.replace('-نیم پرس', '')
    
    print(food)