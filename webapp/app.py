import logging
import uuid
import os
from fastapi import FastAPI, File, Request, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import engine
from typing import List
from PIL import Image


app = FastAPI()
UPLOAD_FOLDER = "images-input"
OUTPUT_FOLDER = "images-output"
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images-input", StaticFiles(directory=UPLOAD_FOLDER), name="images-input")
app.mount("/images-output", StaticFiles(directory=OUTPUT_FOLDER), name="images-output")
templates = Jinja2Templates(directory="templates")


# %% ---------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

@app.get("/augmentation", response_class=HTMLResponse)
async def augmentation(request: Request):
    return templates.TemplateResponse("augmentation.html", context={"request": request})


@app.post("/remove-bg", response_class=HTMLResponse)
async def remove_bg(request: Request, file: UploadFile = File(...)):
    try:
        new_name = str(uuid.uuid4()).split("-")[0]
        ext = file.filename.split(".")[-1]
        file_name = f"{UPLOAD_FOLDER}/{new_name}.{ext}"

        with open(file_name, "wb+") as f:
            f.write(file.file.read())

        input_image = Image.open(file_name)
        img_pil = engine.remove_bg_mult(input_image)

        output_image = os.path.join(OUTPUT_FOLDER, f'{new_name}.png')
        img_pil.save(output_image)

        return templates.TemplateResponse("results.html", context={"request": request,
                                                                   'original_path': file_name,
                                                                   'filepath': output_image,
                                                                   'img_no_bk': f'{new_name}.png'})
    except Exception as ex:
        logging.info(ex)
        print(ex)
        return JSONResponse(status_code=400, content={"error": str(ex)})


@app.post("/change-bg")
async def change_bg(img_no_bk: str = Form(...), file: UploadFile = File(...)):
    try:
        new_name = str(uuid.uuid4()).split("-")[0]
        ext = file.filename.split(".")[-1]
        file_name = f"{UPLOAD_FOLDER}/{new_name}_bk.{ext}"

        with open(file_name, "wb+") as f:
            f.write(file.file.read())

        input_img = Image.open(os.path.join(OUTPUT_FOLDER, img_no_bk)).convert("RGBA")
        input_bk = Image.open(file_name).convert("RGBA")

        new_img = engine.change_background(input_img, input_bk)
        output_image = os.path.join(OUTPUT_FOLDER, f'{new_name}.png')
        new_img.save(output_image)

        return JSONResponse(
            status_code=200,
            content={
                'img_with_bk': output_image,
                'img_no_bk': img_no_bk,
            },
        )

    except Exception as ex:
        logging.info(ex)
        print(ex)
        return JSONResponse(status_code=400, content={"error": str(ex)})


@app.post("/generate-augmentation")
async def generate_augmentation(file_input: UploadFile = File(...), files_background: List[UploadFile] = File(...)):
    bk_paths = []
    try:
        # save input file
        new_name = str(uuid.uuid4()).split("-")[0]
        ext = file_input.filename.split(".")[-1]
        input_fname = f"{UPLOAD_FOLDER}/{new_name}.{ext}"
        with open(input_fname, "wb+") as f:
            f.write(file_input.file.read())

        # save all background files
        for file in files_background:
            new_name = str(uuid.uuid4()).split("-")[0]
            ext = file_input.filename.split(".")[-1]
            bk_fname = f"{UPLOAD_FOLDER}/{new_name}.{ext}"
            with open(bk_fname, "wb+") as f:
                f.write(file.file.read())
            bk_paths.append(bk_fname)

        # remove bk from input file
        input_image = Image.open(input_fname)
        input_pil = engine.remove_bg_mult(input_image)

        new_name = str(uuid.uuid4()).split("-")[0]
        no_bk_path = os.path.join(OUTPUT_FOLDER, f'{new_name}.png')
        input_pil.save(no_bk_path)


        # merge with each bk
        output_bk = []
        for bk_path in bk_paths:
            new_name = str(uuid.uuid4()).split("-")[0]
            input_bk = Image.open(bk_path).convert("RGBA")
            new_img = engine.change_background(input_pil, input_bk)
            output_path = os.path.join(OUTPUT_FOLDER, f'{new_name}.png')
            new_img.save(output_path)
            output_bk.append(output_path)



        return JSONResponse(
                    status_code=200,
                    content={
                        'img_no_bk': no_bk_path,
                        'augmentations': output_bk,
                    },
                )
    except Exception as ex:
        logging.info(ex)
        return JSONResponse(status_code=400, content={"error": str(ex)})


# @app.post('/api/process')
# async def process(files: List[UploadFile] = File(...)):
#     res = []
#     try:
#         for file in files:
#             d = {}
#             name = str(uuid.uuid4()).split('-')[0]
#             ext = file.filename.split('.')[-1]
#             file_name = f'{UPLOAD_FOLDER}/{name}.{ext}'
#             with open(file_name, 'wb+') as f:
#                 f.write(file.file.read())
#             f.close()

#             confidence, idx = engine.predict(file_name)

#             d['file'] = f'images/{name}.{ext}'
#             d['confidence'] = f'{confidence:.3f}'
#             d['prediction'] = labels[idx]
#             res.append(d)
#         return JSONResponse(status_code=200, content=res)
#     except Exception as ex:
#         logger.info(ex)
#         return JSONResponse(status_code=400, content=str(ex))


# @app.post("/api/remove-bg")
# async def api_recommend(file: UploadFile = File(...)):
#     try:
#         new_name = str(uuid.uuid4()).split("-")[0]
#         ext = file.filename.split(".")[-1]
#         file_name = f"{UPLOAD_FOLDER}/{new_name}.{ext}"

#         with open(file_name, "wb+") as f:
#             f.write(file.file.read())

#         img_array_full, bboxes, scores, classes, = engine.predict(img_path=file_name)
#         output_image = os.path.join(OUTPUT_FOLDER, f'{new_name}.jpg')
#         cv2.imwrite(output_image, img_array_full)

#         return JSONResponse(
#             status_code=200,
#             content={
#                 'img': output_image,
#                 'scores': scores,
#                 'bbox': bboxes,
#                 'classes': classes
#             },
#         )
#     except Exception as ex:
#         logging.info(ex)
#         return JSONResponse(status_code=400, content={"error": str(ex)})
