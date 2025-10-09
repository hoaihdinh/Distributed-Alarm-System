from fastapi import FastAPI, Request, Response
import httpx

ALARM_URL = "http://alarm_manager:5001/alarms"

app = FastAPI(title="API Gateway")

@app.get("/")
def root():
    return {"message": "API Gateway is running"}

@app.api_route("/alarms/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def alarms_proxy(request: Request, path: str):
    target_url = f"{ALARM_URL}/{path}" if path != "" else ALARM_URL
    async with httpx.AsyncClient() as client:
        response = await client.request(
            request.method,
            target_url,
            params=request.query_params,
            content=await request.body(),
            headers=dict(request.headers),
        )

        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type")
        )