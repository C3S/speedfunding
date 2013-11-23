# -*- coding: utf-8 -*-

from speedfunding.models import (
    Speedfundings,
    TheTotal,
    DBSession,
)

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
    DEBUG = False
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

    # # declare a form
    # class PaymentChoiceForm(colander.MappingSchema):
    #     """
    #     do you want to pay with paypal or not?
    #     """
    #     payment_option = colander.SchemaNode(
    #         colander.String(),
    #         title=_('I want to pay for the donation/shirt via paypal '
    #                 '... or rather not.'),
    #         widget=deform.widget.RadioChoiceWidget(
    #             values=(
    #                 ('paypal', _(u'Yes, PayPal is OK for me.')),
    #                 ('transfer', _(u'No. I will transfer the money myself.')),
    #             ),
    #             default='paypal',
    #         )
    #     )

    # schema = PaymentChoiceForm()

    # form = deform.Form(
    #     schema,
    #     buttons=[  # stick three buttons on the form
    #         deform.Button('donate', _(u'Donate')),
    #         deform.Button('shirt', _(u'T-Shirt')),
    #         deform.Button('shares', _(u'Shares')),
    #     ])

    # # if the form has been used and SUBMITTED, check contents
    # # the form was submitted, if there is either 'donate',
    # # 'shirt' or 'share' in request.POST
    # submitted = (
    #     ('donate' in request.POST)
    #     or ('shirt' in request.POST)
    #     or ('shares' in request.POST)
    # )
    # if submitted is True:
    #     print("submitted!")

    # if submitted:  # someone klicked a button, but which one?

    #     if 'shares' in request.POST:
    #         print("shares was chosen.")
    #         return HTTPFound(
    #             location=request.route_url('yes'),  # https://yes.c3s.cc
    #         )

    #     controls = request.POST.items()
    #     try:
    #         appstruct = form.validate(controls)
    #     except deform.ValidationFailure, e:
    #         print(e)
    #         request.session.flash(
    #             _(u"Please note: There were errors, "
    #               "please check the form below."),
    #             'message_above_form',
    #             allow_duplicate=False)
    #         # if there were errors, present the form with error messages
    #         return{'form': e.render()}

    #     request.session.pop_flash('message_above_form')
    #     # if the form validated correctly, use the data given
    #     print("the appstruct: %s" % appstruct)

    #     if 'shirt' in request.POST:
    #         if appstruct['payment_option'] == 'paypal':
    #             print("it is paypal, do something")
    #             request._paypal = True
    #         if appstruct['payment_option'] == 'transfer':
    #             print("it is transfer, do something")
    #             request._paypal = False

    #         return HTTPFound(
    #             location=request.route_url('shirt'),
    #             headers=request.response.headers,
    #         )

    #     if ('donate' in request.POST):
    #         if appstruct['payment_option'] == 'paypal':
    #             print("it is paypal, do something")
    #             #request._paypal = True
    #             request.response.set_cookie('_paypal_', 'yes')
    #             request.session['appstruct'] = appstruct
    #             request.session.flash('DEBUG: with paypal',
    #                                   'message_above_form')
    #             return HTTPFound(
    #                 location=request.route_url('donate')
    #                 # redirect to paypal donation options
    #             )

    #         if appstruct['payment_option'] == 'transfer':
    #             print("it is transfer, do something")
    #             #request._paypal = False
    #             request.response.set_cookie('_paypal_', 'no')
    #             request.session['appstruct'] = appstruct
    #             request.session.flash('DEBUG: no paypal',
    #                                   'message_above_form')
    #         return HTTPFound(
    #             location=request.route_url('donate'),
    #             headers=request.response.headers,
    #         )

    # # if not submitted: show form
    # html = form.render()
    html = ''

    _the_total = TheTotal.get_total()
    try:
        _missing_sum = 70000 - int(_the_total.amount_actual)
    except TypeError, t:
        print("the error: %s" % t)
        #import pdb; pdb.set_trace()
        _missing_sum = "70000"
    except AttributeError, a:
        print("the error: %s" % a)
        _missing_sum = "70000"

    return {'form': html,
            'the_total': '12.345,67',
            'missing_sum': _missing_sum,
            'project': 'speedfunding'}


