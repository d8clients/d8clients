# Docker instructions

To build the docker image (under name `nis-app`), use
```sh
docker build -t nis-app .
```

To run the container, you need to do several things:
- First, create a volume (let's call it `database`) for database persistence:
  ```sh
  docker volume create database
  ```
- Then, run the image in background, forwarding port `8080` to `0.0.0.0:80` and mounting database volume to `/app/db`:
  ```sh
  docker run -dp 0.0.0.0:80:8080 -v database:/app/db nis-app
  ```
