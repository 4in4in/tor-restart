#!/bin/bash

HOST='0.0.0.0'
PORT=8001

uvicorn main:app --host=$HOST --port=$PORT
