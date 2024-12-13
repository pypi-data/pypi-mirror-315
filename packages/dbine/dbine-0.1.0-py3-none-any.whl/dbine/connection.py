from enum import Enum
import psycopg
import mysql.connector
from pydantic import BaseModel
import graspgraph as gg
import yaml

class Type(Enum):
  PostgreSQL = 1
  MySQL = 2

  @classmethod
  def from_name(cls, name):
    for type in Type:
      if type == name or type.name == name:
        return type
    return Type.PostgreSQL

  @classmethod
  def from_value(cls, value):
    for type in Type:
      if type == value or type.value == value:
        return type
    return Type.PostgreSQL

class ConnectionOptions(BaseModel):
  Type: Type
  DatabaseName: str
  UserName: str
  Password: str
  Host: str = "localhost"
  Port: str = ""

  def update(self):
    match self.Type:
      case Type.PostgreSQL:
        if len(self.Port) == 0:
          self.Port = "5432"
      case Type.MySQL:
        if len(self.Port) == 0:
          self.Port = "3306"
    return self

  def to_string(self):
    return " ".join([
      """dbname={}""".format(self.DatabaseName),
      """host={}""".format(self.Host),
      """port={}""".format(self.Port),
      """user={}""".format(self.UserName),
      """password={}""".format(self.Password),
    ])

  def to_dict(self):
    return {
      "database": self.DatabaseName,
      "host": self.Host,
      "port": self.Port,
      "user": self.UserName,
      "password": self.Password,
    }

  def load(self, filePath):
    with open(filePath, "r", encoding = "utf-8") as file:
      connectionOptions = ConnectionOptions.from_yaml(file)
      self.Type = connectionOptions.Type
      self.DatabaseName = connectionOptions.DatabaseName
      self.UserName = connectionOptions.UserName
      self.Password = connectionOptions.Password
      self.Host = connectionOptions.Host
      self.Port = connectionOptions.Port
    return self

  def save(self, filePath):
    gg.Path.from_file_path(filePath).makedirs()
    with open(filePath, "w", encoding = "utf-8", newline = "\n") as file:
      connectionOptions = self.model_dump()
      connectionOptions["Type"] = connectionOptions["Type"].name
      yaml.dump(connectionOptions, file, sort_keys = False, default_flow_style = False, allow_unicode = True)
    return self

  @classmethod
  def default_dict(cls):
    return {"Type": Type.PostgreSQL, "DatabaseName": "", "UserName": "", "Password": ""}

  @classmethod
  def from_yaml(cls, stream):
    connectionOptions = yaml.safe_load(stream) or ConnectionOptions.default_dict()
    connectionOptions["Type"] = Type.from_name(connectionOptions["Type"])
    return ConnectionOptions(**connectionOptions)

  @classmethod
  def from_file_path(cls, filePath):
    return ConnectionOptions(**ConnectionOptions.default_dict()).load(filePath)

class Connection:
  def __init__(self, connectionOptions):
    self.__Connections = []
    self.open(connectionOptions)

  @property
  def Cursor(self):
    if len(self.__Connections) == 0:
      return None
    return self.__Connections[0]

  def __enter__(self):
    return self

  def __exit__(self, *args):
    self.close()

  def open(self, connectionOptions):
    self.close()
    connectionOptions.update()
    self.ConnectionOptions = connectionOptions
    match connectionOptions.Type:
      case Type.PostgreSQL:
        connection = psycopg.connect(connectionOptions.to_string())
        self.__Connections = [connection.cursor(), connection]
      case Type.MySQL:
        connection = mysql.connector.connect(**connectionOptions.to_dict())
        self.__Connections = [connection.cursor(), connection]
    return self

  def close(self):
    if 0 < len(self.__Connections):
      for connection in self.__Connections:
        connection.close()
      self.__Connections = []
    return self

  def get_database(self):
    database = gg.Database()
    match self.ConnectionOptions.Type:
      case Type.PostgreSQL:
        cursor = self.Cursor
        cursor.execute("SELECT schemaname, tablename FROM pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'")
        for tableDefinitions in cursor.fetchall():
          table = gg.Table(**{"Namespace": """{}.{}""".format(self.ConnectionOptions.DatabaseName, tableDefinitions[0]), "Name": tableDefinitions[1]})
          cursor.execute("""SELECT pg_description.description FROM pg_class JOIN pg_description ON pg_class.oid = pg_description.objoid WHERE pg_class.relname = '{}' AND pg_description.objsubid = 0""".format(tableDefinitions[1]))
          if cursor.rowcount == 1:
            table.Comment = cursor.fetchone()[0]
          cursor.execute("""SELECT column_name, data_type, character_maximum_length, ordinal_position FROM information_schema.columns WHERE table_schema = '{}' AND table_name = '{}'""".format(*tableDefinitions))
          for columnDefinitions in cursor.fetchall():
            column = gg.Column(**{"Name": columnDefinitions[0], "Type": columnDefinitions[1].upper()})
            if columnDefinitions[2] is not None:
              column.Type = """{}({})""".format(column.Type, columnDefinitions[2])
            cursor.execute("""SELECT pg_description.description FROM pg_class JOIN pg_description ON pg_class.oid = pg_description.objoid WHERE pg_class.relname = '{}' AND pg_description.objsubid = {}""".format(tableDefinitions[1], columnDefinitions[3]))
            if cursor.rowcount == 1:
              column.Comment = cursor.fetchone()[0]
            cursor.execute("""SELECT constraint_type FROM information_schema.table_constraints JOIN information_schema.constraint_column_usage ON information_schema.table_constraints.constraint_name = information_schema.constraint_column_usage.constraint_name WHERE information_schema.constraint_column_usage.table_catalog = '{}' AND information_schema.constraint_column_usage.table_schema = '{}' AND information_schema.constraint_column_usage.table_name = '{}' AND information_schema.constraint_column_usage.column_name = '{}'""".format(self.ConnectionOptions.DatabaseName, tableDefinitions[0], tableDefinitions[1], columnDefinitions[0]))
            if cursor.rowcount == 1 and cursor.fetchone()[0] == "PRIMARY KEY":
              column.Caption = "PK"
            table.Columns.append(column)
          database.Tables.append(table)
      case Type.MySQL:
        cursor = self.Cursor
        cursor.execute("SHOW TABLE STATUS")
        for tableDefinitions in cursor.fetchall():
          table = gg.Table(**{"Namespace": self.ConnectionOptions.DatabaseName, "Name": tableDefinitions[0], "Comment": tableDefinitions[-1]})
          cursor.execute("""SHOW FULL COLUMNS FROM {}""".format(tableDefinitions[0]))
          for columnDefinitions in cursor.fetchall():
            caption = ""
            if columnDefinitions[4] == "PRI":
              caption = "PK"
            table.Columns.append(gg.Column(**{"Name": columnDefinitions[0], "Type": columnDefinitions[1].upper(), "Comment": columnDefinitions[-1], "Caption": caption}))
          database.Tables.append(table)
    return database
