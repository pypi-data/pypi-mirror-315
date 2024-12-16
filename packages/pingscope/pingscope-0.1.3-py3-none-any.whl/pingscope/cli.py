from pyemon.list import *
from pyemon.task import *
from pyemon.status import *
import pingscope as ps

class PingTask(Task):
  def run(self, argv):
    pingFileName = List.shift(argv)
    dst = List.shift(argv)
    if pingFileName is not None and dst is not None:
      count = int(List.shift(argv, "5"))
      maxCount = int(List.shift(argv, "30"))
      pingscope = ps.Pingscope(maxCount)
      pingFilePath = """{}.ping""".format(pingFileName)
      pingscope.save(pingFilePath, dst, count)
      print(FileStatus(pingFilePath, "done"))
      pngFilePath = """{}.png""".format(pingFileName)
      pingscope.to_figure().Write(pngFilePath)
      print(FileStatus(pngFilePath, "done"))
Task.set(PingTask("<ping file name> <dst> <count> <max count>"))

Task.parse_if_main(__name__, Task.get("help"))
def main():
  pass
