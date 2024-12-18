from pyemon.task import *
from pyemon.directory import *
from pyemon.option import *
from pyemon.status import *
from .template import *
import glob

class RenderTask(Task):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.OptionParser = OptionParser([Option("o", "output", "", "Output file path")])

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
      self.OptionParser.parse(argv)
      value = Template.render(self.OptionParser.Argv)
      if value is None:
        return
      outputFilePath = self.OptionParser.find_option_from_long_name("output").Value
      if len(outputFilePath) == 0:
        print(value, end = "")
      else:
        with open(outputFilePath, "w", encoding = "utf-8", newline = "\n") as file:
          file.write(value)
        print(FileStatus(outputFilePath, "done"))
Task.set(RenderTask("<template name> <args>"))

Task.parse_if_main(__name__, Task.get("help"))
def main():
  pass
