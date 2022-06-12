---
title: CloudApp
---

<div class="text-center">
  <!-- You can use Vue components inside markdown -->
  <div i-carbon-dicom-overlay class="text-4xl -mb-6 m-auto" />
  <h2>Blog</h2>
</div>

[FastAPI](https://fastapi.tiangolo.com) is a progressive, performant and highly scalable ASGI [Python](https://python.org) web framework specially designed for great developer experience on making APIs, specially REST APIs with sweet features out of the box such as auto-documentation, easy dependency injection, built-in security standards such as JWT, OAuth2 and OpenID, rich ecosystem with ORM such as Tortoise and SQL (this one made by the same author).
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
async def main():
  return {
    "message": "Hello Vue"
  }

```

```json
    POST https://YOUR_DOMAIN/passwordless/start
Content-Type: application/json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET", // for web applications
  "connection": "email|sms",
  "email": "USER_EMAIL", //set for connection=email
  "phone_number": "USER_PHONE_NUMBER", //set for connection=sms
  "send": "link|code", //if left null defaults to link
  "authParams": { // any authentication parameters that you would like to add
    "scope": "openid",
    "state": "YOUR_STATE"
  }
}
```


</div>
</template>