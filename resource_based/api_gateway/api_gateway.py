from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI(title="API Gateway")

@app.get("/")
def root():
    return {"message": "API Gateway is running"}

@app.api_route("/alarms/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def alarms_proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        target_url = f"http://alarm_storage:5001/alarms/{path}"
        response = await client.request(
            request.method,
            target_url,
            params=request.query_params,
            content=await request.body(),
            headers=request.headers,
        )
        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type")
        )