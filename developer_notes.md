

# Adding args to the launch.json

Note: if you want to use the config, pass the flag --use_config. If the intent is not to use the config
remove the flag altogether. 

```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
    
        {
            "name": "Python Debugger: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "args": ["--use_config", "-if", "C:/Plate_reader", "-of", "C:/plate_reader_frames", "-fname", "highway.mp4"]
        }
    ]
}

```




# running from the terminal 

```

python .\step01_my_fucking_video_splitter.py -if "C:/Plate_reader" -of "C:/plate_reader_frames" -fname "highway.mp4"

```
