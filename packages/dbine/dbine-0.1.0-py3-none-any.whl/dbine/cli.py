import sys
from .list import *
from .connection import *
import graspgraph as gg

def main():
  argv = ListHelper(sys.argv)
  argv.shift()
  match argv.shift():
    case "graph":
      yamlFilePath = argv.shift()
      if yamlFilePath is None:
        return
      yamlPath = gg.Path.from_file_path(yamlFilePath)
      connectionOptions = ConnectionOptions.from_file_path(yamlFilePath)
      with Connection(connectionOptions) as connection:
        pdfFilePath = argv.shift()
        if pdfFilePath is None:
          pdfFilePath = gg.Path.join(yamlPath.File, "pdf", yamlPath.Directory)
        dbergraph = gg.Dbergraph(connection.get_database())
        dbergraph.Database.update()
        dbergraph.to_dot_helper().write_image(pdfFilePath)
    case "pdf":
      match argv.shift():
        case "convert":
          fromFilePath = argv.shift()
          toFilePath = argv.shift()
          if fromFilePath is not None and toFilePath is not None:
            gg.Pdf.convert(fromFilePath, toFilePath)
