from fastapi import APIRouter, HTTPException
from psycopg2 import Error
from utils.data_preprocessing import connect_to_db, insert_data, create_table

router = APIRouter()

@router.post("/create_table")
async def create_table_endpoint():
    try:
        conn = connect_to_db()
        create_table(conn)
        return {"message": "Table created successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/insert_data")
async def insert_data_endpoint(image: bytes, label: str):
    try:
        conn = connect_to_db()
        insert_data(conn, image, label)
        return {"message": "Data inserted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_data")
async def get_data_endpoint():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM images")
        data = cur.fetchall()
        return {"data": data}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))