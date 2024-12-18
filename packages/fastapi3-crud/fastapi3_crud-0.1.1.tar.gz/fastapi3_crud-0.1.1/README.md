# fastapi3_crud

基于fastapi3, 自动生成crud接口, 提高开发效率

## 快速入门教程

### 安装

```shell
pip install fastapi3
pip install sqlalchemy3
pip install fastapi3_crud
```

## 01.导入相关的依赖

```python
from sqlalchemy3 import Column, DateTime, Integer, Numeric, String, func
from sqlalchemy3.orm import DeclarativeBase, sessionmaker
from sqlalchemy3.ext.asyncio import AsyncSession, create_async_engine

import datetime
from typing import AsyncGenerator

from fastapi3 import FastAPI
from fastapi3_crud import crud_router
from fastapi3_crud import FastCRUD
from pydantic import BaseModel
```

## 02.定义数据库表模型

```python
class Base(DeclarativeBase):
    pass


# 数据库表模型
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
```

## 03.定义schema

```python
class UserSchema(BaseModel):
    name: str | None = None
    age: int | None = None
```

## 04.连接数据库

```python
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

## 05.创建应用实例

```python
# 在应用启动之前, 初始化数据库表格
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


# 创建app应用
app = FastAPI(lifespan=lifespan)
```

## 06.自动生成CRUD接口

```python
# 数据库session依赖注入
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


# 自动生成CRUD接口对象
user_crud = FastCRUD(User)

# 自动生成CRUD接口
item_router = crud_router(
    session=get_session,
    model=User,
    create_schema=UserSchema,
    update_schema=UserSchema,
    crud=user_crud,
    path="/user",
    tags=["用户管理"],
)

# 将CRUD接口注册到app上
app.include_router(item_router)
```

## 07.启动服务

```python
import uvicorn

uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 08.完整代码

```python
from sqlalchemy3 import Column, DateTime, Integer, Numeric, String, func
from sqlalchemy3.orm import DeclarativeBase, sessionmaker
from sqlalchemy3.ext.asyncio import AsyncSession, create_async_engine

from typing import AsyncGenerator

from fastapi3 import FastAPI
from fastapi3_crud import crud_router
from fastapi3_crud import FastCRUD
from pydantic import BaseModel


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


class UserSchema(BaseModel):
    name: str | None = None
    age: int | None = None


DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# 在应用启动之前, 初始化数据库表格
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


# 创建app应用
app = FastAPI(lifespan=lifespan)


# 数据库session依赖注入
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


# 自动生成CRUD接口对象
user_crud = FastCRUD(User)

# 自动生成CRUD接口
item_router = crud_router(
    session=get_session,
    model=User,
    create_schema=UserSchema,
    update_schema=UserSchema,
    crud=user_crud,
    path="/user",
    tags=["用户管理"],
)

# 将CRUD接口注册到app上
app.include_router(item_router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

