from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    current_entry = util.get_entry(entry)
    if current_entry:
        return render(request, "encyclopedia/entry.html", {
            "text": markdown2.markdown(current_entry),
            "entry_name": entry
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "entry_name": entry
        })

def search(request):
    query = request.GET.get('q','')
    if(util.get_entry(query) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': query }))
    else:
        entries = []
        for entry in util.list_entries():
            if query.upper() in entry.upper():
                entries.append(entry)

        return render(request, "encyclopedia/search.html", {
            "entries": entries,
            "search": True,
            "value": query
            })

def new_entry(request):
    return render(request, "encyclopedia/new_entry.html")

def save(request):
    if request.method == "POST":
        entry_name = request.POST['entry_name']
        entry_content = request.POST["entry_content"]
        entries = util.list_entries()

        existing_entry = False
        for entry in entries:
            if entry_name.upper() == entry.upper():
                existing_entry = True

        if existing_entry == True:
            return render(request, "encyclopedia/error_existing_entry.html")
        else:
            util.save_entry(entry_name, entry_content)
            return render(request, "encyclopedia/entry.html", {
                "text": markdown2.markdown(entry_content),
                "entry_name": entry_name
            })

def edit_entry(request):
    if request.method == "POST":
        entry_name = request.POST.get('entry_name', False)
        entry_content = util.get_entry(entry_name)

    return render(request, "encyclopedia/edit_entry.html", {
        "text": entry_content,
        "entry_name": entry_name
    })

def save_edit(request):
    if request.method == "POST":
        entry_name = request.POST['entry_name']
        entry_content = request.POST['entry_content']
        util.save_entry(entry_name, entry_content)
        
        return render(request, "encyclopedia/entry.html", {
            "text": markdown2.markdown(entry_content),
            "entry_name": entry_name
        })


def random_entry(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    entry_content = markdown2.markdown(util.get_entry(entry))

    return render(request, "encyclopedia/entry.html", {
        "text": entry_content,
        "entry_name": entry
    })



        

