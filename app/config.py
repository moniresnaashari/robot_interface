from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_string: str = (
        'postgresql://ConsoleRole:Console1391@127.0.0.1/RobotDB'
    )
    current_position: str = "(4, 2), 'EAST'"
    obstacles: set = {(1, 4), (3, 5), (7, 4)}


settings = Settings()
