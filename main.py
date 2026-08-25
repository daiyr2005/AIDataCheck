from fastapi import FastAPI
import uvicorn
from mysite.db.db import Base, engine
from mysite.db import model # импорт моделей ОБЯЗАТЕЛЕН
from mysite.admin.setup import setup_admin
from mysite.api import user, auth, agent, objects


Base.metadata.create_all(bind=engine)

user_app = FastAPI(title="User")
user_app.include_router(user.user_router)
user_app.include_router(auth.auth_router)
user_app.include_router(agent.agent_router)
user_app.include_router(objects.object_router)
setup_admin(user_app)



if __name__ == "__main__":
    uvicorn.run(user_app, host="127.0.0.1", port=8001)