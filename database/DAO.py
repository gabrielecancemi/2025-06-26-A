from collections import defaultdict

from database.DB_connect import DBConnect
from model.circuit import Circuito
from model.piazzamento import Piazzamento


class DAO():
    @staticmethod
    def getAnni():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct(year) from seasons s order by year desc"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["year"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getPiazzamenti(inizio, fine, id):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select year, driverId, position from races ra, results re where ra.raceId = re.raceId
                    and ra.`year`  >= %s and ra.`year` <= %s and ra.circuitId = %s"""
        cursor.execute(query, (inizio, fine, id))

        res = defaultdict(list)
        for row in cursor:
            res[row["year"]].append(Piazzamento(row["driverId"], row["position"]))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getNodi():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select * from circuits"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Circuito(**row))

        cursor.close()
        cnx.close()
        return res

