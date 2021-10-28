import psycopg2
from config import config

def editItems(item_id, item_orderdetails_id, q1, q2, q3, q4):
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        sql_update_query = """Update public."PPMP_orderdetails" set first_quantity = %s where id = %s"""
        cursor.execute(sql_update_query, (q1, item_orderdetails_id))
        connection.commit()

        sql_update_query = """Update public."PPMP_orderdetails" set second_quantity 
        = %s where id = %s"""
        cursor.execute(sql_update_query, (q2, item_orderdetails_id))
        connection.commit()

        sql_update_query = """Update public."PPMP_orderdetails" set third_quantity 
        = %s where id = %s"""
        cursor.execute(sql_update_query, (q3, item_orderdetails_id))
        connection.commit()

        sql_update_query = """Update public."PPMP_orderdetails" set fourth_quantity 
        = %s where id = %s"""
        cursor.execute(sql_update_query, (q4, item_orderdetails_id))
        connection.commit()

        if item_id:
            sql_update_query = """Update public."PPMP_orderdetails" set item_description_id_id 
            = %s where id = %s"""
            cursor.execute(sql_update_query, (item_id, item_orderdetails_id))
            connection.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error in update operation", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")        