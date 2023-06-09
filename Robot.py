
from Back import *

from Robot import *

from telebot import *

from persiantools import digits

TOKEN = '6254025537:AAGT8c4OYPdzGH5r2Y1y3wged0ENLIvNcc0'

schedule.every().day.at('00:30').do(Code.clearList)

while True:
    
    schedule.run_pending()
    
    sleep(5)
    
    try:
        
        bot = TeleBot(token=TOKEN)
        
        @bot.message_handler(commands=['start' , 'restart'])
        
        def start_bot(message):
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
            
            item1 = types.KeyboardButton('فروش کد')
            
            item2 = types.KeyboardButton('خرید کد')
            
            item3 = types.KeyboardButton('نحوه عملکرد ربات')
            
            markup.add(item1,item2,item3)
            
            bot.send_message(message.chat.id, 'یک گزینه را انتخاب کنید' , reply_markup=markup)
            
        @bot.message_handler(content_types=['text'])
        
        def handle_start(message):
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True , row_width=1)
            
            item1 = types.KeyboardButton('ناهار')
            
            item2 = types.KeyboardButton('شام')
            
            markup.row(item1,item2)
            
            if message.text == 'فروش کد':
                
                bot.send_message(message.chat.id, 'تایید شد' , reply_markup=markup)
                
                meal = bot.reply_to(message, 'وعده مورد نظر را انتخاب کنید')
                
                bot.register_next_step_handler(meal, seller_meal)
                
            elif message.text == 'خرید کد':
                
                bot.send_message(message.chat.id, 'تایید شد' , reply_markup=markup)
                
                meal = bot.reply_to(message, 'وعده مورد نظر را انتخاب کنید')
                
                bot.register_next_step_handler(meal, buyer_meal)
                
            elif message.text == 'نحوه عملکرد ربات':
                
                about = '--- ربات با گرفتن شماره دانشجویی و کد ملی فروشنده ، به صورت خودکار کد فراموشی غذای رزرو شده را از سایت دریافت کرده و در صورت تایید در لیست کد ها قرار می‌دهد /\n--- پس از درخواست خریدار برای خرید کد ، کد فروشنده مجددا با سایت چک می‌شود و پس از دریافت شماره دانشجویی و کد ملی خریدار ، مبلغ غذا از حساب خریدار برداشته و به حساب فروشنده واریز می‌شود و کد برای خریدار فعال می‌شود /\n--- هزینه خرید کد رستوران مکمل ۱۰ هزار تومان و دریافتی فروش کد رستوران مکمل مبلغ ۶ هزار تومان است /\n--- در باقی سلف ها هزینه خرید و فروش برابر مبلغ غذا است /\n--- Code: @mehdizhd11 \n--- Source: https://github.com/mehdizhd11/Beheshti-Self \n--- & Thanks to the friends who helped  ❤️'
                
                bot.send_message(message.chat.id, text=about)
                
                bot.send_message(message.chat.id, '/restart')
                
                return
            
            else:
                
                bot.send_message(message.chat.id, '/restart') 
                
                return
                
        def seller_meal(mealText):
            
            meal = mealText.text
            
            if meal == 'ناهار' or meal == 'شام':
            
                studentId = bot.reply_to(mealText, 'شماره دانشجویی خود را وارد کنید')
            
                bot.register_next_step_handler(studentId, seller_studentId , meal)
                
            else:
                
                bot.send_message(mealText.chat.id, 'خطا')
                
                bot.send_message(mealText.chat.id, '/restart')
                
                return
                
        def seller_studentId(studentIdText,*args):
            
            meal = args[0]
            
            studentId = studentIdText.text
            
            studentId = digits.fa_to_en(studentId)
            
            if studentId.isnumeric() == False:
                
                bot.send_message(studentIdText.chat.id, 'شماره دانشجویی اشتباه است')
                
                bot.send_message(studentIdText.chat.id, '/restart')
                
                return
            
            studentId = int(studentId)
            
            idNumber = bot.reply_to(studentIdText, 'شماره ملی خود را وارد کنید')
            
            bot.send_message(studentIdText.chat.id, 'بعد از ارسال کد ملی ، پردازش اطلاعات و ثبت کد ممکن است به دلایل فنی طولانی بشود . پس از پردازش ، ربات به شما پیام خواهد داد . منتطر بمانید')

            bot.register_next_step_handler(idNumber, seller_idNumber , studentId , meal)
            
        def seller_idNumber(idNumberText , *args):
            
            studentId = args[0]
            
            meal = args[1]
            
            idNumber = idNumberText.text

            idNumber = digits.fa_to_en(idNumber)
            
            if idNumber.isnumeric() == False:
                
                bot.send_message(idNumberText.chat.id, 'شماره ملی اشتباه است')
                
                bot.send_message(idNumberText.chat.id, '/restart')
                
                return
            
            idNumber = int(idNumber)
            
            seller = Seller(code=None, studentId=studentId, idNumber=idNumber, meal=meal, checked=False, payedTo=False, chatId=idNumberText.chat.id)
            
            if Seller.findCode(seller):
                
                bot.send_message(seller.chatId, 'کد شما در لیست فرار گرفت')
                
                bot.send_message(seller.chatId, 'در صورت فروش ، ربات مبلغ غذا را به حساب شما واریز و به شما اطلاع خواهد داد')
                
                bot.send_message(idNumberText.chat.id, '/restart')
                
                return
            
            else:
                
                bot.send_message(idNumberText.chat.id, 'خطا ! اطلاعات ارسال شده خود و رزرو بودن غذا را بررسی و مجددا تلاش کنید')
                
                bot.send_message(idNumberText.chat.id, '/restart')
                
                return

        def buyer_meal(mealText):
            
            meal = mealText.text
            
            if meal == 'ناهار' or meal == 'شام':
                
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=5)

                item1 = types.KeyboardButton('بهشتی مرکزی برادران')

                item2 = types.KeyboardButton('بهشتی مرکزی خواهران')

                item3 = types.KeyboardButton('بهشتی کوی پسران')

                item4 = types.KeyboardButton('بهشتی کوی دختران')

                item5 = types.KeyboardButton('عباسپور مرکزی برادران')

                item6 = types.KeyboardButton('عباسپور مرکزی خواهران')

                item7 = types.KeyboardButton('عباسپور کوی پسران')

                item8 = types.KeyboardButton('عباسپور کوی دختران')

                item9 = types.KeyboardButton('رستوران مکمل دانشجویی')

                markup.row(item1,item2)
                
                markup.row(item3,item4)
                
                markup.row(item5,item6)
                
                markup.row(item7,item8)
                
                markup.row(item9)

                bot.send_message(mealText.chat.id, 'تایید شد' , reply_markup=markup)

                room = bot.reply_to(mealText, 'سلف مورد نظر را انتخاب کنید')

                bot.register_next_step_handler(room, buyer_room , meal)
                
            else:
                
                bot.send_message(mealText.chat.id, 'خطا')
                
                bot.send_message(mealText.chat.id, '/restart')
                
                return
            
        def buyer_room(roomText , *args):
            
            meal = args[0]
            
            room = roomText.text
            
            if room == 'بهشتی مرکزی برادران':
                
                room = 'BMB'
                
            elif room == 'بهشتی مرکزی خواهران':
                
                room = 'BMG'
                
            elif room == 'بهشتی کوی پسران':
                
                room = 'BDB'
                
            elif room == 'بهشتی کوی دختران':
                
                room = 'BDG'
                
            elif room == 'عباسپور مرکزی برادران':
                
                room = 'AMB'
                
            elif room == 'عباسپور مرکزی خواهران':
                
                room = 'AMG'
                
            elif room == 'عباسپور کوی پسران':
                
                room = 'ADB'
                
            elif room == 'عباسپور کوی دختران':
                
                room = 'ADG'
                
            elif room == 'رستوران مکمل رانشجویی':
                
                room = 'MKL'
                
            else:
                
                bot.send_message(roomText.chat.id, 'خطا')
                
                bot.send_message(roomText.chat.id, '/restart')
                
                return
            
            buyer = Buyer(code=None, studentId=0, idNumber=0, meal=meal, room=room, isPayed=False, chatId=roomText.chat.id)
            
            enableCodes = Buyer.findCodesList(buyer)
            
            if len(enableCodes) < 1:
                
                bot.send_message(buyer.chatId, 'در حال حاضر کدی برای این سلف موجود نیست')
                
                bot.send_message(buyer.chatId, '/restart')
                
                return
            
            else:
                
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=len(enableCodes))
                
                for idx in range(len(enableCodes)):
                    
                    if enableCodes[idx].completed:
                        
                        markup.row(types.KeyboardButton(f'{enableCodes[idx].food}'))
                        
                    else:
                        
                        markup.row(types.KeyboardButton(f'{enableCodes[idx].food}-نیم پرس'))
            
                bot.send_message(roomText.chat.id, 'تایید شد' , reply_markup=markup)
                
                food = bot.reply_to(roomText, 'یک گزینه را انتخاب کنید')
                
                bot.register_next_step_handler(food, buyer_food , meal , room , buyer)
                
        def buyer_food(foodText , *args):
            
            meal = args[0]
            
            room = args[1]
            
            buyer = args[2]
            
            food = foodText.text
            
            completed = True
            
            if food.find('-نیم پرس'):
                
                food = food.replace('-نیم پرس', '')
                
                completed = False
                
            findCode = Buyer.findCode(buyer, food=food, completed=completed)
            
            if findCode:
                
                studentId = bot.reply_to(foodText, 'یک کد برای شما پیدا شد . یرای پرداخت هزینه شماره دانشجویی خود را وارد کنید')
                
                bot.register_next_step_handler(studentId, buyer_studentId , buyer)
            
            else:
                
                bot.send_message(foodText.chat.id, 'کدی پیدا نشد')
                
                bot.send_message(foodText.chat.id, '/restart')
                
                return
            
        def buyer_studentId(studentIdText , *args):
            
            buyer = args[0]
            
            studentId = studentIdText.text
            
            studentId = digits.fa_to_en(studentId)
            
            if studentId.isnumeric() == False:
                
                bot.send_message(studentIdText.chat.id, 'شماره دانشجویی اشتباه است')
                
                bot.send_message(studentIdText.chat.id, '/restart')
                
                return
            
            studentId = int(studentId)
            
            idNumber = bot.reply_to(studentIdText, 'شماره ملی خود را وارد کنید')
            
            bot.send_message(studentIdText.chat.id, 'بعد از ارسال کد ملی ، پردازش اطلاعات و ثبت کد ممکن است به دلایل فنی طولانی بشود . پس از پردازش ، ربات به شما پیام خواهد داد . منتطر بمانید')

            bot.register_next_step_handler(idNumber, buyer_idNumber , studentId , buyer)
            
        def buyer_idNumber(idNumberText , *args):
            
            studentId = args[0]
            
            buyer = args[1]
            
            idNumber = idNumberText.text

            idNumber = digits.fa_to_en(idNumber)
            
            if idNumber.isnumeric() == False:
                
                bot.send_message(idNumberText.chat.id, 'شماره ملی اشتباه است')
                
                bot.send_message(idNumberText.chat.id, '/restart')
                
                return
            
            idNumber = int(idNumber)
            
            buyer.studentId = studentId
            
            buyer.idNumber = idNumber
            
            if Buyer.payment(buyer):
                
                bot.send_message(buyer.chatId, f'{buyer.code.num}')
                
                Seller.payment(buyer.code.seller)
                
                bot.send_message(buyer.code.seller.chatId , 'کد شما فروخته شد و مبلغ آن به حساب شما واریز شد')
                
                bot.send_message(buyer.code.seller.chatId, '/restart')
                
                return
                
            else:
                
                bot.send_message(idNumberText.chat.id, 'پرداخت ناموفق بود . اطلاعات و موجودی حساب خود را بررسی و مجددا تلاش کنید')
                
                bot.send_message(idNumberText.chat.id, '/restart')
                
                return
        
        bot.polling(non_stop=True)  
            
    except:
        
        pass