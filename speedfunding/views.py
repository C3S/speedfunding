# _*_ coding: utf-8 _*_

#from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from pyramid.i18n import (
    #    get_localizer,
    get_locale_name
)

#from sqlalchemy.exc import DBAPIError

#from .models import (
#    DBSession,
#    MyModel,
#)

import deform
import colander

from translationstring import TranslationStringFactory
_ = TranslationStringFactory('speedfunding')

# XXX TODO: i18n
country_codes = [
    ('AT', _(u'Austria')),
    ('BE', _(u'Belgium')),
    ('BG', _(u'Bulgaria')),
    ('CH', _(u'Switzerland')),
    ('CZ', _(u'Czech Republic')),
    ('DE', _(u'Germany')),
    ('DK', _(u'Denmark')),
    ('ES', _(u'Spain')),
    ('EE', _(u'Estonia')),
    ('FI', _(u'Finland')),
    ('FR', _(u'France')),
    ('GB', _(u'United Kingdom')),
    ('GR', _(u'Greece')),
    ('HU', _(u'Hungary')),
    ('HR', _(u'Croatia')),
    ('IL', _(u'Israel')),
    ('IE', _(u'Ireland')),
    ('IT', _(u'Italy')),
    ('LT', _(u'Lithuania')),
    ('LV', _(u'Latvia')),
    ('LU', _(u'Luxembourg')),
    ('MT', _(u'Malta')),
    ('NL', _(u'Netherlands')),
    ('PL', _(u'Poland')),
    ('PT', _(u'Portugal')),
    ('SK', _(u'Slovakia')),
    ('SI', _(u'Slovenia')),
    ('SE', _(u'Sweden')),
    ('XX', _(u'other'))
]


@view_config(route_name='speedfund', renderer='templates/speedfunding.pt')
def speedfunding_view(request):
    """
    this view is the default view or landing page: the main speedfunding form

    simple: one option, three buttons

    option: paypal or not

    buttons: [Donate]  [T-Shirt]  [Share(s)]
    """
    DEBUG = True
    # if another language was chosen by clicking on a flag
    # the add_locale_to_cookie subscriber has planted an attr on the request

    if hasattr(request, '_REDIRECT_'):
        _query = request._REDIRECT_
        request.response.set_cookie('_LOCALE_', _query)
        request._LOCALE_ = locale_name = _query
        return HTTPFound(location=request.route_url('speedfund'),
                         headers=request.response.headers)
    else:
        locale_name = get_locale_name(request)

    # set default of Country select widget according to locale
    LOCALE_COUNTRY_MAPPING = {
        'de': 'DE',
        #'da': 'DK',
        'en': 'GB',
        #'es': 'ES',
        #'fr': 'FR',
    }
    country_default = LOCALE_COUNTRY_MAPPING.get(locale_name)
    if DEBUG:  # pragma: no cover
        print("== locale is :" + str(locale_name))
        print("== choosing :" + str(country_default))

    # declare a form
    class PaymentChoiceForm(colander.MappingSchema):
        """
        do you want to pay with paypal or not?
        """
        payment_option = colander.SchemaNode(
            colander.String(),
            title=_('I want to pay for the donation/shirt via paypal '
                    '... or rather not.'),
            widget=deform.widget.RadioChoiceWidget(
                values=(
                    ('paypal', _(u'Yes, PayPal is OK for me.')),
                    ('transfer', _(u'No. I will transfer the money myself.')),
                ),
                default='paypal',
            )
        )

    schema = PaymentChoiceForm()

    form = deform.Form(
        schema,
        buttons=[  # stick three buttons on the form
            deform.Button('donate', _(u'Donate')),
            deform.Button('shirt', _(u'T-Shirt')),
            deform.Button('shares', _(u'Shares')),
        ])

    # if the form has been used and SUBMITTED, check contents
    # the form was submitted, if there is either 'donate',
    # 'shirt' or 'share' in request.POST
    submitted = (
        ('donate' in request.POST)
        or ('shirt' in request.POST)
        or ('shares' in request.POST)
    )
    if submitted is True:
        print("submitted!")

    if submitted:  # someone klicked a button, but which one?

        if 'shares' in request.POST:
            print("shares was chosen.")
            return HTTPFound(
                location=request.route_url('yes'),  # https://yes.c3s.cc
            )

        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except deform.ValidationFailure, e:
            print(e)
            request.session.flash(
                _(u"Please note: There were errors, "
                  "please check the form below."),
                'message_above_form',
                allow_duplicate=False)
            # if there were errors, present the form with error messages
            return{'form': e.render()}

        request.session.pop_flash('message_above_form')
        # if the form validated correctly, use the data given
        print("the appstruct: %s" % appstruct)

        if 'shirt' in request.POST:
            if appstruct['payment_option'] == 'paypal':
                print("it is paypal, do something")
                request._paypal = True
            if appstruct['payment_option'] == 'transfer':
                print("it is transfer, do something")
                request._paypal = False

            return HTTPFound(
                location=request.route_url('shirt'),
                headers=request.response.headers,
            )

        if ('donate' in request.POST):
            if appstruct['payment_option'] == 'paypal':
                print("it is paypal, do something")
                #request._paypal = True
                request.response.set_cookie('_paypal_', 'yes')
                request.session['appstruct'] = appstruct
                request.session.flash('DEBUG: with paypal',
                                      'message_above_form')
                return HTTPFound(
                    location=request.route_url('donate')
                    # redirect to paypal donation options
                )

            if appstruct['payment_option'] == 'transfer':
                print("it is transfer, do something")
                #request._paypal = False
                request.response.set_cookie('_paypal_', 'no')
                request.session['appstruct'] = appstruct
                request.session.flash('DEBUG: no paypal',
                                      'message_above_form')
            return HTTPFound(
                location=request.route_url('donate'),
                headers=request.response.headers,
            )

    # if not submitted: show form
    html = form.render()

    return {'form': html,
            'project': 'speedfunding'}


