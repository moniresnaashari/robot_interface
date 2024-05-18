import ast

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models
from app.config import settings
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def current_position(db):
    """
    Get current position. Firstly try to get from database and if does not
    exist get it from initial value
    """
    last_command_position = (
        db.query(models.CommandsPosition)
        .order_by(models.CommandsPosition.id.desc())
        .first()
    )
    if last_command_position:
        result = (
            last_command_position.x,
            last_command_position.y,
        ), last_command_position.direction
    else:
        current_position = settings.current_position
        current_position = ast.literal_eval(current_position)
        result = (
            current_position[0][0],
            current_position[0][1],
        ), current_position[1]
    return result


@app.get('/')
def root():
    return {'message': 'Hello Robot'}


@app.get('/current-position')
def get_current_position(db: Session = Depends(get_db)):
    try:
        (x, y), direction = current_position(db)
    except Exception:
        raise HTTPException(status_code=400, detail='Bad request')
    return {'position': f'({x}, {y}), {direction}'}


@app.get('/execute-command/{command}')
def execute_command(command: str, db: Session = Depends(get_db)):
    try:
        (x, y), direction = current_position(db)
        change_position_dict = {
            'F,EAST': {'x': 1, 'y': 0, 'direction': 'EAST'},
            'B,EAST': {'x': -1, 'y': 0, 'direction': 'EAST'},
            'L,EAST': {'x': 0, 'y': 0, 'direction': 'NORTH'},
            'R,EAST': {'x': 0, 'y': 0, 'direction': 'SOUTH'},
            'F,WEST': {'x': -1, 'y': 0, 'direction': 'WEST'},
            'B,WEST': {'x': 1, 'y': 0, 'direction': 'WEST'},
            'L,WEST': {'x': 0, 'y': 0, 'direction': 'SOUTH'},
            'R,WEST': {'x': 0, 'y': 0, 'direction': 'NORTH'},
            'F,NORTH': {'x': 0, 'y': 1, 'direction': 'NORTH'},
            'B,NORTH': {'x': 0, 'y': -1, 'direction': 'NORTH'},
            'L,NORTH': {'x': 0, 'y': 0, 'direction': 'WEST'},
            'R,NORTH': {'x': 0, 'y': 0, 'direction': 'EAST'},
            'F,SOUTH': {'x': 0, 'y': -1, 'direction': 'SOUTH'},
            'B,SOUTH': {'x': 0, 'y': 1, 'direction': 'SOUTH'},
            'L,SOUTH': {'x': 0, 'y': 0, 'direction': 'EAST'},
            'R,SOUTH': {'x': 0, 'y': 0, 'direction': 'WEST'},
        }
        reach_obstacle = False
        for c in command:
            change_value = change_position_dict[f'{c},{direction}']
            if (
                x + change_value['x'],
                y + change_value['y'],
            ) in settings.obstacles:
                reach_obstacle = True
                break
            else:
                x = x + change_value['x']
                y = y + change_value['y']
                direction = change_value['direction']

        entry = models.CommandsPosition(
            command=command, x=x, y=y, direction=direction
        )
        db.add(entry)
        db.commit()
    except Exception:
        raise HTTPException(status_code=400, detail='Bad request')
    return {
        'position': f'({x}, {y}), {direction}'
        f'{" STOPPED" if reach_obstacle else ""}'
    }
