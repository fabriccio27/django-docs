from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

""" A view handling this form will receive the file data in request.FILES, 
which is a dictionary containing a key for each FileField (or ImageField, or other FileField subclass) in the form. 
So the data from the above form would be accessible as request.FILES['file']. """
#IMPORTANTE
""" request.FILES will only contain data if the request method was POST, 
at least one file field was actually posted, 
and the <form> that posted the request has the attribute enctype="multipart/form-data" """