import os
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from wsgiref.util import FileWrapper
from .forms import UploadFileForm



# Create your views here.

def handle_uploaded_file(f):
    with open('composer/media/composer/userUpload/userUpload.mid', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def index(request):

	form = UploadFileForm()
	return render(request, 'composer/index.html', {'form': form})


	# if request.method == 'POST':
	# 	form = UploadFileForm(request.POST, request.FILES)
	# 	if form.is_valid():
	# 		handle_uploaded_file(request.FILES['file'])
	# 		# os.system("python composer/user_produce.py")
	# 		return HttpResponseRedirect('upload/')
	# else:
	# 	form = UploadFileForm()
	# return render(request, 'composer/index.html', {'form': form})


def user_upload(request):

	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			os.system("python composer/user_produce.py")
			formT=UploadFileForm()
			return render(request, 'composer/upload.html', {'form': formT})
	else:
		form = UploadFileForm()
	return render(request, 'composer/upload.html', {'form': form})


def produce(request):

	form = UploadFileForm()
	os.system("python composer/Produce.py")
	return render(request, 'composer/produce.html', {'form': form})

	# if request.method == 'POST':
	# 	form = UploadFileForm(request.POST, request.FILES)
	# 	if form.is_valid():
	# 		handle_uploaded_file(request.FILES['file'])
	# 		os.system("python composer/user_produce.py")
	# 		formT=UploadFileForm()
	# 		return render(request, 'composer/upload.html', {'form': formT})
	# 		return user_upload(request)
	# else:
		
	# 	form = UploadFileForm()
	# 	os.system("python composer/Produce.py")
	# return render(request, 'composer/produce.html', {'form': form})





def download(request):

	file_path="composer/static/composer/output/output.mid"

	with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="audio/mid")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response


def download_sheet(request):

	file_path="composer/static/composer/musicSheets/musicxml.xml"

	with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="audio/mid")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response

	
def team(request):

	return render(request,'composer/team.html')


def learn(request):

	return render(request,'composer/learn.html')



def comparison(request):

	return render(request,'composer/comparison.html')
	