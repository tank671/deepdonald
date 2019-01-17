from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn, aiohttp, asyncio
from io import BytesIO
from pathlib import Path
import sys
import csv

from fastai import *
from fastai.text import *


model_file_url = 'https://github.com/tank671/deepdonald/blob/master/app/models/trump_all.pth?raw=true'
model_file_name = 'trump_all'
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

async def setup_learner():
    await download_file(model_file_url, path/'models'/f'{model_file_name}.pth')
    trump_lm = TextLMDataBunch.load(path/'static', 'trump_lm')
    data_bunch = (TextList.from_csv(path, csv_name='static/blank.csv', vocab=trump_lm.vocab)
        .random_split_by_pct()
        .label_for_lm()
        .databunch(bs=10))
    learn = language_model_learner(data_bunch, pretrained_model=None)
    learn.load(model_file_name)
    return learn

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

exec(open(path/"textfuncs.py").read())

@app.route('/')
def index(request):
    html = path/'view'/'index.html'
    return HTMLResponse(html.open().read())

@app.route('/analyze', methods=['POST'])
async def analyze(request):
    data = await request.form()
    return JSONResponse({'result': textResponse(data)})

def textResponse(data):
    starter = data['file']
    if starter != '':
        res = generate_text(starter=starter)
    else:
        res = generate_text()
    return res

if __name__ == '__main__':
    if 'serve' in sys.argv: uvicorn.run(app, host='0.0.0.0', port=5000)

