from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA = [
  {"region":"apac","latency_ms":191.08,"uptime_pct":99.097},{"region":"apac","latency_ms":122.25,"uptime_pct":98.488},{"region":"apac","latency_ms":159.14,"uptime_pct":98.917},{"region":"apac","latency_ms":136.95,"uptime_pct":99.096},{"region":"apac","latency_ms":152.38,"uptime_pct":98.815},{"region":"apac","latency_ms":147.09,"uptime_pct":98.687},{"region":"apac","latency_ms":171.46,"uptime_pct":98.192},{"region":"apac","latency_ms":131.84,"uptime_pct":99.168},{"region":"apac","latency_ms":223.98,"uptime_pct":99.329},{"region":"apac","latency_ms":137.99,"uptime_pct":97.358},{"region":"apac","latency_ms":196.11,"uptime_pct":97.465},{"region":"apac","latency_ms":206.33,"uptime_pct":97.928},
  {"region":"emea","latency_ms":238.83,"uptime_pct":98.546},{"region":"emea","latency_ms":130.2,"uptime_pct":98.374},{"region":"emea","latency_ms":213.15,"uptime_pct":98.418},{"region":"emea","latency_ms":173.75,"uptime_pct":99.035},{"region":"emea","latency_ms":150.6,"uptime_pct":97.268},{"region":"emea","latency_ms":212.42,"uptime_pct":99.473},{"region":"emea","latency_ms":196.56,"uptime_pct":98.014},{"region":"emea","latency_ms":117.56,"uptime_pct":98.77},{"region":"emea","latency_ms":193.23,"uptime_pct":97.56},{"region":"emea","latency_ms":172.05,"uptime_pct":97.794},{"region":"emea","latency_ms":148.75,"uptime_pct":98.458},{"region":"emea","latency_ms":158.4,"uptime_pct":99.12},
  {"region":"amer","latency_ms":203.95,"uptime_pct":99.102},{"region":"amer","latency_ms":188.99,"uptime_pct":98.436},{"region":"amer","latency_ms":204.64,"uptime_pct":98.557},{"region":"amer","latency_ms":166.29,"uptime_pct":98.335},{"region":"amer","latency_ms":158.75,"uptime_pct":98.814},{"region":"amer","latency_ms":176.09,"uptime_pct":97.672},{"region":"amer","latency_ms":214.98,"uptime_pct":98.617},{"region":"amer","latency_ms":154.38,"uptime_pct":98.725},{"region":"amer","latency_ms":118.54,"uptime_pct":97.674},{"region":"amer","latency_ms":176.69,"uptime_pct":97.292},{"region":"amer","latency_ms":197.21,"uptime_pct":98.35},{"region":"amer","latency_ms":163.28,"uptime_pct":97.408},
]

@app.post("/api/analytics")
async def analytics(request: Request):
    body = await request.json()
    regions = body.get("regions", [])
    threshold = body.get("threshold_ms", 200)
    result = {}
    for region in regions:
        rows = [d for d in DATA if d["region"] == region]
        if not rows:
            continue
        lat = [r["latency_ms"] for r in rows]
        upt = [r["uptime_pct"] for r in rows]
        result[region] = {
            "avg_latency": round(float(np.mean(lat)), 2),
            "p95_latency": round(float(np.percentile(lat, 95)), 2),
            "avg_uptime": round(float(np.mean(upt)), 4),
            "breaches": int(sum(1 for l in lat if l > threshold))
        }
    return JSONResponse(
        content=result,
        headers={"Access-Control-Allow-Origin": "*"}
    )

@app.options("/api/analytics")
async def options():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )
