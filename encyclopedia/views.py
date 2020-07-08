from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def site(request, site):
    if util.get_entry(site):  
        content = markdown2.markdown(util.get_entry(site))
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
                print(f"query je {query.lower()}")
                print(f"entry je {entry.lower()}")
                newList.append(entry)
                print(f"newList je sad {newList}")
        
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