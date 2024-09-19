from fastapi import FastAPI, Path


app = FastAPI()
users = {'1': 'Имя: Example, возраст: 18'}

@app.get('/users')
async def get_users() -> dict:
  return users


@app.post('/user/{username}/{age}')
async def new_user(username: str = Path(min_length=5, max_length=20, description='Enter user name'),
                   age: int = Path(ge=18, le=120)) -> str:
    try:
        curr_index = str(int(max(users, key=int)) + 1)
        users[curr_index] = f'Имя: {username}, возраст: {age}'
    except IndexError as ie:
        return f'Error adding element. {ie.args}'
    except TypeError as te:
        return f'Wrong input data. {te.args}'
    else:
        return f'User {curr_index} is registered!'


@app.put('/user/{user_id}/{username}/{age}')
async def edit_user(user_id: str, username:str, age: int) -> str:
    try:
        users[user_id] = f'Имя: {username}, возраст: {age}'
    except IndexError as ie:
        return f'Error getting element by id. {ie.args}'
    except TypeError as te:
        return f'Wrong input data. {te.args}'
    else:
        return f'Data of user with id: {user_id} updated!'


@app.delete('/user/{user_id}')
async def remove_user(user_id: str) -> str:
    try:
        users.pop(user_id)
    except IndexError as ie:
        return f'Wrong id. {ie.args}'
    else:
        return f'User with id: {user_id} has been deleted!'
