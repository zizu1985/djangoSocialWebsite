from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import connection
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, SQLCommandForm
from .token import account_activation_token
from .models import Profile, SQLCommand
import datetime
import os
from .utils import store_as_csv
from django.conf import settings
from .models import Contact
from .decorators import ajax_required

# Form for authenticate user
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # CHECK - Do ktorej bazy sie laczy aby sprawdzić? Gdzie to jest trzymane?
            # SOL. django.contrib.auth dostarcza modele do tego. Baza main.auth_user
            # authenticate - check user correctness and return not null if all is ok
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    # login - set user in current session
                    login(request, user)
                    return HttpResponse("Authenticated " \
                                        "successfully")
            else:
                return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request,'account/dashboard.html',{'section': 'dashboard'})


# Method is not marked as login required, but after form submitt switch to login page.
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet - we will modify one field
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # New user is not active by default
            new_user.is_active = False
            # Save the user object
            new_user.save()
            # Create new profile
            profile = Profile.objects.create(user=new_user)

            # Send activcation email
            current_site = get_current_site(request)
            mail_subject = 'Please approve new account creation.'
            message = render_to_string('acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            #to_email = form.cleaned_data.get('t')
            # TODO -- all admins
            to_email = 'tziss85@gmail.com'
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request,"User registration awaits approvals by administrator")
            return HttpResponse('You account creation is waiting for approval by admin.')
            #return render(request,'account/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})


# activate user when administrator accept user registration
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def create_sqlcommand(request):
    if request.method == 'POST':
        # Have to direct specify which user created SQL command
        sqlcommandform = SQLCommandForm(data=request.POST)
        if sqlcommandform.is_valid():

            # Create a new sql comamnd - without commit
            sqlCommand = sqlcommandform.save(commit=False)

            # Sql command is not approved by default
            sqlCommand.set_approved(False)
            sqlCommand.set_creation_date(datetime.datetime.now())
            sqlCommand.set_user(request.user)
            sqlCommand.save()

            # Send email for approval to execute query
            current_site = get_current_site(request)
            mail_subject = 'Please approved sql command request from user {}'.format(request.user.username)
            message = render_to_string('sql_command_approve_email.html', {
                'user': request.user.username,
                'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
                'domain': current_site.domain,
                'sqlid': urlsafe_base64_encode(force_bytes(sqlCommand.id)),
                'token': account_activation_token.make_token(request.user),
                'sql_command': sqlCommand.command,
            })

            # TODO -- all admins
            to_email = 'tziss85@gmail.com'
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
    else:
        # Have to direct specify which user created SQL command
        # LEARN - if form is not properly initialized error appears "expected number, get NonType
        #           Here request.user is required as user has to be created for sql form
        sqlcommandform = SQLCommandForm()

    return render(request, 'account/create_sqlcommand.html', {'sqlcommand_form': sqlcommandform})


# Run sql command and send output to user
def sql_execute(request, sqlid, token, uid):
    user = request.user
    try:
        sqlid = force_text(urlsafe_base64_decode(sqlid))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        sqlid = None
    if user is not None and account_activation_token.check_token(user, token):
        # TODO - dlaczego sqlid jest zly? Likwidacja sztywniaka
        # Trimming because __str__ for Query strings add [' ']
        sqlcmd = str(SQLCommand.objects.filter(id=21).values_list('command', flat=True))[2:][:-2]

        # Run query.
        # TODO - how to avoid sql injection ?
        cursor = connection.cursor()
        cursor.execute(sqlcmd)
        data = cursor.fetchall()

        # generate filename for storing
        filename = "sqloutput_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename += '.csv'

        # store output in server as csv file. Location is not accessible to public.
        store_as_csv(data,filename,settings.CSV_ROOT)
        #return HttpResponse(filename)

        full_filepath = settings.CSV_ROOT + os.path.sep + filename
        # Check if file has been created and send if
        if os.path.exists(full_filepath):
            mail_subject = 'Output from sql'
            message = render_to_string('sql_executed.html', {
                'user': request.user.username
            })
            to_email = str(User.objects.filter(pk=force_text(urlsafe_base64_decode(uid))).values_list('email', flat=True))[2:][:-2]
            #return HttpResponse(to_email)
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.encoding = "utf-8"
            file = open(full_filepath, "r")
            email.attach(full_filepath, content = file.read(), mimetype="text/csv")
            file.close()
            email.send()
        else:
            return HttpResponse('Something wrong with generating csv filename with response!')

        return HttpResponse('SQL command succesfully generated and send to requestor.')
    else:
        return HttpResponse('Activation link for sql command is not valid!')


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,'account/user/list.html',
            {'section': 'people',
             'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User,username=username,is_active=True)
    return render(request,'account/user/detail.html',
                  {'section': 'people',
                   'user': user})

# Build an AJAX view to follow users
# Build following rule between Users using Contact class
@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})

