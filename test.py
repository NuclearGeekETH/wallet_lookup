import json

import quart
import quart_cors
from quart import request
from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

url: str = os.environ["SUPABASE_URL"]
key: str = os.environ["SUPABASE_SERVICE_API_KEY"]

supabase: Client = create_client(url, key)

def get_signatures(address=None):
    query = supabase.table('arye').select("*")
    if address:
        query = query.eq("address", address)
    data, count = query.execute()
    return data[1] if data else []

data = get_signatures("0xeD4467f352B2b346D39B33adB24BACB8FB665a68")
print(data[0]['signature'])