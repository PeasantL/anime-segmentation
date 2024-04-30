# Character Card-V2 Background Segmentation 

Inference to remove backgrounds of [character-card-spec-v2](https://github.com/malfoyslastname/character-card-spec-v2)  

See [here](https://github.com/SkyTNT/anime-segmentation) for details on the removal process. 


## Run 

```
git clone https://github.com/PeasantL/anime-segmentation
cd anime-segmentation

./run.sh #Linux
./run.bat #Windows
```


## Inference Parameters

| Flag | Default | Desc |
| --- | --- | --- |
| --net |  isnet_is  | net name |
| --ckpt | saved_models/isnet_is.ckpt | model checkpoint path |
| --data | input | input data dir |
| --out | out | output dir |
| --img-size | 1024 | Hyperparameter, input image size of the net |
| --device | cuda:0 | cpu or cuda:0 |
| --fp32 | False | disable mix precision |
| --only-matted | True | only output matted image |

