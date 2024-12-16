from .connection import *
from pyemon.list import *
from pyemon.task import *
from pyemon.status import *

class PdfWriteTask(Task):
  def run(self, argv):
    yamlFilePath = List.shift(argv)
    pdfFilePath = List.shift(argv)
    if yamlFilePath is None or pdfFilePath is None:
      return
    with Connection(ConnectionConfig.from_file_path(yamlFilePath)) as connection:
      dbergraph = gg.Dbergraph(connection.get_database())
      dbergraph.Database.update()
      dbergraph.to_dot().Save(pdfFilePath, cleanup = True)
      print(FileStatus(pdfFilePath, "done"))
Task.set(PdfWriteTask("<yaml file path> <pdf file path>"))

class PdfConvertTask(Task):
  def run(self, argv):
    pdfFilePath = List.shift(argv)
    imageFilePath = List.shift(argv)
    if pdfFilePath is not None and imageFilePath is not None:
      gg.Pdf.convert(pdfFilePath, imageFilePath)
      print(FileStatus(imageFilePath, "done"))
Task.set(PdfConvertTask("<pdf file path> <image file path>"))

Task.parse_if_main(__name__, Task.get("help"))
def main():
  pass