@view_config(route_name='donate', renderer='templates/donate.pt')
def donate_view(request):
    """
    this view handles donations
    """
    DEBUG = True
    if hasattr(request, '_REDIRECT_'):
        _query = request._REDIRECT_
        request.response.set_cookie('_LOCALE_', _query)
        request._LOCALE_ = locale_name = _query
        return HTTPFound(location=request.route_url('speedfund'),
                         headers=request.response.headers)
    else:
        locale_name = get_locale_name(request)
    if hasattr(request, '_paypal'):
        print("hasattr(request, '_paypal') !!!")
    # set default of Country select widget according to locale
    LOCALE_COUNTRY_MAPPING = {
        'de': 'DE',
        #'da': 'DK',
        'en': 'GB',
        #'es': 'ES',
        #'fr': 'FR',
    }
    country_default = LOCALE_COUNTRY_MAPPING.get(locale_name)
    if DEBUG:  # pragma: no cover
        print("== locale is :" + str(locale_name))
        print("== choosing :" + str(country_default))

    donation_amount_choice = (
        ('9', u'10000€'),
        ('8', u'5000€'),
        ('7', u'2000€'),
        ('6', u'1000€'),
        ('5', u'500€'),
        ('4', u'100€'),
        ('3', u'20€'),
        ('2', u'10€'),
        ('1', u'5€'),
    )

    # declare a data set
    class DonationOption(colander.MappingSchema):
        """
        a class for the donation choices in our speedfunding
        """
        the_amount = colander.SchemaNode(
            colander.String(),
            title=_(u'I want to say thanks with money. I donate:'),
            default='1',  # default: '1' ==> '5€'
            #widget=deform.widget.SelectWidget(
            widget=deform.widget.SelectSliderWidget(
                values=donation_amount_choice),
            #    values=(('a', 'foo'), ('b', 'bar'))
            #),
            oid="donation_choice",
        )

    class PersonalData(colander.MappingSchema):
        address1 = colander.SchemaNode(
            colander.String(),
            title=_(u'Address Line 1')
        )
        address2 = colander.SchemaNode(
            colander.String(),
            missing=unicode(''),
            title=_(u"Address Line 2")
        )
        postcode = colander.SchemaNode(
            colander.String(),
            title=_(u'Post Code'),
            oid="postcode"
        )
        city = colander.SchemaNode(
            colander.String(),
            title=_(u'City'),
            oid="city",
        )
        country = colander.SchemaNode(
            colander.String(),
            title=_(u'Country'),
            default=country_default,
            widget=deform.widget.SelectWidget(
                values=country_codes),
            oid="country",
        )

    class DonationForm(colander.Schema):
        """
        a donation
        """
        donation = DonationOption(
            title=_('The Donation')
        )
        #if True:
        personalData = PersonalData(
            title=_('Personal Data')
        )

    # now construct the form schema from the parts above
    schema = DonationForm()

    form = deform.Form(
        schema,
        buttons=[
            deform.Button('donate', _(u'Yes, I want to donate!')),
            deform.Button('go_back', _(u'Go back, let me start over again.')),
        ])

    # if the form has been used and SUBMITTED, check contents
    submitted = (('donate' in request.POST) or ('go_back' in request.POST))

    if submitted:
        if ('go_back' in request.POST):
            return HTTPFound(
                location=request.route_url('speedfund'),
            )
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except deform.ValidationFailure, e:
            print(e)
            request.session.flash(
                _(u"Please note: There were errors, "
                  "please check the form below."),
                'message_above_form',
                allow_duplicate=False)
            # if there were errors, present the form with error messages
            return{'form': e.render()}

        # if the form validated correctly, use the data given
        print("the appstruct: %s" % appstruct)
        return HTTPFound(
            location=request.route_url('success'),
        )

    # if not submitted: show form
    html = form.render()

    return {'form': html,
            'project': 'speedfunding'}


