# Background Remove with Deep Learning

This repository show the code to remove the background of the pictures using the [U2Net](https://github.com/xinntao/ESRGAN).

The code is clean and simple, and the application has three main functions:

1. Remove the background, producing a transparent PNG file.

2. Change the background by another picture.

3. Combine the image and multiple backgrounds to augment the dataset.


### Demos
![Demo](screenshot/demo1.gif)
![Demo](screenshot/demo2.gif)



### Endpoint available
| Endpoint | Description
| --- | ---
| http://localhost:8000/ |  Front-end to perform background remove.
| http://localhost:8000/augmentation |  Front-end to perform augment images.


### Install
1. Clone this repository
```bash
git clone https://github.com/renatoviolin/super-resolution-image-esrgan.git
cd bg-remove-augment/webapp
```

2. Download the pre-trained model
```bash
wget "https://www.dropbox.com/s/58x64ex9m047gdy/model.pth?dl=0" -O ckpt/u2net.pth
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Start web-application
```bash
cd webapp
uvicorn app:app --host 0.0.0.0 --port 8000
```

### References
ESRGAN (Enhanced SRGAN): [https://github.com/xinntao/ESRGAN](https://github.com/xinntao/ESRGAN)


### BibTeX
    @InProceedings{wang2018esrgan,
        author = {Wang, Xintao and Yu, Ke and Wu, Shixiang and Gu, Jinjin and Liu, Yihao and Dong, Chao and Qiao, Yu and Loy, Chen Change},
        title = {ESRGAN: Enhanced super-resolution generative adversarial networks},
        booktitle = {The European Conference on Computer Vision Workshops (ECCVW)},
        month = {September},
        year = {2018}
    }