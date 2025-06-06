
import asyncio
import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from router import router as books_router

from queries.orm import AsyncORM

async def main():
    await AsyncORM.create_tables()
    await AsyncORM.insert_books()
    await AsyncORM.insert_users_test()


def create_fastapi_app():
    app = FastAPI(title="FastAPI")
    app.include_router(books_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    )
        
    return app

   
    

app = create_fastapi_app()


if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run(
    app="src.main:app",
    reload=True,
        )
