
def about(request):
    return render(request, "common/about.html", context={"components": OPEN_SOURCE_COMPONENTS})
