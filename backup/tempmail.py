from mailtm import Email

file_path = './routines/mail_settings.txt'

bool_stop_listener = False

def listener(message):
    if(message['subject']):
        instagram_code = message['subject'].split()[0]
        with open(file_path, 'a') as file:
            file.write(instagram_code)
        bool_stop_listener = True

def _init():
    # Get Domains
    test = Email()
    print("\nDomain: " + test.domain)

    # Make new email address
    test.register()
    print("\nEmail Adress: " + str(test.address))
    with open(file_path, 'w') as file:
        file.write(test.address +'\t')

    # Start listening
    test.start(listener)
    print("\nWaiting for new emails...")
    if bool_stop_listener is True:
        test.stop()

_init()