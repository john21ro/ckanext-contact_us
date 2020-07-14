import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.plugins as p
import ckan.lib.captcha as captcha
import ckan.plugins.toolkit as tk
from ckan.lib.base import BaseController, config
import jinja2
from ckan.common import _, c, g, request
import ckan.lib.mailer
from validate_email import validate_email

abort = base.abort
render = base.render

class ContactUsController(BaseController):
    def index(self, context=None):
        c = p.toolkit.c
        public_key = g.recaptcha_publickey
        data = request.params or {}
        errors = {}
        error_summary = {}
        # print data
        # print config.get('email_to');
        
        if not data == {} :
            try:
                captcha.check_recaptcha(data.get('g-recaptcha-response'))
                # print data.get('g-recaptcha-response')
            except captcha.CaptchaError:
                # error_msg = _(u'Bad Captcha. Please try again.')
                errors['g-recaptcha-response'] = [_('Bad Captcha. Please try again.')]
            if data.get('contact_us.nochange') != 'http://' :
                errors['contact_us.nochange'] = [_('The value was edited')]
            if not data.get('g-recaptcha-response') :
                errors['g-recaptcha-response'] = [_('Missing captcha value')]
                # print errors['g-recaptcha-response']
            if not data.get('contact_us.name') :
                errors['contact_us.name'] = [_('Missing value')]
            if not data.get('contact_us.email') :
                errors['contact_us.email'] = [_('Missing value')]
            if not data.get('contact_us.category') :
                errors['contact_us.category'] = [_('Missing value')]
            elif not validate_email(data.get('contact_us.email')):
                errors['contact_us.email'] = [_('Invalid email')]
            if not data.get('contact_us.message') :
                errors['contact_us.message'] = [_('Missing value')]
            
            if errors == {} :
                try:
                    message_text = "Topic: " + data.get('contact_us.category') + "\nEmail: " + data.get(
                        'contact_us.email') + "\n\n" + data.get('contact_us.message')
                    # emails = config.get('contact_us.email') 
                    emails = "john21ro@yahoo.com,datagovro@gmail.com,online@gov.ro"
                    for v in emails.split(',') :
                        ckan.lib.mailer._mail_recipient('Admin',v,data.get('contact_us.name'),data.get('contact_us.email'),'Contact form',message_text)
                    h.flash_success(_('Email sent'))
                    data = {}
                except ckan.lib.mailer.MailerException:
                    raise
        #error_summary = errors
        vars = {'data': data, 'errors': errors, 'error_summary': error_summary, 'public_key' : g.recaptcha_publickey}
        return render('ckanext/contact_us/index.html', extra_vars=vars)

