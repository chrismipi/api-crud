class DbUtils(object):
  @staticmethod
  def getDBTables(cur):
    cur.execute("select table_name from information_schema.tables where table_schema not in('pg_catalog', 'information_schema')")
    ver = cur.fetchall()
    tables_list = []
    for tname in ver:
      tables_list.append(tname[0])
    return tables_list