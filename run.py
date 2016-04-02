from revolvr import server
import config

if __name__ == "__main__":
    server.run(host='0.0.0.0', debug=config.DEBUG)