@view_config(route_name='donate', renderer='templates/donate.pt')
def donate_view(request):
    """
    this view handles donations
    """
    DEBUG = False
    if hasattr(request, '_REDIRECT_'):
        _query = request._REDIRECT_
        request.response.set_cookie('_LOCALE_', _query)
        request._LOCALE_ = locale_name = _query
        return HTTPFound(location=request.route_url('speedfund'),
                         headers=request.response.headers)
    else:
        locale_name = get_locale_name(request)
    #if hasattr(request, '_paypal'):
    #    print("hasattr(request, '_paypal') !!!")
    #import pdb;pdb.set_trace()
    # set default of Country select widget according to locale
    LOCALE_COUNTRY_MAPPING = {
        'de': 'DE',
        #'da': 'DK',
        'en': 'GB',
        #'es': 'ES',
        #'fr': 'FR',
    }

    if 'paypal' in request.params:
        return {
            'form': '',  # if paypal was chosen, don't show the form
            'paypal': True}  # but the paypal button (see templates/donate.pt)
    else:
        paypal = False

    #print("DEBUG: paypal in donate_view is %s" % paypal)

    country_default = LOCALE_COUNTRY_MAPPING.get(locale_name)
    if DEBUG:  # pragma: no cover
        print("== locale is :" + str(locale_name))
        print("== choosing :" + str(country_default))

    donation_amount_choice = (
        ('10', u'5000,00 €'),
        ('9', u'2500,00 €'),
        ('8', u'1000,00 €'),
        ('7', u'500,00 €'),
        ('6', u'250,00 €'),
        ('5', u'100,00 €'),
        ('4', u'50,00 €'),
        ('3', u'25,00 €'),
        ('2', u'10,00 €'),
        ('1', u'5,00 €'),
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
            #widget=deform.widget.SelectSliderWidget(
            widget=deform.widget.SelectWidget(
                values=donation_amount_choice),
            oid="donation_choice",
        )

    class PersonalData(colander.MappingSchema):
        email = colander.SchemaNode(
            colander.String(),
            title=_(u'Email'),
            validator=colander.Email(),
            oid="email",
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
            title=_('We need some personal data to be able to contact you.')
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
            #print("the form did validate!")
            #print("the appstruct: %s" % appstruct)
            # if the form validated correctly, use the data given
            _donation = Speedfundings(
                firstname='',
                lastname='',
                email=appstruct['personalData']['email'],
                address1='',
                address2='',
                postcode='',
                city='',
                country='',
                locale=locale_name,
                donation=appstruct['donation']['the_amount'],
                shirt_size='',
                comment='',
            )
            try:
                DBSession.add(_donation)
                DBSession.flush()
            except:
                print("failed to persist")

        except deform.ValidationFailure, e:
            print(e)
            request.session.flash(
                _(u"Please note: There were errors, "
                  "please check the form below."),
                'message_above_form',
                allow_duplicate=False)
            # if there were errors, present the form with error messages
            return{
                'form': e.render(),
                'paypal': paypal,
            }

        #print("the appstruct: %s" % appstruct)
        request.session.pop_flash()  # delete old error messages
        return HTTPFound(
            location=request.route_url('success'),
        )

    # if not submitted: show form
    html = form.render()

    return {'form': html,
            'paypal': paypal,
            'project': 'speedfunding'}


@view_config(route_name='shirt', renderer='templates/shirt.pt')
def shirt_view(request):
    """
    this view is the default view: the speedfunding form
    """
    DEBUG = True

    if 'paypal' in request.params:
        #print("paypal option")
        return {
            'form': '',  # if paypal was chosen, don't show the form
            'paypal': True}  # but the paypal button (see templates/shirt.pt)
    else:
        paypal = False

    #print("DEBUG: paypal in shirt_view is %s" % paypal)

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
    class TShirt(colander.MappingSchema):
        """
        what size and fit for the shirt?
        """
        shirt_option = colander.SchemaNode(
            colander.String(),
            title=_(u"Yes, I'll have a T-Shirt please! Send Me"),
            #widget=deform.widget.RadioChoiceWidget(
            #            widget=deform.widget.SelectSliderWidget(
            widget=deform.widget.Select2Widget(
                values=(
                    (u'S', _(u'S €35,00 EUR')),
                    (u'M', _(u'M €35,00 EUR')),
                    (u'L', _(u'L €35,00 EUR')),
                    (u'XL', _(u'XL €35,00 EUR')),
                    (u'XXL', _(u'XXL €35,00 EUR')),
                    (u'S (Ladyfit)', _(u'S (Ladyfit) €35,00 EUR')),
                    (u'M (Ladyfit)', _(u'M (Ladyfit) €35,00 EUR')),
                    (u'L (Ladyfit)', _(u'L (Ladyfit) €35,00 EUR')),
                    (u'XL (Ladyfit)', _(u'XL (Ladyfit) €35,00 EUR')),
                    (u'XXL (Ladyfit)', _(u'XXL (Ladyfit) €35,00 EUR')),
                )
            )
        )

    class PersonalData(colander.MappingSchema):
        """
        people who want a shirt need to give us some address information
        """
        firstname = colander.SchemaNode(
            colander.String(),
            widget=deform.widget.TextInputWidget(
                css_class='deformWidgetWithStyle'),
            title=_(u'First Name')
        )
        lastname = colander.SchemaNode(
            colander.String(),
            title=_(u"Last Name")
        )
        email = colander.SchemaNode(
            colander.String(),
            validator=colander.Email(),
            title=_(u"Email (just in case we need to check back with you)")
        )
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

    class TShirtForm(colander.Schema):
        """
        the shirt form comprises shirt option and personal data
        """
        shirt_data = TShirt(
            title=_(u'choose shirt size')
        )
        personalData = PersonalData(
            title=_('Personal Data')
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
            #print("the form validated!")
            # XXX TODO: persist
            _shirt = Speedfundings(
                firstname=appstruct['personalData']['firstname'],
                lastname=appstruct['personalData']['lastname'],
                email=appstruct['personalData']['email'],
                address1=appstruct['personalData']['address1'],
                address2=appstruct['personalData']['address2'],
                postcode=appstruct['personalData']['postcode'],
                city=appstruct['personalData']['city'],
                country=appstruct['personalData']['country'],
                locale=locale_name,
                donation='',
                shirt_size=appstruct['shirt_data']['shirt_option'],
                comment='',
            )
            try:
                DBSession.add(_shirt)
                DBSession.flush()
            except:
                print("failed to persist")

        except deform.ValidationFailure, e:
            print(e)
            request.session.flash(
                _(u"Please note: There were errors, "
                  "please check the form below."),
                'message_above_form',
                allow_duplicate=False)
            # if there were errors, present the form with error messages
            #print("DEBUG: paypal in shirt_view is %s" % paypal)
            return{'form': e.render(),
                   'paypal': paypal}

        # if the form validated correctly, use the data given
        #print("the appstruct: %s" % appstruct)
        request.session.pop_flash()  # delete old error messages
        return HTTPFound(
            location=request.route_url('success'),  # XXX transport info there
        )

    # if not submitted: show form
    html = form.render()
    #print("DEBUG: paypal in shirt_view is %s" % paypal)
    return {'form': html,
            'paypal': paypal,
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
