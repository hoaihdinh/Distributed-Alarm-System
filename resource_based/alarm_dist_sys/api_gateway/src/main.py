from fastapi import FastAPI, Request, Response, Query
import httpx

ALARM_URL = "http://alarm_manager:5001/alarms"
USER_URL  = "http://user_manager:5002/users"
NOTIFICATION_URL = "http://notification_manager:5003/notifications"

app = FastAPI(title="API Gateway")

@app.get("/")
def root():
    return {"message": "API Gateway is running"}

@app.api_route("/alarms/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def alarms_proxy(request: Request, path: str):
    target_url = f"{ALARM_URL}/{path}" if path != "" else ALARM_URL
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
        response = await client.request(
            request.method,
            target_url,
            params=dict(request.query_params),
            content=await request.body(),
            headers=dict(request.headers),
        )

        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type")
        )
    
@app.api_route("/users/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def users_proxy(request: Request, path: str):
    target_url = f"{USER_URL}/{path}" if path != "" else USER_URL
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
        response = await client.request(
            request.method,
            target_url,
            params=dict(request.query_params),
            content=await request.body(),
            headers=dict(request.headers),
        )

        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type")
        )

@app.api_route("/notifications/{path:path}", methods=["GET", "DELETE"])
async def notificaion_proxy(request: Request, path: str):
    target_url = f"{NOTIFICATION_URL}/{path}" if path != "" else NOTIFICATION_URL
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
        response = await client.request(
            request.method,
            target_url,
            params=dict(request.query_params),
            content=await request.body(),
            headers=dict(request.headers),
        )

        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type")
        )
