#! /usr/bin/python
 
import os
import glob
 
what_to_find = "*"
 
def do_something_with_directory(path, do_nothing=False):
    # Uncomment this if you need to do something with directories
    #return do_something(path, do_nothing)
    return path
 
 
def do_something(path, do_nothing=False):
    filepath, filename = os.path.split(path)
    if do_nothing:
        print "Do nothing with %s" % (path)
        return path
    else:
        # Replace this string with your code
        os.system("echo Done something with %s" % (path))
        #
        return path
 
def search(path=".", do_nothing=False):
    for item in glob.glob(os.path.join(path, what_to_find)):
        if os.path.isdir(item):
            search(do_something_with_directory(item, do_nothing), do_nothing)
        elif os.path.isfile(item):
            do_something(item, do_nothing)
 
 
def request_confirmation(text):
    resplist = { "yes": True, "y": True, "n": False, "no": False }
    while 1:
        print "%s [y\\n]:" % (text),
        choice = raw_input().lower()
        if choice.strip() in resplist:
            return resplist[choice.strip()]
 
 
if __name__ == "__main__":
    search(do_nothing=True)
    if request_confirmation("Do something with theese files"):
        search()
