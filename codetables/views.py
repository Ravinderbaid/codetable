from django.shortcuts import render
from django.core.files import File
from django.http import HttpResponseRedirect,HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
import os
import json
from django.http import Http404
import subprocess,shlex,time,psutil,datetime
from django.contrib.auth import authenticate, login, logout
from codetables.models import Files_saveds
from forms import MyRegistrationForm

# Create your views here.
@login_required(login_url = '/login/')
def index(request):
	files = Files_saveds.objects.filter(author__exact = request.user.id)
	return render(request, 'home.html', {'files' :files})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def login_user(request):
	state = "Please log in below..."
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				state = "You're successfully logged in!"
				return HttpResponseRedirect("/")
			else:
				state = "Your account is not active, please contact the site admin."
		else:
			state = "Your username and/or password were incorrect."
	
	return render(request, 'login.html',{'state':state, 'username': username})

def signup(request):
	args = {}
	if request.method == 'POST':
		form = MyRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/")
		else:
			args['form'] = form
	else:
		args['form'] = MyRegistrationForm()	

	
	args.update(csrf(request))
	return render(request, 'signup.html', args)

def compile_output_code():
	args = shlex.split('gcc sample.c -o test1')
	proc = subprocess.Popen(args, stderr=subprocess.PIPE)
	return proc.stderr.read()
	# compile_status=''
	# while True:
	#   line = proc.stderr.readline()
	#   if line != '':
	#     compile_status = compile_status +line
	#     line.rstrip()
	#   else:
	#     return compile_status
def output_error_code(value):
	flag = 1
	now = datetime.datetime.now()
	proc = subprocess.Popen('./test1', stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE) 
	p = psutil.Process(proc.pid)
	pidcreated = datetime.datetime.fromtimestamp(p.create_time)
	allowed_time = pidcreated + datetime.timedelta( 0, 5 )
	while proc.poll() is None:
		now = datetime.datetime.now()
		if value:
			stdout,stderr = proc.communicate(value)
			flag = 0
			if stdout or stderr:
				time_taken = (now.second + now.microsecond/1000000.0) - (pidcreated.second +pidcreated.microsecond/1000000.0)
				return stdout,stderr,str(time_taken)[:-2]
		if allowed_time > datetime.datetime.now():
			flag=1
		else :
			flag=0
			break
		time.sleep(1)
		
	if flag:
		tmp = proc.stdout.read()
		message = ''
	else:
		tmp = ''
		message = 'Compilation took more than 5 seconds'
		proc.kill()
	time_taken = (now.second + now.microsecond/1000000.0) - (pidcreated.second +pidcreated.microsecond/1000000.0)
	return tmp,message,str(time_taken)[:-2]

def compile_code(request):
	if request.method == 'POST':
		code_text = request.POST.get('code_text')
		checkbox_value = request.POST.get('check_uncheck')
		if checkbox_value:
			user_input_value = request.POST.get('user_input_value')
		else:
			user_input_value =''
		with open('sample.c', 'w') as files:
			code_file = File(files)
			code_file.write(code_text)
		files.closed
		compile_status = compile_output_code()	
		if not compile_status:
			output,error,time_taken = output_error_code(user_input_value)
		else:
			output,error,time_taken = '','',''
		data={'output_code' : output, 'error_code' : error, 'time_taken' : time_taken, 'compile_status' : compile_status}
		return HttpResponse(json.dumps(data))

@login_required(login_url = '/login/')
def save_file(request):
	if request.method == 'POST':
		title = request.POST.get('title')
		code_text = request.POST.get('code_text')
		filename = 'user_codes/'+title+'_'+request.user.username+'.c'
		verify_duplicate=[]
		if title != '' and code_text != '':
			try:
				verify_duplicate = Files_saveds.objects.get(author__exact=request.user.id,title__exact = title)
			except Exception, e:
				pass
			if verify_duplicate:
				with open(filename, 'r') as files:
					code_file = File(files)
					file_code=code_file.read()
					files.closed
					state = {'1':'3', '2' : file_code }
			else:
				try:
					with open(filename, 'w') as files:
						code_file = File(files)
						code_file.write(code_text)
					files.closed
					p = Files_saveds(title=title, author=request.user)
					p.save()
					state = {'1' : '0', '2' :'Successful'}
				except Exception, e:
					state = {'1' : '1','2' : 'Couldnot save'}
				
		else:
			state = {'1' : '2','2' : 'No title or code_text'}

		return HttpResponse(json.dumps(state))

def get_file(request,file_id):
	fi=[]
	try:
		fi = Files_saveds.objects.get(pk=file_id)
	except Exception,e:
		raise Http404
	if request.user == fi.author:
		filename = 'user_codes/'+fi.title+'_'+request.user.username+'.c'
		with open(filename, 'r') as files:
			code_file = File(files)
			file_code=code_file.read()
			files.closed
		return render(request,'home.html',{'file_code':file_code})
	else:
		raise Http404