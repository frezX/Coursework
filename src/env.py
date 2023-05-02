from env_attributes import Environment
from src.schemes.env.server import EnvTypesDB, EnvTypesApp

db_env: Environment = Environment(env_path='env/server/db.env', env_types=EnvTypesDB)
app_env: Environment = Environment(env_path='env/server/app.env', env_types=EnvTypesApp)
