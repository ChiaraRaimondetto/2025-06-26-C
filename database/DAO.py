from database.DB_connect import DBConnect
from model.arco import Arco
from model.costruttore import Costructor
from model.result import Result


class DAO():
    @staticmethod
    def getAllConstructors():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from constructors"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Costructor(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct s.`year` as y
                        from seasons s """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row["y"])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getResults(id_costr,anno):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
                    
            select r2.driverId ,r2.`position` 
            from races r ,results r2 
            where r.raceId =r2.raceId and r.`year` =%s and r2.constructorId =%s and r2.`position` is not null
        """
        cursor.execute(query,(anno,id_costr))

        res = []
        for row in cursor:
            res.append(Result(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllEdges(min,max,idMap):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
        select t1.constructorid as c1,t2.constructorid as c2,sum(t1.totgare +t2.totgare ) as peso
        from (select r2.constructorId ,count(*) as totGare
        from races r ,results r2 
        where r.raceId =r2.raceId and r.`year` between %s and %s and r2.`position` is not null 
        group by r2.constructorId ) t1,
        (select r2.constructorId ,count(*) as totGare
        from races r ,results r2 
        where r.raceId =r2.raceId and r.`year` between %s and %s and r2.`position` is not null 
        group by r2.constructorId ) t2
        where t1.constructorid>t2.constructorid  
        group by t1.constructorid ,t2.constructorid 
        """
        cursor.execute(query, (min,max,min,max))

        res = []
        for row in cursor:
            res.append(Arco(idMap[row["c1"]],idMap[row["c2"]],row["peso"]))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getCampionatiPerC(constr,min,max):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
            select q.raceId as r
            from qualifying q, races r 
            where q.raceId =r.raceId and r.`year` between %s and %s and q.constructorId =%s
            group by r.`year`
                """
        cursor.execute(query, (min,max,constr.constructorId))

        res = []
        for row in cursor:
            res.append(row["r"])

        cursor.close()
        cnx.close()
        return len(res)

    @staticmethod
    def getD(id_costr, anno):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """

            select r2.driverId ,r2.`position` 
            from races r ,results r2 
            where r.raceId =r2.raceId and r.`year` =%s and r2.constructorId =%s 
        """
        cursor.execute(query, (anno, id_costr))

        res = []
        for row in cursor:
            res.append(Result(**row))

        cursor.close()
        cnx.close()
        return res

