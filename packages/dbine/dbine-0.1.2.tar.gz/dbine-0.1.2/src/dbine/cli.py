import sys
from .list import *
from .connection import *
import graspgraph as gg

def main():
  argv = ListHelper(sys.argv)
  argv.shift()
  match argv.shift():
    case "pdf":
      match argv.shift():
        case "write":
          yamlFilePath = argv.shift()
          if yamlFilePath is None:
            return
          yamlPath = gg.Path.from_file_path(yamlFilePath)
          with Connection(ConnectionConfig.from_file_path(yamlFilePath)) as connection:
            pdfFilePath = argv.shift()
            if pdfFilePath is None:
              pdfFilePath = gg.Path.join(yamlPath.File, "pdf", yamlPath.Directory)
            dbergraph = gg.Dbergraph(connection.get_database())
            dbergraph.Database.update()
            dbergraph.to_dot_helper().write_image(pdfFilePath, cleanup = True)
            print("""\033[40m\033[36m{}\033[0m is done.""".format(pdfFilePath))
        case "convert":
          fromFilePath = argv.shift()
          toFilePath = argv.shift()
          if fromFilePath is not None and toFilePath is not None:
            gg.Pdf.convert(fromFilePath, toFilePath)
            print("""\033[40m\033[36m{}\033[0m is done.""".format(toFilePath))
