
from pydantic import BaseModel

# Define class, extend BaseModel - pydantic - This is for schema and validation
class PostBase(BaseModel):
    title:  str
    content: str
    published: bool = False    

class PostCreate(PostBase):        
    pass

