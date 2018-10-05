# Real-time plotter

*Real-time Plotter* is plot sensor data for real-time.  
Require [chartjs-plugin-streaming](https://github.com/nagix/chartjs-plugin-streaming)

## Usage

1. copy web scripts.

```
cp index.html /path/to/www
cp get_data.php /path/to/www
cp -r js /path/to/www
```

2. run data publish server.

```
sudo nohup python serial_to_socket.py &
```

## License

MIT License

