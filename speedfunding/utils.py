# -*- coding: utf-8 -*-

from speedfunding.gnupg_encrypt import encrypt_with_gnupg
from pyramid_mailer.message import Message


def make_donation_confirmation_emailbody(_input):
    """
    a mail body to confirm the submission
    """
    # DEBUG _input
    #import pprint
    #pprint.pprint(_input)

    d_key = {
        u'1': u'5',
        u'2': u'10',
        u'3': u'25',
        u'4': u'50',
        u'5': u'100',
        u'6': u'250',
        u'7': u'500',
        u'8': u'1000',
        u'9': u'2500',
        u'10': u'5000',
    }

    #print(
    #    "_input.locale is %s and type(_input.locale) is %s" % (
    #        _input.locale, type(_input.locale)))

    #import pprint
    #pprint.pprint(_input)
    #print d_key.get(_input.donation)

    if 'de' in _input.locale:  # GERMAN
        #print('lang is de')
        _body = (
            u"""Liebe_r Supporter_in,

vielen lieben Dank für Deine Unterstützung!

Wir freuen uns über Deine Spende über """ +
            d_key.get(_input.donation) +
            u""" EUR. Bitte überweise das Geld auf unser
Konto bei der

EthikBank eG
Kontoinhaber: C3S SCE
Verwendungszweck: Spende """ +
            _input.speed_id +
            u"""
BIC: GENO DE F1 ETK
IBAN: DE79830944950003264378

Kontonummer: 3264378
BLZ: 83094495

Sobald sie auf unserem Konto eingegangen ist,
geben wir Dir bescheid, damit Du weißt, ob alles seinen korrekten Lauf nimmt.

Bei Problemen kannst Du Dich gern melden bei Wolfgang (yes@c3s.cc)

Danke für Deine Mühe & Deinen Beitrag zur C3S!

Liebe Grüße

Das C3S-Team

""")

    else:  # NON-GERMAN --> ENG
        #print('lang is not de')
        _body = (
            u"""Dear supporter,

we just received your pledge to donate """ +
            d_key.get(_input.donation) +
            u""" EUR. Please transfer the money to our
bank account at

EthikBank eG
Account holder: C3S SCE
Reference: donation """ +
            _input.speed_id +
            u"""
BIC: GENO DE F1 ETK
IBAN: DE79830944950003264378

(old style account id below)
(Konto: 3264378 )
(BLZ: 83094495 )

Many heartfelt thanks for your support!

We highly appreciate your donation. As soon as it hits our bank account we will
notify you. Just so you know everything's going fine.

In case of any problems please don't hesitate to contact Wolfgang (yes@c3s.cc)

Thanks a lot for your effort & your contribution to C3S!

Best wishes

The C3S Team
""")
# email body must donation amount and contain speed_id

    return _body


def make_shirt_confirmation_emailbody(_in):
    #print("_in.locale is %s" % _in.locale)
    if 'de' in _in.locale:
        _body = (
            u"""Liebe_r Supporter_in,

vielen lieben Dank für Deine Unterstützung!

Du hast ein T-Shirt gewählt - das zeugt von gutem Geschmack. Wir geben Dir
bescheid, sobald Deine Bezahlung auf unserem Konto eingegangen ist, damit Du
weißt, ob alles seinen korrekten Lauf nimmt.

Bitte überweise 35 EUR auf unser Konto bei der

EthikBank eG
Kontoinhaber: C3S SCE
Verwendungszweck: Shirt """ +
            _in.speed_id +
            u"""
BIC: GENO DE F1 ETK
IBAN: DE79830944950003264378
Kontonummer: 3264378
BLZ: 83094495

Die T-Shirts für das Speedfunding gehen noch vor Weihnachten raus, aber nicht
vor dem 9. Dezember. Möglicherweise verschicken wir sie gleichzeitig mit den
Shirts vom großen Crowdfunding.

Bei Problemen kannst Du Dich gern melden bei Wolfgang (yes@c3s.cc).

Danke für Deine Mühe & Deinen Beitrag zur C3S!

Liebe Grüße

Das C3S-Team

""")

    else:
        _body = (u"""Dear supporter,

many thanks for your support!

You have chosen a t-shirt, C3S style - well, that means you've got a good sense
of fashion, n'est-çe pas? As soon as the payment is in, we will notify you.
Just so you know everything's alright.

Please transfer the amount of 35 EUR to our account at

EthikBank eG
Account holder: C3S SCE
Reference: shirt """ + _in.speed_id +
                 u"""
BIC: GENO DE F1 ETK
IBAN: DE79830944950003264378

(old style account id below)
(Konto: 3264378 )
(BLZ: 83094495 )


The tees for the speedfunding are going to be sent to you before Xmas but not
earlier than 9th December. Maybe we even sent them the same time we sent the
t-shirts from the crowdfunding before.

In case you encounter any problems, please don't hesitate to contact Wolfgang
(yes@c3s.cc)

Thanks a lot for your effort & your contribution to C3S!

Best wishes

The C3S Team
""")

    return _body

