import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import openai

# 从环境变量获取OpenAI API密钥
openai.api_key = os.getenv('OPENAI_API_KEY')

# 定义请求体模型
class QuestionRequest(BaseModel):
    question: str

# 定义响应体模型
class AnswerResponse(BaseModel):
    answer: str

# 创建FastAPI应用
app = FastAPI()

# 创建HTTP Basic认证对象
security = HTTPBasic()

# 模拟验证函数，用于检查用户名和密码是否正确
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv('USERNAME')
    correct_password = os.getenv('PASSWORD')
    if (
        credentials.username == correct_username
        and credentials.password == correct_password
    ):
        return True
    else:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )

# 定义问题回答的路由，使用身份验证
@app.post("/answer", response_model=AnswerResponse)
def answer_question(request: QuestionRequest, authenticated: bool = Depends(authenticate)):
    question = request.question

    # 调用OpenAI API进行问题回答
    response = openai.Completion.create(
        engine="davinci",
        prompt=question,
        max_tokens=2049,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # 获取问题回答
    answer = response.choices[0].text.strip()

    # 返回回答
    return AnswerResponse(answer=answer)

