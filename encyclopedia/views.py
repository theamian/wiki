from django.shortcuts import render
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def site(request, site):
    content = markdown2.markdown(util.get_entry(site))
    print(type(content))
    return render(request, "encyclopedia/site.html", {
        "site": site,
        "content": content
    })
