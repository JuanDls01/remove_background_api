# REMOVE BACKGROUND API

With this API you can remove the background of your selfies using [Selfie Segmentation](https://google.github.io/mediapipe/solutions/selfie_segmentation.html) model of [Mediapipe](https://google.github.io/mediapipe/). For run this API in local you have to run this code in the terminal at remove_backgroun_api folder:

```
$ python -m venv venv # windows
$ source venv/scripts/activate # activate virtual environment
$ pip install -r requirements.txt # install dependencies
$ uvicorn main:app --reload
```

Then, go to postman and send a selfie picture by form data like this:

- Original picture:

![initial image](/content/fotoperfil.jpeg "First Picture")

- Postman:

![postman image](/content/postman.png "Postman")

And see the results in preview response

![results image](/content/result.png)
