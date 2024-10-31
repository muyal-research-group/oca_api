#!/bin/bash
uvicorn ocaapi.server:app --host ${OCA_HOST-0.0.0.0} --port ${OCA_PORT-5000} --reload
