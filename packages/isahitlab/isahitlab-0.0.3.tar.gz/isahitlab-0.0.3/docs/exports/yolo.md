# Export to Yolo format

Yolo stands for “You Only Look Once”.

[More info about the format](https://yolov8.org/yolov8-label-format)

!!! info "Code Reference"
    See the [code reference](../task.md#isahitlab.actions.task.TaskActions.export_tasks) for further details.

## Compatibility

Export to Yolo format is available for:

* Project type *__Bounding Box__* (`iat-rectangle`)
* Project type *__Data processing__* (`form`) with input type:
    * *Bounding Box* (`tool-iat-rectangle`)

!!! warning "For *Data processing* project"
    The SDK will try to detect the input compatible with the export. 
    If more than one input is compatible, you must provide the `input_id` parameter to select the input to export.

## Output

Zip Archive

```
lab_yolo_`project_id`_`datetime`.zip/
├── data.yaml
└── labels
    ├── image_07750.jpg.txt
    ├── image_07751.jpg.txt
    └── image_07752.jpg.txt
```


## Usage

``` python
from isahitlab.client import IsahitLab

lab = IsahitLab()

lab.export_tasks(project_id="<project_id>", format="yolo")
```

You can filter the tasks with the same parameters than you can use to [get tasks](../task.md#isahitlab.actions.task.TaskActions.get_tasks).

``` python
from isahitlab.client import IsahitLab

lab = IsahitLab()

lab.export_tasks(project_id="<project_id>", 
                 format="yolo", 
                 batch_id_in=["<batch_id>"], 
                 status_in=["complete"], 
                 updated_at_gte="2024-12-25 00:00:00"
                 )
```

Use `output_folder` and / or `output_filename` to choose where to save the results.


``` python
from isahitlab.client import IsahitLab

lab = IsahitLab()

lab.export_tasks(project_id="<project_id>", 
                 format="yolo", 
                 output_folder="./output",
                 output_folder="my-export.zip"
                 )
```

!!! warning "Output name"
    If you set the `output_filename` parameter, it must end with `.zip`

!!! info "Directory tree"
    The SDK will automatically create the folder tree if you set an `output_folder` like `output/my_outputs/<project_id>`