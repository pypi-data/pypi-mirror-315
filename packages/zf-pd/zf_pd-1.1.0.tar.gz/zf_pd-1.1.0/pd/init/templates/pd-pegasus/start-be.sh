#!/bin/bash
source venv/bin/activate
python -m uvicorn app.main:app --reload