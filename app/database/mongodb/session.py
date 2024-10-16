import pymongo

from typing import Any, List

from app.common.config import config

class MongoHandler:
    def __init__(
        self,
        db_name: str,
        collection_name: str
    ):  # 생성자 함수를 코딩한다.
        self._mongo = pymongo.MongoClient(config.MONGODB.CONNECTION_STRING)
        self._db_name = db_name
        self._collection_name = collection_name

    def __enter__(self): # 클래스의 처음에서 호출되는 마법함수를 구현합니다.
        return self

    def __exit__(self, type, value, traceback): # 클래스의 마지막에서 호출되는 마법함수를 구현합니다.
        self._mongo.close()
        
    def close(self):
        self._mongo.close()
    
    def ping(self):
        return self._mongo.server_info()
    
    def find_one(
        self,
        condition: dict=None,
        sort: List[tuple]=[],
        collection_name: str=None
    ) -> dict: # 단일 검색
        if collection_name is None:
            collection_name = self._collection_name
        
        # print(self._db_name, collection_name)
        result = self._mongo[self._db_name][collection_name].find_one(filter=condition, sort=sort)
        return result

    def find_many(
        self,
        condition: dict=None,
        sort: List[tuple]=[],
        limit: int=None,
        projection: dict=None,
        collection_name: str=None
    ) -> List[dict]: # 다중 검색
        if collection_name is None:
            collection_name = self._collection_name
            
        params = {
            'filter': condition,
            'sort': sort,
            'limit': limit,
            'projection': projection
        }
        
        if limit is None:
            del params['limit']
            
        results = self._mongo[self._db_name][collection_name].find(**params)
        return list(results)

    def insert_one(
        self,
        data: dict=None,
        collection_name: str=None
    ) -> Any:  # 단일 Document 삽입
        if collection_name is None:
            collection_name = self._collection_name
        
        result = self._mongo[self._db_name][collection_name].insert_one(data)
        return result.inserted_id

    def insert_many(
        self,
        data: List[dict]=None,
        collection_name: str=None
    ) -> List[Any]:  #다중 Document 삽입
        if collection_name is None:
            collection_name = self._collection_name
        
        result = self._mongo[self._db_name][collection_name].insert_many(data)
        return result.inserted_ids

    def update_one(
        self,
        condition: dict=None,
        update_value: dict=None,
        upsert: bool=False,
        collection_name: str=None
    ):  # 단일 Document 업데이트
        if collection_name is None:
            collection_name = self._collection_name
        result = self._mongo[self._db_name][collection_name].update_one(
            filter=condition, update=update_value, upsert=upsert
        )
        return result.upserted_id

    def update_many(
        self,
        condition: dict=None,
        update_value: List[dict]=None,
        upsert: bool=False,
        collection_name: str=None
    ):  # 다중 Document 업데이트
        if collection_name is None:
            collection_name = self._collection_name
            
        result = self._mongo[self._db_name][collection_name].update_many(
            filter=condition, update=update_value, upsert=upsert
        )
        return result.upserted_id

    def delete_one(
        self,
        condition: dict=None,
        collection_name: str=None
    ) -> int:  # 단일 Document 삭제 
        if collection_name is None:
            collection_name = self._collection_name
        result = self._mongo[self._db_name][collection_name].delete_one(condition)
        return result.deleted_count

    def delete_many(
        self,
        condition: dict=None,
        collection_name: str=None
    ) -> int:  # 다중 Document 삭제
        if collection_name is None:
            collection_name = self._collection_name
        results = self._mongo[self._db_name][collection_name].delete_many(condition)
        return results.deleted_count
    
    def aggregate(
        self,
        pipeline: List[dict],
        collection_name: str=None
    ) -> List[dict]:
        if collection_name is None:
            collection_name = self._collection_name
        results = self._mongo[self._db_name][collection_name].aggregate(pipeline)
        return list(results)