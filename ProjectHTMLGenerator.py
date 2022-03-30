from hmac import new
import xml.etree.ElementTree as ET
import sys
import os
import dominate
from dominate.tags import *
from dominate.util import raw

#will generate a new HTML document given the xml documents within a directory
def GenerateHTMLProjects(inputDirectory : str, outDirectory : str) -> None:
    for fileName in os.listdir(outDirectory):
        os.remove(os.path.join(outDirectory,fileName))
    
    fileList : list = []
    for fileName in os.listdir(inputDirectory):
        if os.path.splitext(fileName)[1] == ".xml":
            fileList.append(ET.parse(os.path.join(inputDirectory,fileName)))

    for file in fileList:
        xmlRoot = file.getroot()
        newHTMLDocument : dominate.document = dominate.document()
        with newHTMLDocument.head:
            #ADD SCRIPTS AND LINKS HERE
            try:
                link(rel="stylesheet",type="text/css",href="../css/index.css",media="screen")
                link(href="../prism/prism.css",rel="stylesheet")
                script(src="../prism/prism.js")
            except:
                print("ERROR : check scripts they might be missing")
            try:
                newHTMLDocument.head.children[0].text = xmlRoot.find("title").text
            except:
                newHTMLDocument.head.children[0].text = "put in a title here"
        with newHTMLDocument.body:
            
            with header():
                try:
                    h1(xmlRoot.find("h1").text, id="pageHeader")
                except:
                    h1("add in your header1", id="pageHeader")
                    
                with nav():
                    a("Home",cls="Link", href="../index.html")
                    a("Projects List",cls="Link", href="../html/ProjectsList.html")
                    a("Hobby Projects",cls="Link", href="../html/HobbyProjects.html")
                    a("College Projects",cls="Link", href="../html/CollegeProjects.html")
                
            # setup the article
            with article():
                try:
                    h2(xmlRoot.find("h2").text, id="shortDescription")
                except:
                    h2("add in your header1", id="shortDescription")
                    
                #setup a short description with a b tag, ul tag, and li tags
                with b(id="longDescription"):
                    with ul():
                        try:
                            for newLi in xmlRoot.find("b").find("ul"):
                                try:
                                    li(newLi.text)
                                except:
                                    li("ERROR : this is empty fill this out")
                        except:
                            li("ERROR : make sure you put a b tag with a ul tag and your li tags nested in both for the long description")
                
                #setup a code tag
                try:
                    code(xmlRoot.find("code").text, id="code", cls=xmlRoot.find("code").attrib["class"])
                except:
                    code("ERROR : check your code tag either there is not any code OR the language class was not specified")
                    print("ERROR : check your code tag either there is not any code OR the language class was not specified")
                
                #setup a img tag
                try:
                    img(id="image",src=xmlRoot.find("img").attrib["src"])
                except:
                    print("ERROR : check your img tag on either there is not any code OR the language class was not specified")
                    img(id="image")
                    
            with footer():
                a("GitHub",href="https://github.com/elnachoes")
                p("corbin.martin@protonmail.com")

        #SAVE CONTENTS TO A FILE
        try:
            pathName : str = (os.path.join(outDirectory,xmlRoot.find("title").text))
        except:
            pathName : str = (os.path.join(outDirectory,"NOTITLE_ADDTITLETAG"))
        pathName = pathName.replace(" ","_")
        pathName = pathName.replace("\n","")
        with open(f"{pathName}.html","w") as file:
            file.write(f"{newHTMLDocument}")

def GenerateHTMLProjectsList(htmlProjectsDirectory : str) -> None:
    newHTMLDocument : dominate.document = dominate.document()
    with newHTMLDocument.head:
        #ADD SCRIPTS AND LINKS HERE
        try:
            link(rel="stylesheet",type="text/css",href="../css/index.css",media="screen")
            link(href="../prism/prism.css",rel="stylesheet")
            script(src="../prism/prism.js")
        except:
            print("ERROR : check scripts they might be missing")
            
        title("Projects List", id="pageTitle")
        
    with newHTMLDocument.body:
        
        with header():
            h1("full projects list", id="pageTitle")
            
            with nav():
                a("Home",cls="Link", href="../index.html")
                a("Projects List",cls="Link", href="ProjectsList.html")
                a("Hobby Projects",cls="Link", href="HobbyProjects.html")
                a("College Projects",cls="Link", href="CollegeProjects.html")

        with article():
            with ul():
                for fileName in os.listdir(htmlProjectsDirectory):
                    if os.path.splitext(fileName)[1] == ".html":
                        linkPath = os.path.join("../",htmlProjectsDirectory,fileName)
                        linkPath.replace("\\","/")
                        with p():
                            a(f"{os.path.splitext(fileName)[0]}",href=f"{linkPath}")

        with footer():
            a("GitHub",href="https://github.com/elnachoes")
            p("corbin.martin@protonmail.com")
        
    try:
        with open("html\\ProjectsList.html","w") as file:
            file.write(f"{newHTMLDocument}")
    except:
        print("ERROR : missing html directory")

#you have to call this program with a input directory
def main() -> None:
    GenerateHTMLProjects(sys.argv[1],sys.argv[2])
    GenerateHTMLProjectsList(sys.argv[2])

if __name__ == "__main__":
    main()