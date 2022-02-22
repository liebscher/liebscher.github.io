Title: Deploying a containerized Heroku app with Apple's M1 processor
Date: 2021-11-19
Tags: programming, docker, python
Category: meta
Slug: deploying-heroku-app
Authors: Alex Liebscher
Summary: The M1 is fast and furious, but bound to cause headaches
Status: published

<style >
.file-name {
  color: #bbb;
  font-size: 0.9em;
}
</style>

It's common to want to deploy an app beyond your local machine and onto the web. A plethora of services and platforms now make this easy, compared to what it would have taken 10 or 20 years ago.

In this article, I'd like to outline one way to do so. Particularly, building a Python app, using Flask as a back-end server, bundling all the source files together with [Docker](https://www.heroku.com/), and deploying on Heroku. To add a twist, we're going to do this from a MacBook Pro with an Apple Silicon M1 processor, which demands special treatment in the eyes of Heroku.

## 1. Build your app

We're going to build a simple site that lands the user on a page, allows them fill out a form, and then shows them their submission.

To route traffic, handle requests, and serve static content, we'll be using [Flask](https://flask.palletsprojects.com/). A popular alternative is [Django](https://www.djangoproject.com/).

We'll start with our HTML landing page.

<div class="file-name">templates/index.html</div>

    :::html
    <!doctype html>

    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-sclae=1">

      <title>Example Heroku Deployment</title>
      <meta name="description" content="Deploying a containerized Heroku app with Apple's M1 processor">
    </head>

    <body>
      <h3>Example Heroku Deployment with Apple's M1 Processor</h3>
      <form action="" method="post">
        <p>
          <label for="name">Name</label>
          <input type="text" id="name" name="name">
        </p>
        <p>
          <input type="submit" value="Submit Form">
        </p>
      </form>
      {% if name_data %}
      <h4>Welcome, {{ name_data }}!</h4>
      {% endif %}
    </body>
    </html>

This shouldn't look alien; it is a simple HTML page with a form that submits by button, through POST, to itself. 

Then we'll build our Flask server.

<div class="file-name">server.py</div>

    :::python
    from flask import Flask, request, render_template
    import os

    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def index_get():
      return render_template('index.html')

    @app.route('/', methods=['POST'])
    def index_post():
      return render_template('index.html', name_data = request.form.get('name', ''))

    if __name__ == '__main__':
      port = int(os.environ.get('PORT', 5000))
      app.run(host='0.0.0.0', port=port)

When the user lands on the page without submitting anything, we just show the form. When the server receives a POST request, we pull out the *name* field from the request (assuming it's there, but default to `''` if not) and display that result.

We also look for the environment variable, `PORT`, which is really [for Heroku](https://blog.heroku.com/python_and_django). Heroku will choose and set the port which your app will use. We also set `host` to 0.0.0.0 which overrides the default locahost parameter so that the site is [accessible through Docker](https://stackoverflow.com/q/30323224/3234482).

## 2. Test locally

To test our web app locally, we can just run,

    :::shell
    python server.py

This launches our Flask app as a local server on a localhost port, specifically port 5000. Visit the URL `127.0.0.1:5000` to test.

## 3. Containerize your app

Now that we see our app working locally, we can [containerize the app](https://www.docker.com/blog/containerized-python-development-part-1/). By creating a container for our app, Heroku will be faster at deploying (since it won't have to rebuild the entire app every deployment), and it will ensure dependencies and architectures are platform-agnostic.

Or, almost platform-agnostic. I learned the hard way that Docker is particular in certain ways about the host build machine and its architecture. In particular, the architecture of an M1 Mac requires Docker to build apps differently than what Heroku wants to deploy them.

In any case, we need to start with a Dockerfile, so we'll do that.

First, we'll be starting from a Python 3.8 image as the base layer.

    :::docker
    FROM python:3.8

We need to install our Python dependencies. This could also be done with a requirements file, but here we just write them out.

    :::docker
    RUN pip install flask

We need to copy our HTML and Python source files into the image.

    :::docker
    COPY . .

Flask expects to host the server through an open port, so we'll expose a port just for Flask.

    :::docker
    EXPOSE $PORT

Lastly, the launch command when we run the image as a container is to launch the server. We'll bring it all together here now,

<div class="file-name">Dockerfile</div>

    :::docker
    FROM python:3.8

    RUN pip install flask

    COPY . .

    EXPOSE $PORT

    CMD [ "python", "server.py" ]

For more of this process, see the [documentation](https://devcenter.heroku.com/articles/container-registry-and-runtime). Now we need to build the image. Typically, we'd see,

    :::shell
    docker build . -t example-app

but because we're working on a different architecture, we actually need,

    :::shell
    docker buildx build --platform linux/amd64 -t example-app .

`buildx` allows the devloper to, among other things, build an image to run cross-platform. This is important to us since our source machine, an Apple M1 device, is a different architecture (`arm64`) than the destination machine (`amd64`).

Now that we have it setup with the right architecture, we can test the image locally by building a container. For example,

    :::shell
    docker run --rm -e PORT=5000 -p 5000:5000 example-app

To break down the arguments here: `--rm` removes the container from the running container list once it exits, `-e PORT=5000` sets our port environment variable, and `-p 5000:5000` opens the port 5000 within the container to the host machine's port 5000. The last argument is the name of our image to run.

Now we can visit the exposed port (`127.0.0.1:5000/`) and see our app live, locally.

## 4. Push to Heroku

First, we need to create a Heroku account. After that's been setup, create an app with any name you want, say `example-heroku-deployment`.

We'll be deploying to the Heroku registry manually, but we still will use the Heroku CLI for some parts, so make sure that's [installed](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

We'll authenticate Heroku from the command line, make sure Docker is [installed](https://docs.docker.com/get-docker/), and login to the Heroku Container Registry,

    :::shell
    heroku login
    docker ps
    heroku container:login

Now, we want to retag our image with the location of our Heroku app registry. For example, if we run `docker images`, we can view the image ID of the image we just built for `example-app`. In order to get our local image to the right place in the Heroku Registry, we need to label it correctly,

    :::shell
    docker tag xxxxxxxxxxxx registry.heroku.com/example-heroku-deployment/web

where the image ID is copy and pasted from the `docker images` command.

Next we want to manually push the image to the Registry, like,

    :::shell
    docker push registry.heroku.com/example-heroku-deployment/web

Now our app is pushed up to Heroku, and we just need to tell Heroku to take the image live!

    :::shell
    heroku container:release web -a example-heroku-deployment

To open your app, try `heroku open -a example-heroku-deployment`.

## 5. Wrap up

You should be seeing your site live at *example-heroku-deployment.heroku.com* (or whatever you named your app as, followed by *heroku.com*).

A troubleshooting appendix should come soon!

<!-- # Troubleshooting

## 1. Heroku H10 error

Notorious! -->