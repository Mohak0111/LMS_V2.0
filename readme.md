#       setup required python packages and node modules:
        >       in backend, "pip install -r req.txt"
        >       in frontend, "npm install"



#       **BACKEND**:

#   Start redis server:
>   in wsl, "sudo service redis-server start"
>   enter the password when asked by the terminal, then to check connection, type "redis-cli"
>   type "ping" if you receive "pong", redis is up and running



#   Start flask server:
>   in any terminal of choice, "python main.py"



#   Start Mailhog server
>   in a wsl, navigate to "/go/bin"
>   type "./Mailhog"
<!-- http://172.29.30.148:8025/ -->






#   Start celery beat:
>   in the same wsl:
        celery -A main.celery beat --max-interval 1 -l info

        
#   Start celery workers:
>   in the same wsl, exit redis-cli connection and type:
        celery -A main.celery worker -l info







#       **FRONTEND**:

#   Start Vue Server:
>   navigate to the frontend folder from the terminal
>   type "npm run dev"
>   this will start the vue server