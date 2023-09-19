#!/usr/bin/python3
"""A module that defines a class User"""
from models.base_model import BaseModel


class User(BaseModel):
    """The class defines the user by various attributes"""
    email = ''
    password = ''
    first_name = ''
    last_name = ''
