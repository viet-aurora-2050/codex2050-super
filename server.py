
from flask import Flask, request, jsonify, send_from_directory
import time, hashlib, os

app = Flask(__name__)

STATE = {
    "chainId": "0x321A8",
    "netVersion": "205000",
    "blockNumber": 1,
    "balances": {},
    "txs": []
}

def to_hex(n): return hex(int(n))

def ensure_demo_funds(addr):
    addr = addr.lower()
    if addr not in STATE["balances"]:
        STATE["balances"][addr] = 100 * 10**18

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/rpc", methods=["POST"])
def rpc():
    payload = request.get_json(force=True, silent=True) or {}
    method = payload.get("method")
    params = payload.get("params", [])
    req_id = payload.get("id", 1)

    def resp(result=None, error=None):
        base={"jsonrpc":"2.0","id":req_id}
        if error: base["error"]=error
        else: base["result"]=result
        return jsonify(base)

    if method=="eth_chainId": return resp(STATE["chainId"])
    if method=="net_version": return resp(STATE["netVersion"])
    if method=="eth_blockNumber": return resp(to_hex(STATE["blockNumber"]))

    if method=="eth_getBalance":
        if not params: return resp(error={"code":-32602,"message":"Missing params"})
        addr=params[0]
        ensure_demo_funds(addr)
        return resp(to_hex(STATE["balances"][addr.lower()]))

    if method=="eth_sendRawTransaction":
        raw=params[0] if params else ""
        blob=f"{raw}-{time.time()}".encode()
        tx_hash="0x"+hashlib.sha256(blob).hexdigest()
        STATE["txs"].append({"hash":tx_hash,"raw":raw,"timestamp":int(time.time()),"blockNumber":STATE["blockNumber"]+1})
        STATE["blockNumber"]+=1
        return resp(tx_hash)

    if method=="vl2050_getTxs":
        return resp(STATE["txs"][-50:])

    return resp(error={"code":-32601,"message":f"Method {method} not found"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8000)))
