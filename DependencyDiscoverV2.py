from fileinput import filename
import pathlib
import os
from itertools import chain
from warnings import catch_warnings
from tqdm import tqdm
import pandas as pd
import re
import helpers as help


SoftwareLocation = "Systems\Software"

def rootProjectWalker():
    projects = pathlib.Path(SoftwareLocation)
    for project in projects.iterdir():
        name = project.name

        # Discover Project Java Files here
        javaLocations = looking4Java(project)
        # Looks at each Java Class to look nested classes and subclasses
        classList = []
        print("Identifying Classes within the Project \n")
        for location in tqdm(javaLocations):
            output = inspectFile4Classes(location)

            if output:
                classList.append(output)
        

        flatClassList = list(chain.from_iterable(classList))

        # Looks for dependency matches within files, needs to be updated
        dependencyList = []
        print("Discovering Dependencies within the Project \n")
        for location in tqdm(javaLocations):
            output = dependencyMatcher(location, flatClassList)
            dependencyList.append(output)
            
        

        flatDependencyList = list(chain.from_iterable(dependencyList))

        if(flatDependencyList != []):
            df = pd.DataFrame(flatDependencyList)
            df.to_csv(str('Systems\myOutput\\'+name+'.csv'), index=False, header=False)
            print(name, "Done Processing \n")




# Function identifies all Java files within the project
# Adds the directory to the list so that it can be referenced and looked at
def looking4Java(project):
    javaFileLocs  = []
    for root, dir, files in os.walk(project.absolute()):
        for file in files:
            if file.endswith(".java"):
                location = os.path.join(root, file)
                javaFileLocs.append(location)

    return javaFileLocs

# Reads the entire java class and stored it temporary to prevent data alterations
# Removes any comments that may cause problems
# Looks for any classes, both sub classes and super classes
def inspectFile4Classes(file):
    currentFile = open(file, encoding="utf-8", errors="ignore")
    fileContents = currentFile.read()
    currentFile.close()

    removedComments = help.deleteComments(fileContents)

    # Used to look for classes within comments
    classes = ["".join(x) for x in re.findall(r"((?<=class)|(?<=interface))\ (\w+)", removedComments)]

    
    return classes



def dependencyMatcher(file, classList):
    dependencies = []
    currentFile = open(file, encoding="utf-8", errors="ignore")
    fileContents = currentFile.read()
    currentFile.close()

    filename = str(os.path.basename(file)).removesuffix(".java")

    removedComments = help.deleteComments(fileContents)


    # Seperation of document into different sections based on class detection
    # First instance is the original class that the java file is named after
    # Consecuative instances
    classes = ["".join(x) for x in re.findall(r"((?<=class)|(?<=interface))\ (\w+)", removedComments)]
    
    separationInstance = re.split("(?<= class )|(?<= interface )",removedComments)
    

    
    for sections in range(1, len(separationInstance)):
        print("\n",os.path.relpath(file))
        print(classes, len(separationInstance))
        try:
            currClass = classes[sections-1]


            for uniqueClass in classList:
                
                    if (currClass != uniqueClass):
                        match = re.search("([\ |\<|\.]?)"+uniqueClass+"([\>|\.|\ ]?)+([^0-z|\"])",separationInstance[sections])
                        if match:
                            dependencies.append([currClass, uniqueClass])
        except IndexError:
            print("Index Error Encounter")
    return dependencies

if __name__ == "__main__":
    rootProjectWalker()
