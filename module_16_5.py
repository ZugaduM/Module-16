from fastapi import FastAPI, Path, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int

@app.get('/')
async def main(request: Request) ->HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get(path='/user/{user_id}')
async def get_user(request: Request, user_id: int) -> HTMLResponse:
  try:
      user = next(user for user in users if user.id == user_id)
      return templates.TemplateResponse('users.html', {'request': request, 'user': user})
  except IndexError:
      raise HTTPException(status_code=404, detail='User not found')


@app.post('/user/{username}/{age}')
async def new_user(user: User, username: str = Path(min_length=5, max_length=20, description='Enter user name'),
                   age: int = Path(ge=18, le=120)) -> str:
    try:
        if not users:
            user.id = 1
        else:
            user.id = len(users) + 1
        user.username = username
        user.age = age
    except IndexError as ie:
        return f'Error adding element. {ie.args}'
    except TypeError as te:
        return f'Wrong input data. {te.args}'
    else:
        users.append(user)
        return f'{users}'


@app.put('/user/{user_id}/{username}/{age}')
async def edit_user(user_id: int, username:str, age: int) -> str:
    try:
        user = next(user for user in users if user.id == user_id)
        user.username = username
        user.age = age
    except StopIteration:
        raise HTTPException(status_code=404, detail='User not found')
    else:
        return f'Data of user with id: {user_id} updated!'


@app.delete('/user/{user_id}')
async def remove_user(user_id: int) -> str:
    try:
        user = next(user for user in users if user.id == user_id)
        users.remove(user)
    except StopIteration:
        raise HTTPException(status_code=404, detail='User not found')
    else:
        return f'User with id: {user_id} has been deleted!'
