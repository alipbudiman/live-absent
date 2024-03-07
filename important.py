from flask import Flask, jsonify, request, send_from_directory, render_template, redirect
from pymongo import MongoClient
from datetime import datetime
import uuid, pytz, livejson

import pandas as pd

from PIL import Image, ImageDraw, ImageFont
import concurrent.futures

class Config:
    def __init__(self) -> None:
        config = livejson.File("config.json", True, True, 4)
        self.mongodb_url = config["mongo_client"]