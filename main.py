import xlsxwriter
import telebot
from telebot.types import LabeledPrice, ShippingOption
from telebot import types

token = ''
provider_token = ''  # @BotFather -> Bot Settings -> Payments
bot = telebot.TeleBot(token)

prices = [LabeledPrice(label='Caffeine - Sunburst Orange', amount=65000), LabeledPrice('Winter Discount', -5100)]

shipping_options = [
    ShippingOption(id='novaposhta', title='Нова пошта').add_price(LabeledPrice('Нова пошта', 5000)),
    ShippingOption(id='justin', title='Justin').add_price(LabeledPrice('Justin', 4000))]


# Reply on /start command by implementing inline buttons
@bot.message_handler(commands=['start'])
def command_start(message):
    markup = types.InlineKeyboardMarkup()

    # switch_inline_query_current_chat for prefill text for user to edit
    item1 = types.InlineKeyboardButton(text='\U0001F31F Асортимент', switch_inline_query_current_chat='products')
    item2 = types.InlineKeyboardButton(text='\U0001F50D Зробити заказ', switch_inline_query_current_chat='switch_order',
                                       callback_data='order')
    item3 = types.InlineKeyboardButton(text='\U0001F50D FAQ', switch_inline_query_current_chat='switch_faq',
                                       callback_data='faq')

    markup.add(item1, item2).add(item3)

    welcome_message = \
        'Привіт, {0.first_name} \U0001F609 \n' \
        'Ми дуже раді вітати вас на борту uphealth! \U0001F389 \n \n' \
        '_Натисніть клавішу на нижній клавіатурі, щоб вибрати потрібну операцію_'

    bot.send_message(message.chat.id, welcome_message.format(message.from_user), parse_mode='Markdown',
                     reply_markup=markup)


@bot.inline_handler(lambda query: query.query == 'products')
def query_text(inline_query):
    try:

        caffeine_desc = \
            'Інгалятори виготовлені на основі кофеїну фармацевтичного класу та овочевої основи. В продуктах не містяться такі речовини як: нікотин, вітамін Е та пропіленгліколь. \n \n' \
            'Caffeine Sunburst Orange розрахований на 300 вдохів з 6.5mg кофеїну'
        r = types.InlineQueryResultArticle(
            id="1",
            title="Caffeine - Sunburst Orange",
            thumb_url='https://cdn.shopify.com/s/files/1/1863/2347/products/Vert-CaffeineSunburst_770x@2x.png?v=1639187035',
            input_message_content=types.InputTextMessageContent("Caffeine - Sunburst Orange"),
            description=caffeine_desc
        )

        r2 = types.InlineQueryResultArticle(
            id="2",
            title="Melatonin Lavender Dream",
            thumb_url='https://cdn.shopify.com/s/files/1/1863/2347/products/vert-lavender-dream_770x@2x.png?v=1639426732',
            input_message_content=types.InputTextMessageContent("Melatonin Lavender Dream"),
            description="Inhale Health® забезпечує ідеальну дозу нічного мелатоніну, який швидко поглинається, щоб ви могли легко відійти."
        )

        r3 = types.InlineQueryResultArticle(
            id="3",
            title="B12 Strawberry Fields",
            thumb_url='https://cdn.shopify.com/s/files/1/1863/2347/products/Vert-StrawberryFields_770x@2x.png?v=1639185078',
            input_message_content=types.InputTextMessageContent("B12 Strawberry Fields"),
            description="Вітамін B12 Strawberry Fields™ поєднує нотки свіжої полуниці та тонкого ківі."
        )

        bot.answer_inline_query(inline_query.id, [r, r2, r3])
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['text'])
def command_pay(message):
    if message.chat.type == 'private':
        if message.text == 'Caffeine - Sunburst Orange':
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton("Оплатити", pay=True))
            keyboard.add(types.InlineKeyboardButton("<<  Назад", callback_data="cb_data_1"),
                         (types.InlineKeyboardButton("Наступне  >>", callback_data="cb_data_2")))
            keyboard.add(types.InlineKeyboardButton("Головне меню", callback_data="main_menu",
                                                    switch_inline_query_current_chat='True'))

            desc_message = \
                'Інгалятори виготовлені на основі кофеїну фармацевтичного класу та овочевої основи. В продуктах не містяться такі речовини як: нікотин, вітамін Е та пропіленгліколь. \n \n' \
                'Caffeine Sunburst Orange розрахований на 300 вдохів з 6.5mg кофеїну'

            bot.send_invoice(message.chat.id, title='Caffeine - Sunburst Orange',
                             description=desc_message,
                             provider_token=provider_token,
                             currency='uah',
                             photo_url='https://cdn.shopify.com/s/files/1/1863/2347/products/Vert-CaffeineSunburst_770x@2x.png?v=1639187035',
                             photo_height=512,  # !=0/None or picture won't be shown
                             photo_width=512,
                             photo_size=512,
                             is_flexible=True,  # True If you need to set up Shipping Fee
                             prices=prices,
                             start_parameter='time-machine-example',
                             invoice_payload='true',  # I have no fucking idea what is this, figure out!
                             need_email=True,
                             need_phone_number=True,
                             reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        if call.data == 'main_menu':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            item1 = types.KeyboardButton('\U0001F31F Асортимент')
            item2 = types.KeyboardButton('\U0001F4AC Контакти')
            item3 = types.KeyboardButton('\U0001F50D FAQ')

            markup.add(item1, item2).add(item3)

            welcome_message = '_Натисніть клавішу на нижній клавіатурі, щоб вибрати потрібну операцію_'

            bot.send_message(message.chat.id, welcome_message.format(message.from_user), parse_mode='Markdown',
                             reply_markup=markup)


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options)


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):

    # Convert to SQLite
    print('order_info')
    print(pre_checkout_query.order_info)
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id,
                     'Hoooooray! Thanks for payment! We will proceed your order for `{} {}` as fast as possible! '
                     'Stay in touch.\n\nUse /buy again to get a Time Machine for your friend!'.format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')


bot.infinity_polling(skip_pending=True)
