from django.shortcuts import render
from django.shortcuts import redirect 
from django.http import HttpRequest, HttpResponseRedirect
from markdown2 import Markdown
from random import randint

from . import util
from .forms import NewEntryForm, EditEntryForm

markdowner = Markdown()

def index(request):
    if request.method=="POST":
        search_data= request.POST
        search_term = search_data.get("q")
         
        if util.get_entry(search_term):
            return HttpResponseRedirect(f"/wiki/{search_term}")
        
        else:
            return HttpResponseRedirect(f"/search/{search_term}")

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "random_title": util.list_entries()[randint(0, len(util.list_entries())-1)]
        })

def search_results(request, search_term):
    matching_results = []
    for entry in util.list_entries():
        if search_term.lower() in entry.lower():
            matching_results.append(entry)

    return render(request, "encyclopedia/search.html", {
        "search_term": search_term,
        "matching_results": matching_results
    })    

def entry_page(request, title):
    if util.get_entry(title) is not None:
        return render(request, "encyclopedia/entry_page.html", {
            "title": title.capitalize(),
            "htmlcontent":  markdowner.convert(util.get_entry(title))
        })
    else:
        return render(request, "encyclopedia/error_page.html", {
                    "title": "Page not found",
                    "htmlcontent": f"It looks like the page titled '{title}'  you're looking for does not exist"
                })	   

def new_page(request):
    if request.method=="POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["new_title"]
            content = form.cleaned_data["new_body"]

            
            if util.get_entry(title):
                return render(request, "encyclopedia/error_page.html", {
                    "title": "Duplicate entry",
                    "htmlcontent": "It looks like an entry with this title already exists"
                })

            
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return render (request, "encyclopedia/new_page.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": NewEntryForm()
        })
    


def edit_page(request, title):
    if request.method=="POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["edit_body"]

            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return render (request, "encyclopedia/edit_page.html", {
                "form": form
            })
    else:
        form = EditEntryForm(initial={'edit_body': util.get_entry(title)})
        return render(request, "encyclopedia/edit_page.html", {
            "title": title.capitalize(),
            "form": form
        })


def random_page(request):
    title = util.list_entries()[randint(0, len(util.list_entries())-1)]
    return HttpResponseRedirect(f"/wiki/{title}")