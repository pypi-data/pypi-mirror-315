from pyemon.task import *
from pyemon.directory import *
from .template import *
import glob

class RenderTask(Task):
  def run(self, argv):
    for path in glob.glob("**/*.tngn", recursive = True):
      names = Directory.split(path)
      names[-1] = os.path.splitext(names[-1])[0]
      with open(path) as file:
        Template.set(Template(file.read(), ".".join(names)))
    if len(argv) == 0:
      strings = ["<Templates>"]
      for template in Template.templates():
        strings.append("""  {}""".format(template.Name))
        strings.append("```")
        strings.append(template.Format)
        strings.append("```")
        strings.append("")
      sys.exit("\n".join(strings))
    else:
      print(Template.render(argv), end = "")
Task.set(RenderTask("<tngn name> <strings>"))

Task.parse_if_main(__name__, Task.get("help"))
def main():
  pass
