import psycopg2

class Postgre:

    def __init__(self,database="database", user="user", password="password", host="192.68.1.1", port="5435"):
        self.connexion = psycopg2.connect(database = database, user = user , password = password , host=host , port=port)

    def sql(self,sql,data=None):
        cursor = self.connexion.cursor()
        cursor.execute(sql,data)
        self.connexion.commit()

    def insert(self,table,data):
        colonnes = ", ".join(data.keys())
        valeurs = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table} ({colonnes}) VALUES ({valeurs}) ON CONFLICT DO NOTHING"
        # Création du curseur
        curseur = self.connexion.cursor()
        # Insertion
        curseur.execute(query, tuple(data.values()))
        self.connexion.commit()
        curseur.close()

    def flushTable(self,table):
        curseur = self.connexion.cursor()
        curseur.execute(f"DELETE FROM {table}")
        self.connexion.commit()
        self.connexion.close()

    def deleteBy(self,table,key,value):
        curseur = self.connexion.cursor()
        curseur.execute(f"DELETE FROM {table} WHERE {key} = '{value}'")
        self.connexion.commit()
        self.connexion.close()

    def close(self):
        self.connexion.close()