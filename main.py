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


app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")


@app.post("/check_address/<string:address>")
async def check_address(address):
    signature = get_signatures(address)
    if signature:
        return quart.Response(response=json.dumps({"signature": signature[0]['signature']}), status=200)
    else:
        return quart.Response(response="Nice try, but your address is not authorized. 🤣", status=400)


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
    return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    with open("openapi.yaml") as f:
        text = f.read()
    return quart.Response(text, mimetype="text/yaml")

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)


if __name__ == "__main__":
    main()