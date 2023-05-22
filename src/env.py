from env_attributes import Environment
from src.schemes.environments.server import EnvTypesDB, EnvTypesApp

db_env: Environment = Environment(env_path='env/db.env', env_types=EnvTypesDB)
app_env: Environment = Environment(env_path='env/app.env', env_types=EnvTypesApp)
