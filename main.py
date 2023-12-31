from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

@app.get('/')
async def root():
    return {'Example string'}

@app.post('/')
async def get_post() -> Timestamp:
    return post_db[0]

@app.get('/dog')
async def get_dogs(kind: DogType) -> list[Dog]:
    return [dog for dog in dogs_db.values() if dog.kind == kind]

@app.post('/dog')
async def create_dog(dog: Dog) -> Dog:
    if dog.pk in dogs_db:
        raise HTTPException(status_code=422, detail='Dog already exists')
    dogs_db[dog.pk] = dog
    return dogs_db[dog.pk]

@app.get('/dog/{pk}')
async def get_dog_by_pk(pk: int) -> Dog:
    if pk not in dogs_db:
        raise HTTPException(status_code=422, detail=f'No dog with {pk} index')
    return dogs_db[pk] 

@app.patch('/dog/{pk}')
async def update_dog(pk: int, dog: Dog) -> Dog:
    if pk not in dogs_db:
        raise HTTPException(status_code=422, detail=f'No dog with {pk} index')
    dogs_db[pk] = dog
    return dogs_db[pk]