#
# receipts: implement later
#

# the receipt must carry the donation amount
donation_payment_receipt_en = u"""Dear supporter,

here it is!

Your donation of %s just hit our bank account. Right now, we're dancing
around the shrine we built for you...

In case of any problems please don't hesitate to contact Wolfgang (yes@c3s.cc)

Thanks a lot for your effort & your contribution to C3S!

Best wishes

The C3S Team
"""


# the receipt must carry the donation amount
donation_payment_receipt_de = u"""Liebe_r Supporter_in,

es ist soweit!

Deine Spende ist soeben auf unserem Konto eingegangen. Wir haben Dir zu Ehren
einen kleinen Altar errichtet und feiern Dich gerade. ;-)

Falls Probleme aufgetreten sind, melde Dich bitte bei Wolfgang (yes@c3s.cc)

Danke für Deine Mühe & Deinen Beitrag zur C3S!

Liebe Grüße

Das C3S-Team
"""

# should contain the speed_id
shirt_payment_receipt_en = u"""Dear supporter,

here it is!

The payment for your t-shirt (code %s) just hit our bank account. Right now,
we're dancing around the shrine we built for you...

In case of any problems please don't hesitate to contact wolfgang@c3s.cc

Thanks a lot for your effort & your contribution to C3S!

Best wishes

The C3S Team

P.S.: If you don't mind: Please shoot a photo of you wearing the shirt... now
that would look excellent on our site! (mail to Wolfgang: yes@c3s.cc)
"""

# should contain the speed_id
shirt_payment_receipt_de = u"""Liebe_r Supporter_in,

es ist soweit!

Die Bezahlung für Dein T-Shirt (code %s ) ist soeben auf unserem Konto
eingegangen. Wir haben Dir zu Ehren einen kleinen Altar errichtet und
feiern Dich gerade. ;-)

Falls Probleme aufgetreten sind, melde Dich bitte bei wolfgang@c3s.cc

Danke für Deine Mühe & Deinen Beitrag zur C3S!

Liebe Grüße

Das C3S-Team

P.S.: Mach doch mal ein Foto mit dem T-Shirt - sowas würde auf unserer Site
exzellent aussehen! (an Wolfgang: yes@c3s.cc)
"""


def make_mail_body(funding):
    """
    construct a multiline string to be used as the emails body
    """
    the_body = u"""
Yay!
we got some funding through the form:
speed id:                       %s
donation:                       %s
shirt:                          %s

first name:                     %s
last name:                      %s
email:                          %s
address1                        %s
address2                        %s
postcode:                       %s
city:                           %s
country:                        %s
locale:                         %s
comment:                         %s

that's it.. bye!""" % (
        funding.speed_id,
        funding.donation,
        funding.shirt_size,
        funding.firstname,
        funding.lastname,
        funding.email,
        funding.address1,
        funding.address2,
        funding.postcode,
        funding.city,
        funding.country,
        funding.locale,
        funding.comment,
    )
    return the_body


def accountant_mail(appject):
    """
    this function returns a message object for the mailer

    it consists of a mail body and an attachment attached to it
    """
    unencrypted = make_mail_body(appject)
    #print("accountant_mail: mail body: \n%s") % unencrypted
    #print("accountant_mail: type of mail body: %s") % type(unencrypted)
    encrypted = encrypt_with_gnupg(unencrypted)
    #print("accountant_mail: mail body (enc'd): \n%s") % encrypted
    #print("accountant_mail: type of mail body (enc'd): %s") % type(encrypted)

    message_recipient = 'yes@c3s.cc'

    message = Message(
        subject="[C3S FlashFunding] Yes! a new funding item",
        sender="noreply@c3s.cc",
        recipients=[message_recipient],
        body=encrypted
    )
    #print("accountant_mail: csv_payload: \n%s") % generate_csv(appstruct)
    #print(
    #    "accountant_mail: type of csv_payload: \n%s"
    #) % type(generate_csv(appstruct))
    #csv_payload_encd = encrypt_with_gnupg(generate_csv(appject))
    #print("accountant_mail: csv_payload_encd: \n%s") % csv_payload_encd
    #print(
    #    "accountant_mail: type of csv_payload_encd: \n%s"
    #) % type(csv_payload_encd)

    return message