@view_config(route_name='shirt', renderer='templates/shirt.pt')
def shirt_view(request):
    """
    this view is the default view: the speedfunding form
    """
    # TODO: check for paypal status
    #if '_paypal_' in request.session.cookies:
    #    print(
    #        "paypal in cookies! value: %s" % request.session.cookies['_paypal_'])

    if 'appstruct' in request.session:
        print(
            "appstruct in session! value: %s" % request.session['appstruct'])
    import pprint
    pprint.pprint(request.session)
#    import pdb
#    pdb.set_trace()

    # declare a form
    class TShirtForm(colander.MappingSchema):
        """
        do you want to pay with paypal or not?
        """
        the_shirt = colander.SchemaNode(
            colander.String(),
            title=_(u"Yes, I'll have a T-Shirt please! Send Me"),
            #widget=deform.widget.RadioChoiceWidget(
            #            widget=deform.widget.SelectSliderWidget(
            widget=deform.widget.Select2Widget(
                values=(
                    (u'S',
                     _(u'Size S')),
                    (u'M',
                     _(u'Size M')),
                    (u'L',
                     _(u'Size L')),
                    (u'XL',
                     _(u'Size XL')),
                    (u'XXL',
                     _(u'Size XXL')),
                )
            )
        )

    schema = TShirtForm()
    form = deform.Form(
        schema,
        buttons=[
            deform.Button('order_shirt', _(u'Yes, I want this T-Shirt!')),
            deform.Button('go_back', _(u'Go back, let me start over again.')),
        ])

    # if the form has been used and SUBMITTED, check contents
    submitted = (('order_shirt' in request.POST)
                 or ('go_back' in request.POST))

    if submitted:
        if ('go_back' in request.POST):
            return HTTPFound(
                location=request.route_url('speedfund'),
            )

        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
        except deform.ValidationFailure, e:
            print(e)
            request.session.flash(
                _(u"Please note: There were errors, "
                  "please check the form below."),
                'message_above_form',
                allow_duplicate=False)
            # if there were errors, present the form with error messages
            return{'form': e.render()}

        # if the form validated correctly, use the data given
        print("the appstruct: %s" % appstruct)
        return HTTPFound(
            location=request.route_url('success'),
        )

    # if not submitted: show form
    html = form.render()

    return {'form': html,
            'project': 'speedfunding'}


@view_config(route_name='yes', renderer='templates/shares.pt')
def shares_view(request):
    """
    this view shows a short message and then redirects to the AFM form
    """
    return {'foo': 'bar',
            'project': 'speedfunding'}


@view_config(route_name='success', renderer='templates/success.pt')
def success_view(request):
    """
    this view shows a success message
    """
    #DEBUG = True
    #locale_name = get_locale_name(request)

    return {'foo': 'bar',
            'project': 'speedfunding'}
