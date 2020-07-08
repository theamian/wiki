from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def site(request, site):
    if util.get_entry(site):
        print(util.get_entry(site))  
        content = markdown2.markdown(util.get_entry(site))
        print(content)
    else:
        content = None
    return render(request, "encyclopedia/site.html", {
        "site": site,
        "content": content
    })

def search(request):
    query = request.POST["q"]
    entryList = util.list_entries()

    if query in entryList:
        return HttpResponseRedirect(reverse("site", kwargs={"site": query}))

    else:
        newList = []
        print(f"newList je {newList}")
        for entry in entryList:
            if query.lower() in entry.lower():
                newList.append(entry)
        
        return render(request, "encyclopedia/results.html", {
            "newList": newList
        })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    
    title = request.POST["title"]
    content = request.POST["pgContent"]

    if util.get_entry(title):
        return render(request, "encyclopedia/create.html", {
            "error": "An entry with the same title already exists, please try again"
        })

    util.save_entry(title, content)

    return HttpResponseRedirect(reverse("site", kwargs={"site": title}))

def edit(request, site):
    content = util.get_entry(site)

    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "site": site,
            "content": content
        })
    
    newContent = request.POST["newContent"]
    util.save_entry(site, newContent)

    return HttpResponseRedirect(reverse("site", kwargs={"site": site}))

def rand(request):
    site = random.choice(util.list_entries())

    return HttpResponseRedirect(reverse("site", kwargs={"site": site}))
