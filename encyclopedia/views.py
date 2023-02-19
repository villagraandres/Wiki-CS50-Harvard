from django.shortcuts import render
import markdown2
from . import util
from django.http import HttpResponseRedirect;
from django.http import HttpResponse;
from django import forms;
import secrets;

class NewEntry(forms.Form):
    title=forms.CharField(label="Title");
    body=forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 5}));


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def showEntry(request,title):
    
    entry=util.get_entry(title);

    
    search=request.GET.get('q');
    if(search is not None ):
        if(util.get_entry(search) is not None):
         return HttpResponseRedirect(f"/wiki/{search}");
        else:
            results= util.recomendations(search);
            return render(request, "encyclopedia/search.html", {
                    "results": results
                })
   
    


    if entry is None:
        return render(request, "encyclopedia/errorPage.html", {
            "message": "Page not found"
        })
    else:
        
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(entry)
        })

def search(request):
   
   title=request.GET.get('q');
   if(util.get_entry(title) is not None):
         return HttpResponseRedirect(f"/wiki/{title}");
   else:
     results= util.recomendations(title);
     return render(request, "encyclopedia/search.html", {
            "results": results
        })

def add(request):
    if request.method=="POST":
        form= NewEntry(request.POST);
        if form.is_valid():
            title=form.cleaned_data['title'];
            body=form.cleaned_data['body'];
            entries=util.list_entries();
            for entry in entries:
                if(title==entry):
                     return render(request,"encyclopedia/add.html",{
                         "form":NewEntry(),
                        "error":"The entry already exists!"
                        
                     })
            util.save_entry(title,body);    
            return HttpResponseRedirect(f"/wiki/{title}");
        else:
             return render(request,"encyclopedia/add.html",{
                         "form":NewEntry(),
                        "error":"Complete all the fields!"
                        
                     })

    return render(request,"encyclopedia/add.html",{
        "form":NewEntry()
    })


def edit(request):
    title=request.GET.get('title');
    entry=util.get_entry(title);

    if request.method=="POST":
         entry=request.POST['body'];
         util.save_entry(title,entry);
         return HttpResponseRedirect(f"/wiki/{title}");
    return render(request,"encyclopedia/edit.html",{
        "entry":entry
    });

def randomEntry(request):
    entries=util.list_entries();
    randomChoice=secrets.choice(entries);
    
    return HttpResponseRedirect(f"/wiki/{randomChoice}");

