#!/bin/bash
gunicorn --workers 13 --threads 5 --bind 0.0.0.0:4711 abatix.wsgi
