from tools.Bot import Bot

monitor = int(input('Select Monitor: '))
restart = input('Restart? [y/n]: ')

if restart != 'y' and restart != 'n':
    print('\nError!')
    print('Select y/n for restart option')
    
else:
    bot = Bot(monitor, restart)
    bot.bot_sequence()