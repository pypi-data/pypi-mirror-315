# streamlit-custom-component

Streamlit component that allows you to do X

## Installation instructions

```sh
pip install streamlit-custom-component
```

## Important!

```
This should be used with session state to hold the current state of the kanban, 
more information you can find in the sample code example.py
```

## Usage instructions

```python

#The component should receive a data structure JSON like this sample below:

    data = {
        "columns": [
            {
                "id": "todo",
                "title": "To Do",
                "cards": [
                    {"id": "card-1", "name": "Task 1", "fields": ["Bug"], "color": "#FF5555"},
                    {"id": "card-2", "name": "Task 2", "fields": ["Bug"], "color": "#55FF55"},
                ],
            },
            {
                "id": "in-progress",
                "title": "In Progress",
                "cards": [
                    {"id": "card-3", "name": "Task 3", "fields": ["Bug"], "color": "#5555FF"},
                ],
            },
            {"id": "done", "title": "Done", "cards": []},
        ]
    }

For more example on how to call it please look into example.py file
```