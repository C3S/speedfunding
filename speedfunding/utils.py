# -*- coding: utf-8 -*-
from pyramid_mailer.message import (
    Message,
    #Attachment,
)

# the confirmation must contain the amount and reference code
donation_submission_confirmation_en = u"""Dear supporter,

we just received your pledge to donate %s EUR. Please transfer the money to our
bank account at

EthikBank eG
Account holder: C3S SCE
Reference: donation %s
BIC: GENO DE F1 ETK
IBAN: DE79830944950003264378

(old style account id below)
(Konto: 3264378 )
(BLZ: 83094495 )

Many heartfelt thanks for your support!

We highly appreciate your donation. As soon as it hits our bank account we will
notify you. Just so you know everything's going fine.

In case of any problems please don't hesitate to contact wolfgang@c3s.cc

Thanks a lot for your effort & your contribution to C3S!

Best wishes

The C3S Team
"""

# the receipt must carry the donation amount
donation_payment_receipt_en = u"""Dear supporter,

here it is!

Your donation of %s just hit our bank account. Right now, we're dancing
around the shrine we built for you...

In case of any problems please don't hesitate to contact wolfgang@c3s.cc

Thanks a lot for your effort & your contribution to C3S!

Best wishes

The C3S Team
"""

donation_submission_confirmation_de = u"""Liebe_r Supporter_in,

vielen lieben Dank für Deine Unterstützung!

Wir freuen uns über Deine Spende über % EUR. Bitte überweise das Geld auf unser
Konto bei der

EthikBank eG
Kontoinhaber: C3S SCE
Verwendungszweck: Spende %s

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

"""

donation_payment_receipt_de = u"""Liebe_r Supporter_in,

es ist soweit!

Deine Spende ist soeben auf unserem Konto eingegangen. Wir haben Dir zu Ehren
einen kleinen Altar errichtet und feiern Dich gerade. ;-)

Falls Probleme aufgetreten sind, melde Dich bitte bei Wolfgang (yes@c3s.cc)

Danke für Deine Mühe & Deinen Beitrag zur C3S!

Liebe Grüße

Das C3S-Team
"""


def make_confirmation_email(_input):
    """
    send a mail to confirm the submission
    """
    # DEBUG _input
    #import pprint
    #pprint.pprint(_input)

    d_key = {
        u'1': u'5',
        u'2': u'10',
        u'3': u'25',
        u'4': '50',
        u'5': '100',
        u'6': '250',
        u'7': '500',
        u'8': '1000',
        u'9': '2500',
        u'10': '5000',
    }

    _lang = _input['locale']
    #print(_lang)
    #print(type(_lang))  # unicode

    if _lang is 'DE':
        _body = (
            donation_submission_confirmation_de % (
                d_key.get(_input['donation']), _input['speed_id']))
    else:
        _body = (
            donation_submission_confirmation_en % (
                d_key.get(_input['donation']), _input['speed_id']))
    #print("the body: %s" % _body)
    message = Message(
        subject="[C3S Speedfunding] confirming your submission",
        sender="noreply@c3s.cc",
        recipients=[_input['email']],
        body=(_body)
    )
    return message
