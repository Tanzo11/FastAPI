from sqlalchemy.orm import Session
from sqlalchemy import text

def search(keyword: str, fastdb: Session):
    query = text('''
        SELECT link FROM products
        WHERE generalized_description LIKE :keyword
    ''')
    result = fastdb.execute(query, {"keyword": f"%{keyword}%"})
    print(result)
    return [row[0] for row in result.fetchall()]